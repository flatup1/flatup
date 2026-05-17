# Task Management Skill v1.0.0

## Purpose

JIN専用タスク管理。
`inbox.md` / `board.md` / `done.md` の3ファイルを操作し、忘れても前回の続きから迷わず再開できる状態を作る。

## Triggers

- `/朝` -> `morning_briefing`
- `/メモ <内容>` -> `append_to_inbox`
- `/夜` -> `night_review_preview`
- `/保存` -> `save_night_review`
- `/再開` -> `resume_last_task`

## Mode: morning_briefing

1. `board.md` を読み込む
2. 🔴A・🟡B・🔵C・昨日の続き を整形する
3. AIKAの提案を1つだけ生成する
4. 「この順番で進めていいですか？」で終わる

## Mode: append_to_inbox

1. `inbox.md` の今日セクションに追記する
2. 短く返信する
3. 勝手に実行・分類しない

## Mode: night_review_preview

1. `inbox.md` と `board.md` を読み込む
2. 完了 / 明日に回す / 途中で止まったもの / 明日の最初の一手を整理する
3. この時点ではファイル更新しない
4. 保存前プレビューを表示する
5. 「この内容で保存していいですか？」で終わる

## Mode: save_night_review

1. 直前の `night_review_preview` の内容を保存する
2. `done.md` に再開ログを追記する
3. `board.md` に明日のタスク案を反映する
4. `inbox.md` の処理済み項目を整理する
5. 保存完了を短く報告する

## Mode: resume_last_task

1. `done.md` を読み込む
2. 最後に止まった作業を表示する
3. 次にやる一手を表示する
4. AIKAの提案を1つだけ出す
5. 「この作業から再開していいですか？」で終わる

## Rules

- 提案は1回1つまで
- 必ず確認質問で終わる
- Lv3行動は禁止
- 実行前に必ずJINへ確認する
- タスクはAとBを優先し、Cは保管のみ
- Cを今日の実行対象にしない
- `/夜` はプレビューだけで、ファイルを更新しない
- `/保存` は直前の `/夜` プレビューがある場合だけ実行する
