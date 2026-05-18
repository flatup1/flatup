# JIN Copilot LINE Command Design

公式LINE上で、JIN本人だけがJIN Copilotを呼び出すための設計メモ。

この設計は、FLATUP GYMの体験予約システムとは別系統で動かす。

## 目的

JINが公式LINEへ専用コマンドを送ると、AIKAの顧客対応ではなく、JIN個人の思考整理・作業再開支援が返るようにする。

## 起動条件

JIN Copilotは、以下をすべて満たす場合だけ起動する。

- `uid == OWNER_USER_ID`
- `msg.startswith("/jin")`
- LINE署名検証に成功済み

それ以外のユーザーでは起動しない。

## 初期コマンド

最初は小さく始める。

| コマンド | 役割 |
|---|---|
| `/jin help` | 使えるコマンド一覧を返す |
| `/jin resume` | `4_日記/JIN_AI_RESUME.md` の要約を返す |
| `/jin tasks` | `4_日記/JIN_AI_TASKS.md` の今日見る項目を返す |
| `/jin capture ...` | 内容をINBOXへ預ける提案を返す |
| `/jin organize` | INBOX整理の確認メッセージを返す |

## Webhook差し込み位置

`line_webhook.py` の `webhook()` 内で、既存オーナーコマンドの直後に差し込む。

```python
# /reset
...

# /closed
...

# /jin owner command
jin_reply = handle_jin_command(msg, uid)
if jin_reply is not None:
    reply_line(token, jin_reply, None)
    continue
```

`reply_line()` は現状Quick Reply必須の形なので、実装時は以下のどちらかにする。

- `quick_items=None` を許可する
- JIN Copilot専用のQuick Replyなし送信関数を作る

## 推奨関数

```python
JIN_COMMAND_PREFIX = "/jin"

def is_owner_jin_command(uid, msg):
    return uid == OWNER_USER_ID and msg.startswith(JIN_COMMAND_PREFIX)

def handle_jin_command(msg, uid):
    if not is_owner_jin_command(uid, msg):
        return None

    command = msg[len(JIN_COMMAND_PREFIX):].strip()

    if command in ("", "help"):
        return build_jin_help()
    if command == "resume":
        return read_jin_resume()
    if command == "tasks":
        return read_jin_today_tasks()
    if command.startswith("capture "):
        return propose_jin_capture(command.removeprefix("capture ").strip())
    if command == "organize":
        return "INBOXを整理候補に分けます。反映前に確認します。整理していい？"

    return "未対応のJINコマンドです。/jin help を見てください。"
```

## 絶対に共有しないもの

JIN Copilotは以下を使わない、または変更しない。

- `SYSTEM_PROMPT`
- `call_aika()`
- 体験予約の `conversation_history`
- `user_state`
- `closed_dates.json`
- `closed_mode`
- 体験予約用Quick Reply
- `HANDOVER_PHRASE`

## ログ

顧客ログとは分ける。

推奨:

- `JIN_COPILOT_LOGS/YYYY-MM-DD.md`

顧客会話ログ `LOGS/conversation_{user_id}.md` には混ぜない。

## 実装前チェック

- [ ] `/reset` が今まで通り動く
- [ ] `/closed today` が今まで通り動く
- [ ] 一般ユーザーの「体験したい」が今まで通り動く
- [ ] 一般ユーザーが `/jin help` を送ってもJIN Copilotが起動しない
- [ ] JIN本人の `/jin resume` だけがJIN Copilotへ分岐する
- [ ] `/jin` 応答でmanual状態にならない
- [ ] `/jin` 応答で体験予約Quick Replyが出ない
