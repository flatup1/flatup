# FLATUPGYM AI 機能一覧

最終更新: 2026-05-17

今まで作ったFLATUPGYM AI関連機能を、ここでまとめて管理します。

## 1. AIKA本番LINE Bot

| 項目 | 内容 |
|---|---|
| 目的 | LINEで体験希望者・会員に安全に返信する |
| 本番 | `flatup-aika.service` |
| 仕様 | `6_システム/LINE_BOT_仕様.md` |
| 人格 | `1_AIKA人格_本番.md` |
| 重要ルール | 予約確定しない、料金・時間は正確に、医療判断しない |

主な機能:

- LINE署名検証
- OpenRouter経由 Claude Haiku 4.5
- AIKA人格ファイル読み込み
- 会話履歴保持
- Quick Reply
- `/reset`
- 手動モード
- PIIマスクログ
- JST日時注入
- 営業日/祝日認識
- `/health` 監視

## 2. FLATUP AI OS 実行エンジン

場所:

```text
/Users/jin/Desktop/OPENQLOW HelMES/flatup-ai-os
```

主なコマンド:

| route | 用途 |
|---|---|
| `line_reply` | LINE/DM返信下書き |
| `sns_post` | Instagram/X投稿セット |
| `followup` | 体験後フォロー |
| `review_request` | Google口コミ依頼 |
| `daily_manager` | 今日やること整理 |
| `risk_check` | リスク事案整理 |
| `training_manual` | スタッフ指導マニュアル |
| `video_script` | 動画台本 |
| `differentiation` | HP/LP差別化文 |
| `uizin` | 初心者向け案内 |

関連ファイル:

- `6_システム/FLATUP_AI_OS_オーナー用コマンド早見表.md`
- `6_システム/FLATUPGYM_AI_使い方.md`

## 3. X / Typefully運用

| 項目 | 内容 |
|---|---|
| 目的 | AIがX投稿案を作り、Typefullyに下書き保存する |
| アカウント | `flatupgym` |
| social set ID | `307036` |
| 設定 | `/Users/jin/.config/typefully/config.json` |
| メモ | `02_SKILLS_MARKETING/SNS/Typefully_X運用メモ_FLATUP.md` |

ルール:

- 公開は人間承認後のみ。
- 1日5投稿まで。
- オリジナル比率70%以上。
- 自動リプライ、自動いいね、自動フォローは禁止。
- APIキーはObsidian/GitHubに書かない。

## 4. SNS / ブランド戦略

保存先:

```text
02_SKILLS_MARKETING/SNS/
```

主な資産:

- FLATUP GYM ブランド構築・SNS戦略 対話履歴
- Typefully X運用メモ
- FLATUP CM Prompt

核となるテーマ:

- 弱い自分と戦う人へ
- 世界一初心者に優しい格闘技ジム
- 女性・子供・未経験者が安心して通える
- 格闘技は人生を変える
- 成田 FLATUP GYMのリアルな日常

## 5. 動画 / AI動画生成

保存先:

```text
02_SKILLS_MARKETING/video_factory/
02_SKILLS_MARKETING/動画_SORA/
```

できること:

- TikTok/Reels台本
- SORA/AI動画プロンプト
- FLATUPの世界観に合う動画企画
- 撮影/編集に渡せる構成案

正本資料:

- `02_SKILLS_MARKETING/video_factory/VIDEO_FACTORY_HOME.md`
- `02_SKILLS_MARKETING/video_factory/STYLE_GUIDE.md`
- `02_SKILLS_MARKETING/video_factory/templates/`
- `02_SKILLS_MARKETING/動画_SORA/FLATUP_Security_SORA_Prompts 4.md`

## 6. 顧客対応スキル

保存先:

```text
01_SKILLS_CUSTOMER/
```

主な機能:

- LINE返信
- 体験予約案内
- 成約率最大化
- FAQ
- 初心者・女性・キッズ向け案内

正本資料:

- `01_SKILLS_CUSTOMER/line_reply.md`
- `01_SKILLS_CUSTOMER/trial_booking.md`
- `01_SKILLS_CUSTOMER/【FLATUP AI OS】成約特化型ナレッジFAQリスト.md`
- `01_SKILLS_CUSTOMER/FLATUPGYM 成約率最大化マスターガイド：体験設計とLINE接客アルゴリズム.md`

絶対ルール:

- 予約確定は人間。
- 料金やルールは推測しない。
- 個人情報をむやみに保存しない。

## 7. JIN Copilot / 思考整理

保存先:

```text
03_SKILLS_INTERNAL/jin_copilot_protocol.md
6_システム/JIN_COPILOT_OS.md
4_日記/JIN_AI_INBOX.md
4_日記/JIN_AI_TASKS.md
4_日記/JIN_AI_RESUME.md
```

役割:

- JINの頭の中を整理する。
- 今日やることを絞る。
- 前回の続きへ戻れるようにする。
- タスクを見える化する。
- ただし勝手に決めない。

## 8. 開発・本番運用

保存先:

```text
6_システム/
```

主な資料:

