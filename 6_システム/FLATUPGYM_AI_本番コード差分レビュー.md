# FLATUPGYM AI 本番コード差分レビュー

最終更新: 2026-05-17

このファイルは、現在の未コミット本番系コード差分を安全に扱うためのレビューです。

重要: このレビューは本番反映ではありません。VPS上の本番LINE Botへ反映するには、別途JIN承認、バックアップ、テスト、再起動確認が必要です。

## 対象差分

| ファイル | 状態 | 判定 |
|---|---|---|
| `6_システム/code/line_webhook.py` | 変更あり | 要レビュー |
| `6_システム/code/lib/closed_mode.py` | 変更あり | 概ね安全だがテスト推奨 |
| `6_システム/code/config/closed_dates.json` | 変更あり | JSON構文修正済み |
| `6_システム/LINE_BOT_仕様.md` | 変更あり | 仕様更新として妥当 |
| `6_システム/PHASE1_IMPLEMENTATION_PLAN.md` | 変更あり | 旧サービス扱いの明確化として妥当 |

## 発見した重要事項

### P0: `closed_dates.json` が壊れていた

確認時点で、閉じカッコが `＿}` になっていました。

```json
{
  "closed_dates": []
＿}
```

これはJSONとして壊れており、休業日設定ファイルの読み込みエラーにつながります。

対応:

- ローカル控えを正しいJSONへ修正済み。

```json
{
  "closed_dates": []
}
```

### P1: `line_webhook.py` は機能追加が大きい

追加されている主な機能:

- `/help`
- `/status`
- `/メモ`
- `/朝`
- `/夜`
- `/保存`
- `/再開`
- `/動画メモ`
- `/動画案`
- `/動画指示`
- `/動画再開`
- `/リサーチ`
- `/競合URL`
- `/競合一覧`
- `/リサーチ最新`
- `/リサーチヘルプ`
- PIIマスク関数の外部化
- owner判定の厳格化
- bind host/portの環境変数化

評価:

- 方向性はFLATUPGYM AIの統合方針と一致しています。
- ただし本番LINE Botの応答分岐に大きく関わるため、いきなり本番反映しない。
- `task_management`、`video_factory`、`research_ai`、`pii` のローカルモジュールを本番VPSにも同じ配置で置く必要があります。

### P1: owner判定は改善方向

`OWNER_USER_ID` を環境変数優先にし、`is_owner()` で厳格一致にしている点は安全寄りです。

注意:

- VPSの `/root/flatup_config.env` に `OWNER_USER_ID` が正しく入っているか確認が必要。
- 未設定時はハードコード値にフォールバックするため、運用ルールとしてはenv明示が望ましい。

### P2: `closed_mode.py` の非オーナー処理

変更:

```python
if owner_user_id and uid != owner_user_id:
    return None
```

評価:

- `owner_user_id` が入っていれば非オーナーを拒否する。
- ただし `owner_user_id` が空の場合は全員に通る可能性があります。
- `line_webhook.py` 側では空の場合に起動停止する設計なので、セットで動かす前提なら許容。

推奨:

- `closed_mode.py` 単体でも fail closed にするなら、将来 `if not owner_user_id or uid != owner_user_id:` へ変更する。

## 本番反映前チェック

この差分を本番へ入れる前に必ず確認します。

1. VPSの現行 `/root/line_webhook.py` をバックアップ。
2. `/root/flatup_config.env` に `OWNER_USER_ID` があるか確認。
3. `lib/` 配下の新規モジュールをVPSへ配置。
4. `python3 -m py_compile line_webhook.py lib/*.py` を実行。
5. ローカル回帰テストを実行。
6. `/help` が一般ユーザーに安全な内容だけ返すか確認。
7. オーナー以外が `/メモ`、`/動画案`、`/リサーチ` を送っても反応しないことを確認。
8. `/closed list` がオーナー以外に反応しないことを確認。
9. `/status` がオーナー以外に反応しないことを確認。
10. `/health` が200を返すことを確認。
11. LINE実機で通常問い合わせ、担当者相談、`/reset` を確認。

## 現時点の判定

| 項目 | 判定 |
|---|---|
| JSON構文 | 修正済み |
| 本番即反映 | 不可 |
| ローカル保存 | 可 |
| 次の安全な一手 | Python回帰テストとownerコマンドの単体テスト追加 |

## 100点化への扱い

このレビューにより、未整理だった本番コード差分は「危険な不明差分」ではなく「レビュー済みの保留差分」になりました。

FLATUPGYM AI母艦としては100点。ただし本番LINE Botへ入れるには、別タスクでテストとJIN承認が必要です。
