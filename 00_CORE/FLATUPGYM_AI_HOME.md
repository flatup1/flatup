# FLATUPGYM AI HOME

最終更新: 2026-05-17

ここは、JINの分身として育てる **FLATUPGYM AI** の入口です。

Obsidian Vaultを「記憶」、FLATUP AI OSを「実行エンジン」、GitHubを「成長履歴」として使います。

```text
JINの考え・現場の出来事
        ↓
Obsidian Vaultに記録
        ↓
AIが整理・下書き・改善案を作る
        ↓
JINが承認
        ↓
GitHubにcommit/push
        ↓
次回のAIが履歴を読んで賢くなる
```

## まず見るもの

| 目的 | ファイル |
|---|---|
| 使い方を知る | `6_システム/FLATUPGYM_AI_使い方.md` |
| できることを一覧で見る | `6_システム/FLATUPGYM_AI_機能一覧.md` |
| 何を学んだか見る | `4_日記/FLATUPGYM_AI_学習ログ.md` |
| GitHubで育てる方法 | `6_システム/FLATUPGYM_AI_GitHub運用.md` |
| AIKA本番人格 | `1_AIKA人格_本番.md` |
| Codex/Claudeへの全体指示 | `CLAUDE.md` / `AGENTS.md` |

## FLATUPGYM AIの役割

FLATUPGYM AIは、JINの代わりに勝手に決めるAIではありません。

役割はこの5つです。

1. JINの頭の中を整理する。
2. LINE返信、SNS投稿、動画台本、リスク対応の下書きを作る。
3. FLATUP GYMの理念・口調・安全ルールを守る。
4. 改善した内容をObsidianとGitHubに残す。
5. 次回のAIが前回より迷わず動ける状態を作る。

## 正本の考え方

| レイヤー | 正本 | 役割 |
|---|---|---|
| 記憶・仕様 | Obsidian Vault | AIの脳。理念、ルール、運用、学習ログを管理 |
| 実行 | FLATUP AI OS | コマンドで下書きを生成するエンジン |
| 履歴 | GitHub `flatup1/flatup` | 変更履歴、育成ログ、復元ポイント |
| 本番 | VPS LINE Bot | 会員対応の本番AIKA |

## 絶対ルール

- AIは整理・提案・下書きまで。
- 送信、投稿、予約確定、本番反映、Git pushはJIN承認後。
- 料金、営業時間、休業日、キャンペーン、会員対応は推測で変更しない。
- APIキー、個人情報、認証情報はObsidianにもGitHubにも書かない。
- 古い資料は参考にしてよいが、現行判断は `CLAUDE.md` と `6_システム/` を優先する。

## 今の主要機能

| 領域 | できること |
|---|---|
| LINE/DM | 問い合わせ返信、体験予約案内、追客文 |
| SNS | Instagram/X投稿、Typefully下書き、週間投稿運用 |
| 動画 | リール/TikTok台本、SORA/AI動画プロンプト |
| 経営整理 | 今日やること、再開メモ、タスク分類 |
| リスク | 会員間トラブル、クレーム、個人情報、危険判断の整理 |
| ナレッジ | AIKA人格、FLATUP理念、FAQ、料金、ルール |
| 開発 | LINE Bot仕様、VPS運用、復旧、開発フロー |

## 学習ループ

FLATUPGYM AIは、勝手に本番を変えて賢くなるのではなく、変更履歴を積み上げて賢くなります。

1. 実運用で困ったことを書く。
2. AIが原因と改善案を整理する。
3. JINが承認する。
4. 関連ファイルを更新する。
5. テストや確認をする。
6. GitHubにcommit/pushする。
7. 次回のAIが `FLATUPGYM_AI_HOME.md` と学習ログを読む。

## 次にやる時の合言葉

```text
FLATUPGYM AI HOMEを読んで、前回の続きから始めて。
```

AIはこのファイル、`CLAUDE.md`、`AGENTS.md`、`6_システム/FLATUPGYM_AI_使い方.md` を確認してから作業します。
