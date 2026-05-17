# FLATUPGYM AI 正本マップ

最終更新: 2026-05-17

このファイルは、FLATUPGYM AIで「どのファイルを本物として見るか」を迷わないための地図です。

## 結論

迷ったら、この順番で見ます。

1. `00_CORE/FLATUPGYM_AI_HOME.md`
2. `CLAUDE.md` / `AGENTS.md`
3. `6_システム/FLATUPGYM_AI_機能一覧.md`
4. `6_システム/FLATUPGYM_AI_整理台帳.md`
5. `4_日記/FLATUPGYM_AI_学習ログ.md`

## 正本レイヤー

| レイヤー | 正本 | 役割 |
|---|---|---|
| 全体入口 | `00_CORE/FLATUPGYM_AI_HOME.md` | AIが最初に読むホーム |
| AIKA人格 | `1_AIKA人格_本番.md` | LINE Botの人格正本 |
| AIKA OS憲法 | `00_CORE/AIKA_OS_CONSTITUTION_v1.md` | JINの分身AIとしての上位ルール |
| ブランド理念 | `00_CORE/ブランド理念/` | FLATUPの理念、SOUL、ミッション |
| 顧客対応 | `01_SKILLS_CUSTOMER/` | LINE返信、体験予約、FAQ、成約率改善 |
| マーケティング | `02_SKILLS_MARKETING/` | SNS、Typefully、広告、配信、動画 |
| JIN Copilot | `03_SKILLS_INTERNAL/jin_copilot_protocol.md` | JINの思考整理・再開支援ルール |
| JIN作業台 | `4_日記/JIN_AI_*.md` | 未整理メモ、タスク、再開メモ |
| システム運用 | `6_システム/` | LINE Bot、AIOS、開発、復旧、整理台帳 |
| 参考資料 | `99_REFERENCE/` | 判断材料。現行ルールより優先しない |
| アーカイブ | `5_アーカイブ/` | 過去資料。現行手順としては使わない |

## GitHubに載せるもの

| 載せる | 理由 |
|---|---|
| 正本ドキュメント | 次回AIが同じ判断を引き継げる |
| 使い方、整理台帳、学習ログ | JINとAIの共通記憶になる |
| 秘密情報を含まないテンプレート | 再利用できる |
| `.claude/commands/*.md` | JIN用コマンドの入口として使える |

## GitHubに載せないもの

| 載せない | 理由 |
|---|---|
| `.env` / APIキー / 認証情報 | 漏洩リスク |
| `.claude/settings.json` / `.claude/settings.local.json` | ローカル権限設定で、環境依存 |
| `.obsidian/` | 端末ごとの表示設定 |
| `.DS_Store` | macOSの自動生成ファイル |
| `*.local.json` | ローカル専用設定 |
| 生データ、画像、動画、PDF | 重く、秘密情報を含む可能性がある |
| 参考リポジトリ内の `.git/` | Vault本体のGit管理と混ざる |

## 未整理ファイルを見つけた時

すぐ削除しません。

1. `6_システム/FLATUPGYM_AI_整理台帳.md` に分類する。
2. 正本に昇格するか、参考に残すか、アーカイブするかを決める。
3. 秘密情報チェックをする。
4. JIN承認が必要なものは確認する。
5. 今回触るファイルだけcommitする。

## 中学生向けに言うと

- `00_CORE/` は、AIの心臓とルールブック。
- `01_SKILLS_CUSTOMER/` は、お客さん対応の教科書。
- `02_SKILLS_MARKETING/` は、集客と発信の道具箱。
- `03_SKILLS_INTERNAL/` は、JINを助ける秘書AIの説明書。
- `4_日記/` は、今日のメモと再開ノート。
- `6_システム/` は、機械を動かす設計図。
- `99_REFERENCE/` は、昔の資料や参考書。
- `5_アーカイブ/` は、捨てないけど普段は見ない倉庫。

## 今回の最適化で正式採用したもの

- `00_CORE/AIKA_OS_CONSTITUTION_v1.md`
- `00_CORE/README.md`
- `00_CORE/board.md`
- `00_CORE/done.md`
- `00_CORE/inbox.md`
- `00_CORE/ブランド理念/FLATUP_mission.md`
- `00_CORE/ブランド理念/SOUL.md`
- `00_CORE/ブランド理念/中核コピー.md`
- `01_SKILLS_CUSTOMER/README.md`
- `02_SKILLS_MARKETING/README.md`
- `03_SKILLS_INTERNAL/jin_copilot_protocol.md`
- `4_日記/JIN_AI_INBOX.md`
- `4_日記/JIN_AI_TASKS.md`
- `4_日記/JIN_AI_RESUME.md`
- `.claude/commands/jin-capture.md`
- `.claude/commands/jin-organize.md`
- `.claude/commands/jin-resume.md`
