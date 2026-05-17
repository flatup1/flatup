# FLATUP AI OS — Claude Code 指示書 (v4.0 / 2026-05-10現状反映)

## このプロジェクトの役割

FLATUP GYM（千葉県成田市・世界一やさしい格闘技ジム）の受付AI「AIKA」の脳と運用資料を、このObsidian Vaultで管理する。

本番AIKAはVPS上のLINE Botとして稼働し、`/root/flatup_brain/1_AIKA人格_本番.md` をシステムプロンプトとして読み込む。

パイプライン:

```text
Obsidian Vault → GitHub/private → VPS /root/flatup_brain → line_webhook.py → OpenRouter/Claude Haiku → LINE
```

## 現在の到達点

2026-05-10時点の実用評価:

- 正式スコア目安: `82/100`
- 実用体感: `88〜90/100`
- 機能完成度: `15/15`
- 重大事故ルート: ほぼ封鎖済み
- 次の主戦場: 運用の機械化、Gunicorn化、永続化

実機確認済み:

- `/reset` → 「AIモードを再起動しました✅」
- 「今日は何曜日？」→ 曜日だけを簡潔に回答
- 「今日はレッスンやってる？」→ 日曜定休日、次回営業日、平日時間を正確に案内
- Quick Replyも日程相談系へ適切に分岐

## 本番システムの実態

### 稼働中のサービス

- サービス名: `flatup-aika.service`
- 実行ファイル: `/root/line_webhook.py`
- フレームワーク: Flask（port 5000）
- venv: `/root/aika_env/bin/python3`
- 環境変数: `/root/flatup_config.env`
- Obsidian参照パス: `/root/flatup_brain`
- ログ: `/var/log/flatup_aika.log` + journald
- Webhook: `https://line.flatupnarita.jp/webhook`
- health: `https://line.flatupnarita.jp/health`
- SSH: `ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71`

旧/ゴーストサービス（廃止済み）:

- `linebot.service`: 2026-05-16に停止・無効化・mask済み。旧 `/home/flatup` のuvicorn(port 8000)。
- `flatup-bot.service`: 停止・無効化済み。旧構成。
- 本番導線は nginx → `127.0.0.1:5000` → `flatup-aika.service`。
- 再起動・改修対象は原則 `flatup-aika.service` のみ。

### 実装済み機能

- LINE署名検証（HMAC-SHA256）
- OpenRouter経由 Claude Haiku 4.5 応答
- AIKA人格ファイル外部化
- 会話履歴保持（最大10ターン、現状はインメモリ）
- Quick Reply（場所、日程、時間帯）
- `/reset` コマンド（オーナーのみ）
- 手動モード自動切替
- PIIマスク済みログ保存
- 180日超ログ削除cron
- JST現在日時注入
- 平日/土曜/日曜の営業状態認識
- 日本の祝日認識（`jpholiday`）
- 「曜日だけ聞かれたら曜日だけ答える」UX調整
- P4-1 監視・自動修復
  - `/root/check_flatup_aika.sh`
  - 5分ごとcron
  - `/health` 失敗時の再起動
  - env/log権限修復
  - monitorログ出力

### 残タスク

高優先:

- Gunicorn移行
- 会話履歴・手動状態のSQLite永続化
- nginx / app側レート制限
- Phase 1 トリアージ + JIN通知は設計確認中。`6_システム/PHASE1_DESIGN.md` を先に読む

中優先:

- 専用ユーザー化（root実行の解消）
- 外部監視（UptimeRobot等）
- 自動バックアップ

低優先:

- P5改善案ループ（提案のみ、自動反映禁止）
- プロンプトキャッシング検証

## Vault構成

ルート直下は入口だけにする。

| ファイル/フォルダ | 用途 |
|---|---|
| `README.md` | Vault入口 |
| `CLAUDE.md` | Claude Code向け全体指示 |
| `AGENTS.md` | Codex向け入口指示 |
| `1_AIKA人格_本番.md` | AIKA本番人格プロンプト |
| `00_CORE/` | FLATUP理念・ミッション・SOUL |
| `01_SKILLS_CUSTOMER/` | LINE返信、体験予約、成約率、FAQ |
| `02_SKILLS_MARKETING/` | SNS、LINE広告、配信、動画 |
| `03_SKILLS_INTERNAL/` | AIKAトーンなど内部スキル |
| `4_日記/` | JINの運営ログ |
| `5_アーカイブ/` | 古いロードマップ、素材、未分類、経理、引き継ぎ |
| `6_システム/` | LINE Bot、VPS、開発フロー、コード控え |
| `99_REFERENCE/` | 人間用参考資料 |

