# システム

LINE Bot、VPS、本番運用、開発フローに関する現行ドキュメントを置く。

## 現行ドキュメント

| ファイル | 役割 |
|---|---|
| `FLATUPGYM_AI_使い方.md` | FLATUPGYM AIのわかりやすい使い方 |
| `FLATUPGYM_AI_中学生向け説明書.md` | FLATUPGYM AIを中学生にもわかる言葉で説明した入門書 |
| `FLATUPGYM_AI_機能一覧.md` | 今まで作った機能の一覧 |
| `FLATUPGYM_AI_GitHub運用.md` | ObsidianとGitHubでAIを育てる運用手順 |
| `FLATUPGYM_AI_整理台帳.md` | 未整理ファイルを安全に分類するための台帳 |
| `FLATUPGYM_AI_正本マップ.md` | どのファイルを正本として見るかの地図 |
| `LINE_BOT_仕様.md` | FLATUP GYM LINE Botの現行仕様と100点化ロードマップ |
| `AIKA_LINE_Bot本体コマンド早見表.md` | LINEで使う本体コマンド一覧 |
| `AIKA_OS_中学生向け使い方.md` | AIKA OS全体をやさしく説明した使い方 |
| `JIN_COPILOT_OS.md` | JINの思考整理・作業再開AI設計 |
| `PHASE1_DESIGN.md` | トリアージ + JIN通知の設計文書 |
| `PHASE1_NEXT_STEPS.md` | Phase 1 次回再開用の実行手順 |
| `開発フロー.md` | 実装、レビュー、本番反映の安全ルール |
| `check_flatup_aika.sh` | VPS監視スクリプトのローカル控え |
| `code/` | LINE Bot本体に近いコード控え |
| `flatup-research-ai/` | 競合調査・広告案・LINE文・リール台本生成MVP |
| `JIN専用：Master Brain & LINE AI 運用マニュアル.md` | AI OS運用マニュアル |
| `⭐️FLATUP_AI_OS_修復マニュアル.md` | 復旧時の参照マニュアル |
| `CLOSED_MODE_DESIGN.md` | 休業日・オーナー限定モードの設計 |
| `FLATUPGYM_AI_本番コード差分レビュー.md` | 本番コード差分を安全に保留するためのレビュー |
| `openqlow_drafts/` | OPENQLOW / HelMESで生成したSNS下書き控え |
| `openqlow_logs/` | OPENQLOW / HelMESの生成・承認ログ |

## 参照優先順位

1. FLATUPGYM AI全体なら `00_CORE/FLATUPGYM_AI_HOME.md`
2. 使い方確認なら `FLATUPGYM_AI_使い方.md`
3. かんたんな説明なら `FLATUPGYM_AI_中学生向け説明書.md`
4. 機能棚卸しなら `FLATUPGYM_AI_機能一覧.md`
5. 未整理ファイルを扱うなら `FLATUPGYM_AI_整理台帳.md`
6. LINE Bot本番仕様なら `LINE_BOT_仕様.md`
7. 開発・本番反映なら `開発フロー.md`
8. AIKA人格なら `1_AIKA人格_本番.md`
9. JINの思考整理・作業再開なら `JIN_COPILOT_OS.md` と `03_SKILLS_INTERNAL/jin_copilot_protocol.md`
10. `5_アーカイブ/` 内の資料

アーカイブ資料は過去ログ扱い。現行判断には使わない。

## 本番コードの扱い

以下は、設計資料と分けて扱います。

- `6_システム/code/line_webhook.py`
- `6_システム/code/lib/closed_mode.py`
- `6_システム/code/config/closed_dates.json`

これらは本番影響があるため、JIN承認、テスト、バックアップ、ロールバック手順が揃うまで反映しません。

## OPENQLOW下書きの扱い

`openqlow_drafts/` と `openqlow_logs/` は、SNS下書きと承認ログの控えです。

- 公開済み扱いにしない。
- 投稿・予約・Typefully保存はJIN承認後のみ。
- `approval_id` と `publication_level` を残す。
- 個人情報やAPIキーは保存しない。
