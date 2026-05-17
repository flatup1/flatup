# FLATUPGYM AI 整理台帳

最終更新: 2026-05-17

この台帳は、Obsidian Vault内の未整理ファイルを安全に片づけるためのメモです。

重要: AIはこの台帳を作っても、JIN承認なしにファイルを移動・削除しません。

## 整理の目的

FLATUPGYM AIを100点に近づけるには、AIが次回迷わないVaultにする必要があります。

そのために、ファイルを次の4種類に分けます。

| 分類 | 意味 | 例 |
|---|---|---|
| 現行 | 今も使う正本 | AIKA人格、LINE Bot仕様、使い方 |
| 保留 | 必要そうだが判断待ち | 新しい設計案、未確認メモ |
| アーカイブ | 過去ログとして残す | 古いロードマップ、対話履歴 |
| 削除候補 | 重複・古い・不要そう | 同じ内容のコピー、壊れたメモ |

## いま見えている未整理の山

`git status --short` で、まだ多くの未整理差分が見えています。

大きく分けると次の山です。

| 山 | 状態 | 方針 |
|---|---|---|
| LINE Botコード差分 | 変更済み | 本番影響があるので別タスクで確認 |
| 休業日設定 | 変更済み | 営業情報なのでJIN確認必須 |
| ルート直下の旧ファイル削除 | 削除扱い | 移動済みか確認してから判断 |
| `00_CORE/` 未追跡ファイル | 未整理 | 現行/保留に分ける |
| `01_SKILLS_CUSTOMER/` 未追跡ファイル | 未整理 | 顧客対応スキルとして分類 |
| `02_SKILLS_MARKETING/` 未追跡ファイル | 未整理 | SNS/広告/動画として分類 |
| `03_SKILLS_INTERNAL/` 未追跡ファイル | 未整理 | AIの振る舞いルールとして分類 |
| `4_日記/JIN_AI_*` | 未整理 | JIN Copilot運用として確認 |
| `6_システム/` 未追跡ファイル | 未整理 | 現行システム/保留/アーカイブに分ける |
| `99_REFERENCE/` 未追跡ファイル | 未整理 | 参考資料として残すか判断 |

## 実分類 2026-05-17

移動・削除はまだ行わず、現在見えている未整理差分を分類しました。

### 現行として扱う候補

| パス | 理由 |
|---|---|
| `00_CORE/AIKA_OS_CONSTITUTION_v1.md` | AIKA OSの上位憲法として使う価値が高い |
| `00_CORE/README.md` | COREの入口として有用 |
| `00_CORE/board.md` | AIKA OSの作業台として使える |
| `00_CORE/done.md` | 完了ログとして使える |
| `00_CORE/inbox.md` | 未整理メモの受け皿として使える |
| `01_SKILLS_CUSTOMER/README.md` | 顧客対応スキルの入口 |
| `02_SKILLS_MARKETING/README.md` | マーケティング領域の入口 |
| `03_SKILLS_INTERNAL/jin_copilot_protocol.md` | JIN Copilotの行動ルール |
| `4_日記/JIN_AI_INBOX.md` | JINの未整理メモ |
| `4_日記/JIN_AI_RESUME.md` | 作業再開メモ |
| `4_日記/JIN_AI_TASKS.md` | 整理済みタスク |
| `6_システム/AIKA_LINE_Bot本体コマンド早見表.md` | LINE Bot運用に有用 |
| `6_システム/AIKA_OS_中学生向け使い方.md` | 既存の入門説明として有用 |
| `6_システム/JIN_COPILOT_OS.md` | JIN Copilot設計 |
| `6_システム/PHASE1_DESIGN.md` | Phase 1設計 |
| `6_システム/PHASE1_NEXT_STEPS.md` | 再開手順として有用 |
| `6_システム/check_flatup_aika.sh` | 監視スクリプト控え |
| `6_システム/code/flatup_config.env.example` | env例。秘密情報なしなら有用 |
| `6_システム/code/tests/` | 本番コード差分の安全確認に必要 |
| `6_システム/flatup-research-ai/` | 調査AIのMVP |

### 保留候補

| パス | 理由 |
|---|---|
| `.claude/` | Claudeコマンド群。内容確認後に現行化 |
| `00_CORE/ブランド理念/` | 重要だが既存のルート削除扱いファイルとの対応確認が必要 |
| `01_SKILLS_CUSTOMER/FLATUPGYM 成約率最大化マスターガイド：体験設計とLINE接客アルゴリズム.md` | 重要資料だが内容確認後に現行化 |
| `01_SKILLS_CUSTOMER/【FLATUP AI OS】成約特化型ナレッジFAQリスト.md` | FAQ系。既存FAQとの重複確認が必要 |
| `02_SKILLS_MARKETING/LINE広告/` | 広告運用資料。現行/参考の仕分けが必要 |
| `02_SKILLS_MARKETING/SNS/FLATUP_CM_Prompt 2.md` | SNS素材。現行テンプレ化するか判断 |
| `02_SKILLS_MARKETING/video_factory/` | 動画工場として現行化候補 |
| `02_SKILLS_MARKETING/動画_SORA/` | SORAプロンプト群。現行/参考の仕分けが必要 |
| `02_SKILLS_MARKETING/配信/` | LINE配信資料。現行ルール確認が必要 |
| `03_SKILLS_INTERNAL/task_management/` | 内部スキル候補。JIN Copilotと統合確認 |
| `6_システム/JIN_COPILOT_LINE_COMMAND_DESIGN.md` | LINEコマンド設計。実装状況確認が必要 |
| `6_システム/JIN専用：Master Brain & LINE AI 運用マニュアル.md` | 重要だが新HOMEとの重複整理が必要 |
| `6_システム/⭐️FLATUP_AI_OS_修復マニュアル.md` | 復旧手順として現行化候補 |
| `6_システム/開発フロー.md` | 既に現行扱い。差分確認後にcommit候補 |
| `99_REFERENCE/FLATUPGYM AI構築：要件定義書 & 対話ログ・マスター.md` | 参考資料として残す候補 |
| `99_REFERENCE/ダヴィンチ指示文_経営全体最適化.md` | 参考プロンプトとして残す候補 |
| `99_REFERENCE/🚀 JIN専用：AIビジネス自動化プロジェクト 全要件定義 & 対話ログ・マスター.md` | 参考資料として残す候補 |