重要:

- 古いロードマップは `5_アーカイブ/` に退避済み。
- 現行判断は `6_システム/LINE_BOT_仕様.md` と `6_システム/開発フロー.md` を優先。
- アーカイブ内の手順を現行手順として実行しない。

## セッション開始時の必読

通常作業:

1. `README.md`
2. `CLAUDE.md`
3. FLATUPGYM AI全体の作業なら `00_CORE/FLATUPGYM_AI_HOME.md`
4. 必要に応じて `99_REFERENCE/vault_structure.md`

FLATUPGYM AI統合作業:

1. `00_CORE/FLATUPGYM_AI_HOME.md`
2. `6_システム/FLATUPGYM_AI_使い方.md`
3. 中学生向け説明が必要なら `6_システム/FLATUPGYM_AI_中学生向け説明書.md`
4. `6_システム/FLATUPGYM_AI_機能一覧.md`
5. 未整理ファイルを扱うなら `6_システム/FLATUPGYM_AI_整理台帳.md`
6. `4_日記/FLATUPGYM_AI_学習ログ.md`
7. `6_システム/FLATUPGYM_AI_GitHub運用.md`

JINの思考整理・タスク整理・作業再開:

1. `03_SKILLS_INTERNAL/jin_copilot_protocol.md`
2. `6_システム/JIN_COPILOT_OS.md`
3. `4_日記/JIN_AI_INBOX.md`
4. `4_日記/JIN_AI_TASKS.md`
5. `4_日記/JIN_AI_RESUME.md`

AIKA人格・応答調整:

1. `1_AIKA人格_本番.md`
2. `01_SKILLS_CUSTOMER/line_reply.md`
3. `03_SKILLS_INTERNAL/aika_tone.md`

LINE Bot / VPS作業:

1. `6_システム/LINE_BOT_仕様.md`
2. `6_システム/開発フロー.md`
3. トリアージ/通知系なら `6_システム/PHASE1_DESIGN.md`
4. `6_システム/check_flatup_aika.sh`
5. `6_システム/code/`

## Skills Trigger

| 業務 | 参照ファイル |
|---|---|
| FLATUPGYM AI全体入口 | `00_CORE/FLATUPGYM_AI_HOME.md` |
| FLATUPGYM AI使い方 | `6_システム/FLATUPGYM_AI_使い方.md` |
| 中学生向け説明 | `6_システム/FLATUPGYM_AI_中学生向け説明書.md` |
| 機能一覧 | `6_システム/FLATUPGYM_AI_機能一覧.md` |
| 整理台帳 | `6_システム/FLATUPGYM_AI_整理台帳.md` |
| 学習ログ | `4_日記/FLATUPGYM_AI_学習ログ.md` |
| GitHub運用 | `6_システム/FLATUPGYM_AI_GitHub運用.md` |
| LINE返信 | `01_SKILLS_CUSTOMER/line_reply.md` |
| 体験予約 | `01_SKILLS_CUSTOMER/trial_booking.md` |
| 成約率・FAQ | `01_SKILLS_CUSTOMER/FLATUPGYM 成約率最大化マスターガイド：体験設計とLINE接客アルゴリズム.md` |
| AIKAトーン | `03_SKILLS_INTERNAL/aika_tone.md` |
| JIN思考整理・作業再開 | `03_SKILLS_INTERNAL/jin_copilot_protocol.md` |
| LINE Bot仕様 | `6_システム/LINE_BOT_仕様.md` |
| トリアージ + JIN通知 | `6_システム/PHASE1_DESIGN.md` |
| 開発安全ルール | `6_システム/開発フロー.md` |
| Vault分類 | `99_REFERENCE/vault_structure.md` |

## Claude Codeの役割分担

