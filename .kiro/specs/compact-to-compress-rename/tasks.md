# 実装計画

- [x] 1. バックエンドファイル名とモジュール構造の変更
  - `backend/app/usecases/compact_conversation.py` を `compress_conversation.py` にリネーム
  - インポート文を更新してファイル名変更を反映
  - _要件: 3.4, 3.5_

- [x] 2. バックエンドスキーマとクラス名の変更
- [x] 2.1 conversation.py スキーマの更新
  - `CompactConversationRequest` クラス名を `CompressConversationRequest` に変更
  - `type: Literal["compact_conversation"]` を `type: Literal["compress_conversation"]` に変更
  - `ChatRequest` Union型の更新
  - _要件: 3.3, 4.1, 4.2_

- [x] 2.2 compress_conversation.py の関数名変更
  - `compact_conversation()` 関数を `compress_conversation()` に変更
  - `format_messages_for_compact()` 関数を `format_messages_for_compress()` に変更
  - 関数内のコメントとログメッセージを更新
  - _要件: 3.1, 3.2_

- [x] 2.3 websocket.py の処理関数更新
  - `process_compact_conversation()` 関数を `process_compress_conversation()` に変更
  - インポート文を更新（`compact_conversation` → `compress_conversation`）
  - `CompactConversationRequest` 型参照を `CompressConversationRequest` に変更
  - 条件分岐での型チェックを更新
  - _要件: 3.1, 3.2, 3.3_

- [x] 3. フロントエンド型定義の変更
- [x] 3.1 conversation.d.ts の型定義更新
  - `CompactConversationRequest` 型を `CompressConversationRequest` に変更
  - `type: 'compact_conversation'` を `type: 'compress_conversation'` に変更
  - `ConversationRequest` Union型の更新
  - _要件: 2.4, 4.2_

- [x] 4. フロントエンドコンポーネントとフックの変更
- [x] 4.1 useChat.ts フックの更新
  - `compactConversation` 関数を `compressConversation` に変更
  - `CompactConversationRequest` 型参照を `CompressConversationRequest` に変更
  - `type: 'compact_conversation'` を `type: 'compress_conversation'` に変更
  - エクスポートする関数名を更新
  - _要件: 2.1, 2.2_

- [x] 4.2 ChatPage.tsx コンポーネントの更新
  - `compactConversation` 変数を `compressConversation` に変更
  - `onCompactConversation` 関数を `onCompressConversation` に変更
  - useChat フックからの分割代入を更新
  - InputChatContent への props 渡しを更新
  - _要件: 2.1, 2.2_

- [x] 4.3 InputChatContent.tsx コンポーネントの更新
  - Props インターフェースの `onCompactConversation` を `onCompressConversation` に変更
  - ボタンの onClick ハンドラーを更新
  - _要件: 2.1, 2.2_

- [x] 4.4 InputChatContent.stories.tsx ストーリーファイルの更新
  - デフォルト props の `onCompactConversation` を `onCompressConversation` に変更
  - _要件: 2.1, 2.2_

- [x] 5. 国際化ファイルの更新
- [x] 5.1 英語翻訳ファイルの更新
  - `frontend/src/i18n/en/index.ts` の `compact: 'Compact'` を `compress: 'Compress'` に変更
  - _要件: 1.1, 1.4_

- [x] 5.2 日本語翻訳ファイルの更新
  - `frontend/src/i18n/ja/index.ts` の `compact: '会話の圧縮'` を `compress: '会話の圧縮'` に変更（キーのみ変更）
  - _要件: 1.1, 1.4_

- [ ]* 5.3 その他言語の翻訳ファイル確認と更新
  - 他の言語ファイルで `compact` キーが存在する場合は `compress` に更新
  - _要件: 1.2_

- [-] 6. 統合テストと動作確認
- [ ] 6.1 バックエンド機能テスト
  - 新しい `compress_conversation` 関数の動作確認
  - WebSocket経由での圧縮機能の動作確認
  - API スキーマの整合性確認
  - _要件: 5.1, 5.2, 5.3_

- [ ] 6.2 フロントエンド機能テスト
  - Compress ボタンの表示と動作確認
  - 多言語でのボタンラベル表示確認
  - 会話圧縮機能の完全なフロー確認
  - _要件: 5.1, 5.4, 5.5_

- [ ]* 6.3 回帰テスト実行
  - 既存の会話機能に影響がないことを確認
  - パフォーマンスの劣化がないことを確認
  - エラーハンドリングが正常に動作することを確認
  - _要件: 5.1, 5.2, 5.3, 5.4, 5.5_