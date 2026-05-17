# Vault構造リファレンス（人間用）

## フォルダ一覧

| フォルダ | 用途 |
|---|---|
| `00_CORE/` | ジム基本情報・料金・キャンペーン（Claudeが頻繁に参照） |
| `01_SKILLS_CUSTOMER/` | 顧客対応スキル（LINE返信・予約・入会・クチコミ・クレーム） |
| `02_SKILLS_MARKETING/` | SNS・LINE広告・配信・動画など販促資料 |
| `03_SKILLS_INTERNAL/` | 内部スキル（AIKAトーン・JIN思考整理プロトコル） |
| `4_日記/` | JINの運営ログ、未整理メモ、作業再開メモ（本番非公開） |
| `5_アーカイブ/` | 古いロードマップ・引き継ぎ・未分類・素材・経理契約 |
| `6_システム/` | LINE Bot・VPS仕様書・開発フロー・コード控え |
| `99_REFERENCE/` | 人間用参考資料（Claudeに毎回読ませない） |

## 重要ファイル

| ファイル | 用途 |
|---|---|
| `00_CORE/ブランド理念/中核コピー.md` | FLATUPGYMの北極星コピー |
| `00_CORE/FLATUPGYM_AI_HOME.md` | FLATUPGYM AIの入口。Obsidian記憶・AIOS・GitHub運用の統合ホーム |
| `6_システム/FLATUPGYM_AI_使い方.md` | JIN向けの使い方メモ |
| `6_システム/FLATUPGYM_AI_中学生向け説明書.md` | FLATUPGYM AIを簡単な言葉で説明する入門書 |
| `6_システム/FLATUPGYM_AI_機能一覧.md` | 今まで作ったAI機能の一覧 |
| `6_システム/FLATUPGYM_AI_整理台帳.md` | 未整理ファイルを安全に分類するための台帳 |
| `4_日記/FLATUPGYM_AI_学習ログ.md` | 改善・判断・失敗学習を残すログ |
| `6_システム/FLATUPGYM_AI_GitHub運用.md` | GitHubでAIの成長履歴を管理する手順 |
| `99_REFERENCE/ダヴィンチ指示文_経営全体最適化.md` | 経営全体最適化プロンプトの保管場所 |
| `03_SKILLS_INTERNAL/jin_copilot_protocol.md` | JINの思考整理・作業再開AIの振る舞いルール |
| `6_システム/JIN_COPILOT_OS.md` | JIN Copilotの設計と運用 |
| `4_日記/JIN_AI_INBOX.md` | 未整理メモの受け皿 |
| `4_日記/JIN_AI_TASKS.md` | 整理済みタスク |
| `4_日記/JIN_AI_RESUME.md` | 作業再開メモ |
| `6_システム/PHASE1_DESIGN.md` | AIKA Phase 1 トリアージ + JIN通知の設計 |
| `6_システム/PHASE1_NEXT_STEPS.md` | AIKA Phase 1 次回再開手順 |

## ルート直下に残すもの

| ファイル | 理由 |
|---|---|
| `README.md` | Vaultの入口 |
| `CLAUDE.md` | AIエージェント向け全体指示 |
| `AGENTS.md` | Codex向け入口指示 |
| `1_AIKA人格_本番.md` | AIKA本番人格プロンプト |

## ファイル追加ルール
- ルート直下に散らかさない
- ルート直下は `README.md`、`CLAUDE.md`、`AGENTS.md`、`1_AIKA人格_本番.md` を基本にする
- 必ず上記フォルダに分類
- Skillファイルは150行以内
- 現行仕様は `6_システム/`、古い実装計画は `5_アーカイブ/` に分ける
- JINの思考整理AIは `03_SKILLS_INTERNAL/`、`4_日記/`、`6_システム/` に分ける
- `5_アーカイブ/` 内の資料は現行手順として扱わない
