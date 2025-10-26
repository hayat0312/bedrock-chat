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
    CompactConversationRequest,
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


def compact_conversation(
    user: User,
    request: CompactConversationRequest,
    on_stream: Callable[[str], None] | None = None,
    on_stop: Callable[[OnStopInput], None] | None = None,
) -> tuple[ConversationModel, MessageModel]:
    conversation = find_conversation_by_id(user.id, request.conversation_id)
    message_map = conversation.message_map

    # これまでの会話内容
    messages = trace_to_root(
        node_id=request.parent_message_id,
        message_map=message_map,
    )

    # strands agents を使って、これまでの会話内容に関するレポートを生成させる
    result = converse_with_strands(
        bot=None,
        model_name="claude-v4.5-sonnet",  # レポートの生成に使うモデル
        instructions=[
            "ここまでの会話内容をレポートにまとめて",  # これまでの会話内容に関するレポートを生成するためのプロンプト
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
                        body=str(messages),  # これまでの会話内容を含むメッセージ
                    )
                ],
            ),
        ],
        search_results=[],
        on_stream=on_stream,
    )

    # これまでの会話内容に関するレポートを含むメッセージ
    message = result["message"]
    print("！！！ ", message)


    # 生成されたレポートを使い、新たな会話ツリーで会話を開始する
    return chat(
        user=user,
        chat_input=ChatInput(
            conversation_id=request.conversation_id,
            message=MessageInput(
                role="user",
                content=[
                    TextContent(
                        content_type="text",
                        body="これまでの会話内容を理解して。 " + str(message),  # これまでの会話内容に関するレポートと、それを理解させるためのプロンプトを含むメッセージ
                    ),
                ],
                model=request.model,
                parent_message_id="system",  # 新たな会話ツリーとするため、システムプロンプトを親とするルートメッセージとする
                message_id=None,
            ),
            bot_id=request.bot_id,
            continue_generate=False,
            enable_reasoning=False,
        ),
        on_stream=on_stream,
        on_stop=on_stop,
    )