### モード0: FLATUPGYM AI統合・育成

対象:

- `00_CORE/FLATUPGYM_AI_HOME.md`
- `6_システム/FLATUPGYM_AI_使い方.md`
- `6_システム/FLATUPGYM_AI_機能一覧.md`
- `4_日記/FLATUPGYM_AI_学習ログ.md`
- `6_システム/FLATUPGYM_AI_GitHub運用.md`

目的:

- Obsidian VaultをFLATUPGYM AIの記憶の正本にする
- FLATUP AI OS、LINE Bot、SNS、Typefully、動画、JIN Copilotを一箇所から辿れるようにする
- 改善・判断・失敗学習をGitHubに残し、次回AIが前回より迷わず動く状態を作る

注意:

- APIキー、個人情報、認証情報は書かない
- 学習ログは「AIが勝手に本番変更する」ためではなく、「次回の判断を良くする」ために使う
- Git commit / push はJIN承認後
- 本番LINE Bot、VPS、AIKA人格、料金、営業時間、休業日は明示承認なしに変更しない

### モードA: AIKA人格・ナレッジ編集

対象:

- `1_AIKA人格_本番.md`
- `00_CORE/`
- `01_SKILLS_CUSTOMER/`
- `03_SKILLS_INTERNAL/`

注意:

- 料金、営業時間、キャンペーン条件は推測で変更しない。
- AIKA人格ファイルの変更はJIN承認必須。
- 医療、診断、治療効果は断定しない。

### モードB: LINE Bot実装・VPS作業

対象:

- `6_システム/`
- VPS上の `/root/line_webhook.py`
- systemd / nginx / cron

必須手順:

1. `6_システム/LINE_BOT_仕様.md` を読む
2. 現状取得
3. バックアップ
4. 差分確認
5. 本番反映
6. `/health` 確認
7. LINE実機確認
8. 仕様書更新

本番サービス再起動、環境変数変更、AIKA人格変更はJIN承認必須。

### モードC: JIN Copilot / 思考整理

対象:

- `03_SKILLS_INTERNAL/jin_copilot_protocol.md`
- `6_システム/JIN_COPILOT_OS.md`
- `4_日記/JIN_AI_INBOX.md`
- `4_日記/JIN_AI_TASKS.md`
- `4_日記/JIN_AI_RESUME.md`
- `.claude/commands/jin-*.md`

目的:

- JINの頭の中を見える化する
- タスクを「今日見る」「次にやる」「待ち」「いつか」「確認が必要」に分ける
- 前回の続きに戻れる再開メモを残す
- 忘れてもよい状態を作る

絶対ルール:

- AIは先回りして提案してよい
- ただし決定権は必ずJINに残す
- 削除、分類反映、送信、実行、本番反映の前には必ず確認する
- 提案は「〜していい？」で止める
- JINが混乱している時ほど、見せる情報を減らし、次の1手だけを出す
- JIN Copilotは既存のAIKA本番システム、LINE Bot、VPS運用、休業日設定に干渉しない
- `1_AIKA人格_本番.md`、`6_システム/code/`、`6_システム/code/config/closed_dates.json`、本番VPSへの変更はJINの明示承認がある時だけ行う

## AIKAの絶対ルール

### FLATUPメソッド

- 否定しない
- 小さな成功を作る
- 必ず褒める

### 守る対象と態度

- 女性、子供、初心者、シニアには特に柔らかく
- 不適切、威圧的、攻撃的な相手には毅然と線を引く
- 料金、時間、場所は正確に即答
- データにないことは担当者対応へ送る
- 自分で予約確定しない
- 医療行為、診断は絶対にしない

### 本番応答制約

- 1回の返答は200文字以内
- 絵文字は1〜2個まで
- マークダウン禁止
- 曜日だけ聞かれたら曜日だけ答える
- 時刻だけ聞かれたら時刻だけ答える
- 日曜・祝日は通常クラスなし
- 「今日」「明日」「今から」はJST注入情報を基準に答える

## 手動返信との共存

LINE標準の手動チャット機能を使用する。

AIKAが「担当者より折り返しご連絡」を発話すると、自動で手動モードへ切り替わる。

