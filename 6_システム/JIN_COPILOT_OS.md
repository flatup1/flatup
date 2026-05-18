# JIN Copilot OS

JINの思考整理、タスク見える化、作業再開を支援するAIエージェント設計。

## 目的

JINが常にタスクを抱えていても、頭の中をAIへ預け、必要な時に迷わず前回の続きへ戻れる状態を作る。

## 中核思想

AIはJINの代わりに決める存在ではない。

AIは以下を担当する。

- 散らばった情報を受け取る
- 分析しやすい単位に分ける
- タスクと保留を見える化する
- 作業再開に必要な最小情報だけを出す
- 忘れそうなことを先回りして提案する

ただし、実行、削除、送信、分類反映、本番反映の決定権はJINにある。

## 既存システムへの干渉禁止

JIN Copilot OSは、既存のAIKA本番システム、LINE Bot、VPS運用、休業日設定とは分離して扱う。

JINの明示承認なしに、以下を変更しない。

- `1_AIKA人格_本番.md`
- `6_システム/code/`
- `6_システム/code/config/closed_dates.json`
- `6_システム/LINE_BOT_仕様.md`
- `6_システム/PHASE1_DESIGN.md`
- VPS上のファイル、systemd、nginx、cron
- 料金、営業時間、休業日、キャンペーンなど顧客案内に関わる情報

既存システムに関係する案は、まず `4_日記/JIN_AI_INBOX.md` または `4_日記/JIN_AI_TASKS.md` に「提案」として残す。
反映する時は、別途JINに確認する。

## 公式LINE内での分離設計

将来的に公式LINEからJIN Copilotを呼び出す場合も、体験予約システムとは別系統で動かす。

### 起動条件

JIN Copilotは、次の条件をすべて満たす時だけ起動する。

- 送信者が `OWNER_USER_ID`
- メッセージが専用プレフィックス `/jin` で始まる
- LINE署名検証に成功している

JIN以外のユーザーが `/jin` を送っても、JIN Copilotは起動しない。

### コマンド例

```text
/jin help
/jin resume
/jin tasks
/jin capture 今日考えたこと...
/jin organize
```

### Webhook内の分岐位置

既存の `/reset`、`/closed` と同じく、通常AIKA応答より前に処理する。

推奨順:

```text
署名検証
  ↓
text message取得
  ↓
/reset
  ↓
/closed
  ↓
/jin owner command
  ↓
休業日固定メッセージ
  ↓
manual状態
  ↓
担当者相談ボタン
  ↓
通常AIKA応答
```

この順番にすると、JIN本人の整理コマンドは休業日や手動モードに影響されず、一般ユーザーの体験予約導線も変わらない。

### 分離するもの

JIN Copilotは以下をAIKA本番応答と共有しない。

- AIKA人格プロンプト
- 体験予約の会話履歴
- `user_state` の manual/active 状態
- Quick Replyの体験予約ボタン
- 緊急休業モード
- 顧客会話ログ

JIN Copilot用に別管理するもの:

- `call_jin_copilot()`
- `handle_jin_command()`
- `JIN_AI_INBOX.md`
- `JIN_AI_TASKS.md`
- `JIN_AI_RESUME.md`
- 必要なら `JIN_COPILOT_LOGS/`

### 応答ルール

- `/jin` 応答では体験予約用Quick Replyを出さない
- `/jin` 応答では `HANDOVER_PHRASE` を使わない
- `/jin` 応答で `user_state[uid] = "manual"` にしない
- `/jin` 応答はJIN本人だけに返す
- ファイル反映、削除、本番変更の前には必ず確認する

### 実装方針

最初の実装は、既存AIKAコードへ最小追加にする。

1. `is_owner_jin_command(uid, msg)` を追加
2. `handle_jin_command(msg)` を追加
3. `/jin help` と `/jin resume` だけ先に実装
4. 動作確認後に `/jin capture`、`/jin tasks`、`/jin organize` を増やす

本番反映前には、通常の体験予約、料金案内、休業日コマンド、`/reset` が変わっていないことをLINE実機で確認する。

## 実装ファイル

| ファイル | 役割 |
|---|---|
| `03_SKILLS_INTERNAL/jin_copilot_protocol.md` | AIの振る舞いルール |
| `4_日記/JIN_AI_INBOX.md` | 未整理メモの受け皿 |
| `4_日記/JIN_AI_TASKS.md` | 整理済みタスク |
| `4_日記/JIN_AI_RESUME.md` | 作業再開メモ |
| `.claude/commands/jin-organize.md` | Claude Code用の整理コマンド |
| `.claude/commands/jin-resume.md` | Claude Code用の再開コマンド |
| `AGENTS.md` | Codex用の入口指示 |

## 最小運用

1. JINが雑にメモする
2. AIが `JIN_AI_INBOX.md` を読む
3. AIが分類案を出す
4. JINに「この分類で反映していい？」と確認する
5. 承認後に `JIN_AI_TASKS.md` と `JIN_AI_RESUME.md` を更新する

## 禁止事項

- 未確認でタスクを削除しない
- 未確認で完了扱いにしない
- 未確認で本番システムへ反映しない
- 未確認で外部送信しない
- 提案を決定事項として書かない

## 初期プロンプト

擬人化AIへ移植する時は、以下をシステムプロンプトの芯にする。

```text
あなたはJINの外部作業記憶です。
JINは分析や整理が苦手で、常に多くのタスクを抱えています。
あなたの仕事は、JINの頭の中を見える化し、忘れても戻れる状態を作ることです。

あなたは先回りして提案してよいですが、決定権は必ずJINに残してください。
削除、送信、分類反映、実行、本番変更の前には必ず「〜していい？」と確認してください。

JINが戻ってきたら、前回どこまで進んだか、次の1手は何か、未決定事項は何かだけを短く出してください。
```
