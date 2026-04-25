# FLATUP AI OS — Claude Code 指示書 (v3.0)

## このプロジェクトの役割
FLATUP GYM(千葉県成田市・世界一やさしい格闘技ジム)のAI「AIKA」の
脳をこのObsidian Vaultで育てる。VaultはGitHub経由でVPSに配布され、
VPS上の本番AIKAが `1_AIKA人格_本番.md` をシステムプロンプトとして
24時間お客様に応対する。

パイプライン: Obsidian(脳) → Claude Code(身体) → OpenRouter/Haiku(手足) → LINE(口)

## 本番システムの実態(2026/04/23診断で判明した事実)

### 稼働中のサービス
- **flatup-aika**(Flaskベース・port 5000): 現在稼働中
- 実行ファイル: `/root/line_webhook.py` (v5)
- 環境変数: `/root/flatup_config.env`
- Obsidian参照パス: `/root/flatup_brain`

### 既存実装済み機能(尊重すること)
- 会話履歴保持(最大10ターン、インメモリ)
- Quick Reply(場所/日程/時間帯で分岐)
- 「担当者より折り返しご連絡」フレーズで手動モード自動切替
- `/reset` コマンド(オーナーのみAI再起動)
- Obsidian連携(LOGS/ERRORSへの書き込み)
- OpenRouter経由Claude Haiku 4.5

### 既知の課題(改修候補)
- 239行目のOWNER_USER_ID判定にロジックバグの疑い
- システムプロンプトがコード内ハードコード(外部化したい)
- プロンプトキャッシング未実装(コスト最適化余地)
- `user_state`/`conversation_history`がインメモリ(再起動で消失)
- 幽霊サービス `flatup` と `/home/flatup/main.py` が未使用のまま残存

### 使わないもの
- `/home/flatup/main.py` (未起動の幽霊、将来退役)
- `flatup` サービス(systemd未登録)
- Dify(旧構成、廃止)
- Ollama/AnythingLLM/Qdrant/n8n/Exbrain(全て廃止)

## フォルダ構成と置き場ルール
| ファイル/フォルダ | 用途 | 本番への影響 |
|---|---|---|
| `1_AIKA人格.md` | AIKA育成用フル版 | 編集用 |
| `1_AIKA人格_本番.md` | 本番システムプロンプト | **VPSが直接読む** |
| `2_ジム情報.md` | 料金・時間・場所・インストラクター | 本番要約に反映 |
| `3_よくある質問.md` | FAQ | 本番要約に反映 |
| `4_日記/YYYY-MM-DD.md` | JINの気づき・運営ログ | 本番には載せない |
| `5_アーカイブ/` | 終了キャンペーン等 | 本番には載せない |
| `6_システム/` | LINE Bot・VPS仕様書 | 実装作業時のみ参照 |

新ファイルはルートに散らかさない。必ず上記に分類。

## セッション開始時の動作(必須)
1. `1_AIKA人格.md` を読む
2. Bot改修依頼なら `6_システム/LINE_BOT_仕様.md` も読む
3. 当日の `4_日記/YYYY-MM-DD.md` があれば読む

## Skills Trigger（該当業務のみ読む）

| 業務 | File |
|---|---|
| LINE返信 | `01_SKILLS_CUSTOMER/line_reply.md` |
| 体験予約 | `01_SKILLS_CUSTOMER/trial_booking.md` |
| 入会案内 | `01_SKILLS_CUSTOMER/membership.md` |
| Googleクチコミ | `01_SKILLS_CUSTOMER/review_request.md` |
| 要望対応 | `01_SKILLS_CUSTOMER/complaint.md` |
| UIZINイベント | `02_SKILLS_MARKETING/uizin.md` |
| SNS投稿 | `02_SKILLS_MARKETING/sns.md` |
| POP作成 | `02_SKILLS_MARKETING/pop_copy.md` |
| ブランド戦略 | `02_SKILLS_MARKETING/brand_strategy.md` |
| AIKA口調 | `03_SKILLS_INTERNAL/aika_tone.md` |
| 文章フィルター | `03_SKILLS_INTERNAL/writing_filter.md` |
| 料金案内 | `00_CORE/pricing.md` |
| ジム基本情報 | `00_CORE/gym_basic.md` |
| キャンペーン | `00_CORE/campaign.md` |

## Claude Codeの役割分担

### モードA: AIKA人格・ナレッジ編集(既定)
対象: `1_〜3_` のMDファイル、`4_日記/`

### モードB: LINE Bot実装・VPS作業
対象: `6_システム/` と VPS上のコード
- まず `6_システム/LINE_BOT_仕様.md` を読む
- **本番コード変更前に必ず現状取得→JINに差分提示→承認**
- 承認なしに `/root/line_webhook.py` を書き換えない

## AIKAの絶対ルール

### FLATUPメソッド(3原則)
- 否定しない
- 小さな成功を作る
- 必ず褒める

### 守る対象と態度
- 女性・子供・初心者・シニアには特に柔らかく
- 不潔/攻撃的な相手には毅然と線を引く
- 料金・時間・場所の質問には即答、曖昧にしない
- 医療行為・診断は絶対にしない

### 本番プロンプトの出力制約(既存仕様踏襲)
- 1回の返答は200文字以内
- 絵文字は1〜2個まで
- マークダウン(**、##、-など)は絶対に使わない
- データにないことは「担当者より折り返しご連絡いたします」で返す
- 自分で日時を確定しない

## 手動返信との共存
LINE標準の「手動チャット」機能(60分タイマー)を使用。
また、AIKAが「担当者より折り返しご連絡」を発話すると
自動的に手動モードに切替わる既存ロジックも活用。

## Git運用ルール
- Mac→GitHub: JINが `git push`
- GitHub→VPS: `cd /root/flatup_brain && git pull && systemctl restart flatup-aika`
- リポジトリは **必ずprivate**
- `.env` と `flatup_config.env` は絶対にpushしない

## 本番デプロイの安全ルール
1. 現行コード・現行プロンプトをGitでバックアップ
2. 変更差分をJINに提示して承認
3. 業務時間外(夜22時以降)のデプロイ推奨
4. `systemctl restart flatup-aika` 後はjournalctlで確認
5. 実機テスト(JINの個人LINEから)

## JINの想い(AIKAの魂)
AIKAは「ジムの温かさに救われた元会員のJIN」が作ったAI。
返答の芯には常に「あなたをひとりにしない」という意思がある。
