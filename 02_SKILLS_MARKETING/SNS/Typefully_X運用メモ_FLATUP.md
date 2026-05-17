# Typefully X運用メモ FLATUP

作成日: 2026-05-17

## 目的

FLATUP GYMのX投稿を、AIで下書きし、Typefullyで安全に管理するための運用メモ。

AIは投稿案とスレッド構成を作る。Typefullyは下書き保存と予約管理を担当する。公開は必ず人間が確認してから行う。

## 現在の状態

| 項目 | 状態 |
|---|---|
| Typefully API 疎通 | ローカルPCから確認済み |
| 設定ファイル | `/Users/jin/.config/typefully/config.json` |
| ファイル権限 | `600` |
| default social set ID | `307036` |
| username | `flatupgym` |
| APIキー | Obsidian/Git/READMEには保存しない |

注意: 今回の接続確認では、キーは `tf_` を外した形式で成功した。

## 運用憲法

1. 公開は人間の明示承認後のみ。
2. AIは即時公開しない。
3. 1日のX投稿は最大5本。
4. オリジナル比率は70%以上。
5. APIキーは絶対にコミットしない。
6. 自動リプライ・自動いいね・自動フォローは禁止。

## FLATUPでの使い方

まずAIOSで投稿案を作る。

```bash
cd "/Users/jin/Desktop/OPENQLOW HelMES/flatup-ai-os"
npm run dev -- sns_post "X向け。弱い自分と戦う人へ届ける短いスレッド"
```

その後、Typefullyに下書き保存する。

`asukenn` リポの Typefully skill が使える場合:

```bash
cd "/path/to/asukenn"
./.claude/skills/x-post/scripts/typefully.js config:show
./.claude/skills/x-post/scripts/typefully.js drafts:create --platform x --text "投稿本文"
```

公式 Typefully skill を使う場合:

```bash
<skill-path>/scripts/typefully.js config:show
<skill-path>/scripts/typefully.js drafts:create --platform x --text "投稿本文"
```

最後にTypefully画面で人間が確認し、必要なら修正してから公開・予約する。

## 週間フロー

| 曜日 | 内容 |
|---|---|
| 月 | 今週のテーマ決定 |
| 火-木 | 投稿案作成・レビュー |
| 金 | Typefullyで翌週分を予約 |
| 日 | 反応を見て振り返り |

## 投稿テーマの優先順位

1. 弱い自分と戦う人へ
2. 世界一初心者に優しい格闘技ジム
3. 女性・子供・未経験者が安心して通える
4. 格闘技は人生を変える
5. 成田 FLATUP GYMのリアルな日常

## 安全チェック

- 同じ日に5本を超えていないか。
- 参考元の翻訳ではなく、FLATUPの経験と言葉になっているか。
- 会員個人が特定されないか。
- 体験・入会を煽りすぎていないか。
- 投稿前に人間が読んだか。

## 関連ファイル

- `/Users/jin/Desktop/OPENQLOW HelMES/flatup-ai-os/docs/typefully_x_ops.md`
- `/Users/jin/Documents/Obsidian Vault/6_システム/FLATUP_AI_OS_オーナー用コマンド早見表.md`
- `/Users/jin/Documents/Obsidian Vault/02_SKILLS_MARKETING/SNS/FLATUP GYM ブランド構築・SNS戦略 対話履歴.md`