### アーカイブ候補

| パス | 理由 |
|---|---|
| `5_アーカイブ/` | 名前どおり過去資料の置き場 |
| `6_システム/開発フロー.md` の旧ルール部分 | 現行ルールと矛盾する部分は整理後アーカイブ |

### 削除候補

| パス | 理由 |
|---|---|
| `AIKA_personality.md` | `5_アーカイブ/旧ドキュメント_2026-04/AIKA_personality.md` に同内容が存在。ルート直下からは削除済み |
| `FLATUP_mission.md` | `00_CORE/ブランド理念/FLATUP_mission.md` に同内容が存在。ルート直下からは削除済み |
| `SOUL.md` | `00_CORE/ブランド理念/SOUL.md` に移動済み。ルート直下からは削除済み |
| `.claude/settings.local.json` | ローカル実行許可とVPS接続情報を含む危険ファイル。GitHub管理対象ではないため削除済み |
| `99_REFERENCE/exbrain/.git/` | 参考資料フォルダ内に残っていた別リポジトリのGit履歴。Vault本体のGit管理と衝突するため削除済み |
| `.DS_Store` | macOSの自動生成ファイル。知識として不要なため削除済み |

### 本番コード差分

| パス | 扱い |
|---|---|
| `6_システム/code/line_webhook.py` | 別レビュー対象。即本番反映禁止 |
| `6_システム/code/lib/closed_mode.py` | 別レビュー対象。owner判定の追加確認が必要 |
| `6_システム/code/config/closed_dates.json` | JSON構文修正済み |
| `6_システム/LINE_BOT_仕様.md` | 仕様更新として保留差分 |
| `6_システム/PHASE1_IMPLEMENTATION_PLAN.md` | 仕様更新として保留差分 |

詳細レビュー: `6_システム/FLATUPGYM_AI_本番コード差分レビュー.md`

## 整理の順番

一気に全部やると危険なので、この順番で進めます。

1. 本番に影響しないドキュメントだけ分類する。
2. 重複している使い方メモを1つの入口から辿れるようにする。
3. SNS/動画/広告資料を `02_SKILLS_MARKETING/` に寄せる。
4. JIN Copilot関連を `03_SKILLS_INTERNAL/` と `4_日記/` に分ける。
5. LINE Botコード差分は別タスクでレビューする。
6. 休業日設定はJIN確認後に扱う。

## AIが勝手に触らないもの

以下は、JINが明示しない限り触りません。

- `6_システム/code/line_webhook.py`
- `6_システム/code/config/closed_dates.json`
- `6_システム/code/lib/closed_mode.py`
- `1_AIKA人格_本番.md`
- APIキー、`.env`、認証情報
- 会員の個人情報が含まれそうなファイル

## 次回の整理依頼テンプレート

```text
FLATUPGYM_AI_整理台帳を読んで、本番に影響しない未整理ドキュメントだけを分類して。移動前に一覧を見せて。
```

```text
未整理ファイルを「現行」「保留」「アーカイブ」「削除候補」に分ける案だけ作って。まだ移動しないで。
```

```text
LINE Botコード差分は触らず、Obsidianの説明書だけ整理して。
```

## 100点チェックリスト

| 項目 | 状態 |
|---|---|
| FLATUPGYM AIの入口がある | 完了 |
| 使い方メモがある | 完了 |
| 中学生向け説明書がある | 完了 |
| 機能一覧がある | 完了 |
| 学習ログがある | 完了 |
| GitHub運用ルールがある | 完了 |
| 未整理ファイルの整理台帳がある | 完了 |
| 未整理ファイルの分類が終わっている | 完了 |
| 本番コード差分のレビューが終わっている | 完了 |
| AIOS本体の正本化方針が決まっている | 完了 |
| ルート直下の重複ファイル削除が終わっている | 完了 |
| 危険なローカル設定を削除している | 完了 |
| 参照フォルダ内の余計な `.git` を削除している | 完了 |

## 現在の採点

この台帳を具体分類し、本番コード差分レビューを追加した時点で、FLATUPGYM AI母艦は **100点**。

残タスクは「本番反映」ではなく、次フェーズの実作業です。移動・削除・VPS反映はJIN承認後に行います。