- `LINE_BOT_仕様.md`
- `開発フロー.md`
- `⭐️FLATUP_AI_OS_修復マニュアル.md`
- `AIKA_LINE_Bot本体コマンド早見表.md`
- `check_flatup_aika.sh`
- `code/`

安全ルール:

- 本番反映はJIN承認後。
- 本番サービス再起動は承認後。
- APIキー変更は承認後。
- AIKA人格変更は承認後。

## 9. 調査AI / 研究系

保存先:

```text
6_システム/flatup-research-ai/
```

役割:

- 競合調査
- 広告案
- LINE文
- Instagramリール台本
- 調査と下書き専用

禁止:

- 無断ログイン
- CAPTCHA回避
- 内部API解析
- LINE送信
- 予約確定
- 請求変更

正本資料:

- `6_システム/flatup-research-ai/README.md`
- `6_システム/flatup-research-ai/AGENTS.md`
- `6_システム/flatup-research-ai/CLAUDE.md`
- `6_システム/flatup-research-ai/prompts/`
- `6_システム/flatup-research-ai/src/`
- `6_システム/flatup-research-ai/tests/`

安全ルール:

- 公開情報だけを使う。
- ログイン、CAPTCHA回避、内部API解析はしない。
- 出力は下書きであり、LINE送信・予約確定・請求変更はしない。

## 10. システム設計・復旧資料

保存先:

```text
6_システム/
```

主な資料:

- `AIKA_LINE_Bot本体コマンド早見表.md`
- `AIKA_OS_中学生向け使い方.md`
- `JIN_COPILOT_OS.md`
- `JIN_COPILOT_LINE_COMMAND_DESIGN.md`
- `PHASE1_DESIGN.md`
- `PHASE1_NEXT_STEPS.md`
- `CLOSED_MODE_DESIGN.md`
- `開発フロー.md`
- `⭐️FLATUP_AI_OS_修復マニュアル.md`
- `JIN専用：Master Brain & LINE AI 運用マニュアル.md`

扱い:

- 本番反映前の設計・復旧・再開資料として使う。
- `6_システム/code/line_webhook.py` など本番コード差分は別レビューで扱う。

## 11. 学習ログ

保存先:

```text
4_日記/FLATUPGYM_AI_学習ログ.md
```

使い方:

- うまくいった改善を書く。
- 失敗や詰まりを書いて、次回の判断を楽にする。
- 重要な学びは `CLAUDE.md` / `AGENTS.md` / 各仕様書に昇格する。

## 12. GitHub育成ループ

保存先:

```text
6_システム/FLATUPGYM_AI_GitHub運用.md
```

役割:

- Obsidianで作った記憶をGitHubに残す。
- 変更履歴を次回AIが読めるようにする。
- 既存の未コミット差分と今回の変更を混ぜない。
- APIキーや個人情報をcommit前に止める。

標準手順:

1. `git status --short` で現状を見る。
2. 今回触るファイルだけ決める。
3. 秘密情報チェックをする。
4. `git diff --cached --name-only` でstage内容を確認する。
5. commitする。
6. JINが求めた時だけpushする。

## 13. 中学生向け説明書

保存先:

```text
6_システム/FLATUPGYM_AI_中学生向け説明書.md
```

役割:

- FLATUPGYM AIの全体像をかんたんな言葉で説明する。
- Obsidian、AIOS、GitHubの役割を「脳・手足・タイムマシン」として理解できるようにする。
- AIが勝手に決めず、JINが最後に決めることを明確にする。

## 14. 整理台帳

保存先:

```text
6_システム/FLATUPGYM_AI_整理台帳.md
```

役割:

- 未整理ファイルを安全に分類する。
- すぐ移動せず、現行・保留・アーカイブ・削除候補に分ける。
- 本番コードや休業日設定を勝手に触らないためのガードにする。

## 15. 正本マップ

保存先:

```text
6_システム/FLATUPGYM_AI_正本マップ.md
```

役割:

- どのファイルを正本として見るかを決める。
- GitHubに載せるもの、載せないものを分ける。
- 未整理ファイルを見つけた時の判断順を固定する。

## 16. JIN用Claudeコマンド

保存先:

```text
.claude/commands/
```

主なコマンド:

| コマンド | 用途 |
|---|---|
| `jin-capture` | JINの雑なメモを預かる |
| `jin-organize` | 未整理メモをタスクに分類する |
| `jin-resume` | 前回の続きへ戻る |

ルール:

- コマンド本体はGitHub管理してよい。
- `.claude/settings.json` と `.claude/settings.local.json` はローカル権限設定なのでGitHubに載せない。

## 17. OPENQLOW / HelMES SNS下書き控え

保存先:

```text
6_システム/openqlow_drafts/
6_システム/openqlow_logs/
```

役割:

- OPENQLOW / HelMESで生成したSNS下書きをVaultに残す。
- X、Instagram、Threadsの媒体別下書きを保存する。
- 承認ID、生成日時、安全チェックを後から確認できるようにする。

禁止:

- この控えだけで公開済み扱いにしない。
- Typefully保存、予約投稿、SNS公開を自動実行しない。
- 個人情報やAPIキーを保存しない。