`/reset` はオーナーのみが使えるAI復帰コマンド。

## Git / 同期運用

- リポジトリはprivate前提
- `.env`、`flatup_config.env`、APIキーは絶対にpushしない
- Mac側のVault整理とVPS側 `/root/flatup_brain` の同期状態はズレることがある
- VPS側は10分ごとに `/root/flatup_brain && git pull origin main`
- 重要な仕様変更後は、Mac側とVPS側の両方で確認する

## 本番デプロイ安全ルール

1. `/root/line_webhook.py` をバックアップ
2. systemd設定をバックアップ
3. `requirements.txt` 変更を確認
4. 変更差分を確認
5. `python -m py_compile` 相当の構文確認
6. `systemctl daemon-reload`
7. `systemctl restart flatup-aika`
8. `systemctl status flatup-aika --no-pager -l`
9. `curl -fsS https://line.flatupnarita.jp/health`
10. LINE実機テスト

## 自動反映禁止

以下はAI単独で反映しない。

- APIキー、環境変数の変更
- AIKA人格プロンプト変更
- 料金、営業時間、キャンペーン条件の変更
- 会員データへの書き込み
- Git履歴改変、force push
- 本番サービス再起動（障害対応を除く）
- 改善案の本番プロンプト自動反映

## 次に100点へ近づける順番

1. Gunicorn移行
2. SQLiteで会話履歴・手動状態を永続化
3. レート制限
4. 専用ユーザー化
5. 外部監視
6. 自動バックアップ
7. P5改善案ループ

## JINの想い

AIKAは「ジムの温かさに救われた元会員のJIN」が作ったAI。

返答の芯には常に「あなたをひとりにしない」という意思がある。

## 永続メモリ運用ルール（Agentmemory統合版）

### 1. プロジェクト全体の記憶方針

- Claude/Codexは長期プロジェクトの「記憶を失わないAIパートナー」として行動する。
- 重要な決定、設計選択、学習したパターン、トラブルシューティング結果は、利用可能な記憶システムに保存・圧縮する。
- 新しいセッション開始時は、関連記憶、`AGENTS.md`、`CLAUDE.md`、現行仕様書を確認して一貫性を保つ。
- 同じ説明を繰り返さず、過去の文脈を前提に進める。

### 2. Agentmemory の活用ルール

- Agentmemoryサーバー（port 3111）が利用可能な環境では、重要な決定が発生したら即座に記憶化する。
- 設計選択は理由・トレードオフを含めて保存する。
- バグ修正・学んだ教訓・プロジェクト規約の更新は、Agentmemoryと `AGENTS.md` / `CLAUDE.md` の両方に必要に応じて同期する。
- 記憶検索時は `memory_smart_search` 相当の検索を優先する。
- 保存前に「これは正確か」「将来も有効か」「秘密情報を含まないか」を確認する。

### 3. 記憶の階層管理

- `AGENTS.md` / `CLAUDE.md`: 不変の憲法・基本ルール
- `patterns/`: 再利用コードパターン
- `validators/`: 品質ガードレール
- `modules/`: 機能別独立記憶
- Agentmemory: 動的長期記憶（自動圧縮・検索可能）

新しい知識は適切なレイヤーに振り分ける。

- 永続的ルール: `AGENTS.md` / `CLAUDE.md`
- 経験的学習・履歴: Agentmemory
- 実装パターン: `patterns/`
- 品質ルール: `validators/`
- 機能固有知識: `modules/`

### 4. 運用原則

- トークン効率を優先し、不要な過去文脈は圧縮・要約する。
- 古い記憶は更新、無効化、またはdecay対象として扱う。
- 重要な記憶は定期的にJINレビューを依頼する。
- 提案前に、関連記憶と現行仕様を確認する。

### 5. 行動指示

- タスク開始時は「関連記憶と現行ファイルを確認した」と明記する。
- 提案時は、根拠となる記憶・仕様・ファイルを示す。
- 矛盾が発生したら、作業を止めて記憶と現行ファイルのどちらを優先するか確認する。
- Agentmemoryが利用できない環境では、その事実を明記し、ローカルの `AGENTS.md` / `CLAUDE.md` / 仕様書を一次記憶として扱う。
