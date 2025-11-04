# 設計書

## 概要

この設計書では、チャットインターフェースの「Compact」ボタンに適切なアイコンを追加する実装について詳述します。現在の「Regenerate」ボタンと同様のパターンに従い、視覚的な一貫性を保ちながら、コンパクト化機能を表現する直感的なアイコンを追加します。

## アーキテクチャ

### 現在の実装
- `InputChatContent.tsx`コンポーネント内で、RegenerateボタンとCompactボタンが並んで配置されている
- Regenerateボタンは`PiArrowsCounterClockwise`アイコンを使用
- Compactボタンは現在テキストのみで表示

### 提案する変更
- Compactボタンに適切なPhosphor Iconsライブラリのアイコンを追加
- 既存のRegenerateボタンと同じスタイリングパターンを適用
- アイコンとテキストの間隔を統一

## コンポーネントとインターフェース

### 影響を受けるファイル
- `frontend/src/components/InputChatContent.tsx` - メインの実装ファイル

### アイコンの選択

コンパクト化機能に適したPhosphor Iconsの候補：

1. **PiCompress** (推奨) - 圧縮を表現する最も直接的なアイコン
2. **PiArrowsInSimple** - 内向きの矢印でコンテンツを凝縮する概念を表現
3. **PiMinusSquare** - コンテンツを縮小する概念を表現
4. **PiStack** - コンテンツを整理・積み重ねる概念を表現
5. **PiArrowsIn** - 内向きの矢印でコンパクト化を表現

**推奨アイコン**: `PiCompress`
- 理由: コンパクト化の概念を最も直接的に表現
- 国際的に理解しやすい
- 既存のRegenerateアイコンと視覚的に区別しやすい

### 実装パターン

```tsx
// 現在のRegenerateボタンの実装
<Button
  className="bg-aws-paper-light p-2 text-sm dark:bg-aws-paper-dark"
  outlined
  disabled={props.disabledRegenerate || props.disabled}
  onClick={() => {
    props.onRegenerate(reasoningEnabled);
  }}>
  <PiArrowsCounterClockwise className="mr-2" />
  {t('button.regenerate')}
</Button>

// 提案するCompactボタンの実装
<Button
  className="bg-aws-paper-light p-2 text-sm dark:bg-aws-paper-dark"
  outlined
  disabled={props.disabledRegenerate || props.disabled}
  onClick={props.onCompactConversation}>
  <PiCompress className="mr-2" />
  {t('button.compact')}
</Button>
```

## データモデル

この変更はUIのみの変更であり、データモデルに影響はありません。

## エラーハンドリング

- アイコンの読み込みエラー: Phosphor Iconsライブラリが既に使用されているため、新しいエラーハンドリングは不要
- フォールバック: アイコンが表示されない場合でも、テキストは表示され続ける

## テスト戦略

### 視覚的テスト
1. ライトテーマとダークテーマでのアイコン表示確認
2. Regenerateボタンとの視覚的一貫性確認
3. 異なる画面サイズでの表示確認

### 機能テスト
1. アイコン追加後もボタンの機能が正常に動作することを確認
2. アイコンとテキストの間隔が適切であることを確認
3. ボタンのクリック領域が適切であることを確認

### アクセシビリティテスト
1. スクリーンリーダーでの読み上げ確認
2. キーボードナビゲーションの確認
3. 色覚異常者への配慮確認

## 実装の詳細

### インポート文の追加
```tsx
import { PiArrowsCounterClockwise, PiCompress } from 'react-icons/pi';
```

### CSSクラスの適用
- `mr-2`: アイコンとテキスト間の右マージン（既存パターンと同じ）
- 他のスタイリングは既存のボタンスタイルを継承

### 国際化対応
- テキスト部分は既存の翻訳システム（`t('button.compact')`）を使用
- アイコンは言語に依存しないため、追加の国際化対応は不要

## パフォーマンス考慮事項

- Phosphor Iconsライブラリは既に使用されているため、新しい依存関係は不要
- アイコンの追加によるバンドルサイズへの影響は最小限
- レンダリングパフォーマンスへの影響は無視できる程度

## セキュリティ考慮事項

この変更はUIのみの変更であり、セキュリティへの影響はありません。

## 今後の拡張性

- 他のアクションボタンにも同様のアイコン追加パターンを適用可能
- アイコンのカスタマイズ機能の追加が容易
- テーマに応じたアイコンの変更が可能