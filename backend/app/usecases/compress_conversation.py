import logging
from typing import Callable

from app.repositories.conversation import find_conversation_by_id
from app.repositories.models.conversation import (
    ConversationModel,
    MessageModel,
    SimpleMessageModel,
    TextContentModel,
)
from app.routes.schemas.conversation import (
    CompressConversationRequest,
    ChatInput,
    MessageInput,
    TextContent,
)
from app.strands_integration.chat_strands import converse_with_strands
from app.stream import OnStopInput
from app.usecases.chat import chat, trace_to_root
from app.user import User

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def format_messages_for_compress(messages):
    """Format messages into alternating user_prompt and agent_reply format for compress conversation"""
    formatted = []

    for message in messages:
        # Skip system messages (empty content)
        if message.role == 'system':
            continue

        # Get the text content from the message
        if message.content and len(message.content) > 0:
            # Handle both TextContentModel and other content types
            content = ""
            for content_item in message.content:
                if hasattr(content_item, 'body'):
                    content += content_item.body
                elif hasattr(content_item, 'text'):
                    content += content_item.text

            if content:  # Only add if there's actual content
                if message.role == 'user':
                    formatted.append(f"user_prompt:{content}")
                elif message.role == 'assistant':
                    formatted.append(f"agent_reply:{content}")

    return str(formatted)


def extract_body_from_message(message):
    """Extract body content from MessageModel structure"""
    if hasattr(message, 'content') and message.content:
        for content_item in message.content:
            if hasattr(content_item, 'body'):
                return content_item.body
            elif hasattr(content_item, 'text'):
                return content_item.text
    return str(message)  # Fallback to string representation


def compress_conversation(
    user: User,
    request: CompressConversationRequest,
    on_stream: Callable[[str], None] | None = None,
    on_stop: Callable[[OnStopInput], None] | None = None,
) -> tuple[ConversationModel, MessageModel]:
    conversation = find_conversation_by_id(user.id, request.conversation_id)
    message_map = conversation.message_map

    # Conversations so far
    messages = trace_to_root(
        node_id=request.parent_message_id,
        message_map=message_map,
    )
    formatted_messages = format_messages_for_compress(messages)

    # Use strands agents to generate reports on conversations so far
    result = converse_with_strands(
        bot=None,
        model_name="claude-v4.5-sonnet",
        instructions=[
            "Read the following conversation with user and AI agent and create a summary report to compress the context volume. " +
            "This report aims to significantly reduce the token count while preserving the essential elements of the original information. " +
            "Create in a format that is easy for GenAI to understand, keeping in mind that GenAI will read this report later, take over the context, and resume the conversation." +
            "Write in the language used in conversation up until now.",
        ],
        generation_params=None,
        guardrail=None,
        enable_reasoning=False,
        display_citation=False,
        messages=[
            SimpleMessageModel(
                role="user",
                content=[
                    TextContentModel(
                        content_type="text",
                        body=formatted_messages,  # A message containing a formatted conversation
                    )
                ],
            ),
        ],
        search_results=[],
        on_stream=on_stream,
    )

    # A message containing a report on the conversation so far
    summary = result["message"]
    summary_body = extract_body_from_message(summary)

    # Use generated reports to start conversations in a new conversation tree
    return chat(
        user=user,
        chat_input=ChatInput(
            conversation_id=request.conversation_id,
            message=MessageInput(
                role="user",
                content=[
                    TextContent(
                        content_type="text",
                        body="Read the report shown below and understand the conversation so far. " +
                        "Briefly display the content in the language the report was written in." +
                        summary_body,
                    ),
                ],
                model=request.model,
                # In order to create a new conversation tree, use the system prompt as the root message as the parent
                parent_message_id="system",
                message_id=None,
            ),
            bot_id=request.bot_id,
            continue_generate=False,
            enable_reasoning=False,
        ),
        on_stream=on_stream,
        on_stop=on_stop,
    )
