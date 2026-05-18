# AIKA Phase 1 Design — Triage + JIN Notification

作成日: 2026-05-11

## 位置づけ

Phase 1 は、AIKAの応答品質そのものを変える実装ではなく、会話を「AIKAがそのまま返せるもの」と「JIN確認に回すべきもの」に分類し、必要時にJINへ通知するための設計段階とする。

本番反映前に、`6_システム/開発フロー.md` に従って adversarial-review 相当の疑り深い検査とJIN承認を必須にする。

## 前提

以下は2026-05-10時点で解決済み。

| 項目 | 状態 |
|---|---|
| SYSTEM_PROMPT外部ファイル化 | 実装済み。`/root/flatup_brain/1_AIKA人格_本番.md` を読み込み |
| OWNER_USER_ID判定 | 修正済み。`if uid == OWNER_USER_ID:` |
| 本番サービス特定 | `flatup-aika.service` が本命 |
| 祝日・日曜認識 | 実装済み |
| 曜日だけ回答UX | 実装済み |
| P4-1監視・自動修復 | 実装済み |

したがってPhase 1の真のスコープは「トリアージ」と「JIN通知」のみ。

## 目的

AIKAが自動回答すべき範囲を保ちつつ、人間判断が必要な問い合わせを早くJINへ渡す。

狙い:

- 予約確定、例外対応、苦情、医療、個人事情などをAIKA単独で処理しない
- 「担当者より折り返しご連絡」発話による既存手動モード切替と矛盾させない
- JINに届く通知からPII漏洩を増やさない
- 通知が連打されないようにする

## 非目的

Phase 1では以下をやらない。

- AIKA人格プロンプトの変更
- 料金、営業時間、キャンペーン条件の変更
- 予約をAIKAが確定する機能
- 承認Quick Reply UI
- 自動承認、自動反映
- 会員データへの書き込み

## 判定カテゴリ

### auto

AIKAが既存仕様の範囲でそのまま回答してよい。

例:

- 料金
- 場所、アクセス
- クラス種類
- 平日/土曜/日曜/祝日の通常スケジュール
- 体験料金
- 体験希望のヒアリング
- Googleマップ案内
- 「今日は何曜日？」など単純な日時質問

条件:

- 既存の `1_AIKA人格_本番.md` と `build_runtime_context()` の情報だけで回答できる
- 予約確定や例外判断を含まない
- 医療、苦情、トラブル、個別事情ではない

### approval

JIN確認へ回す。AIKAは確定・判断せず、待機メッセージを返す。

例:

- 予約日時を確定してほしい
- 「今日このあと行っていい？」のような当日可否の確定
- 駐車場、見学、持ち物、休会、退会、返金など未定義情報
- キャンペーン、割引、例外対応
- 医療、怪我、妊娠、持病、診断に関わる相談
- 苦情、トラブル、クレーム
- 女性スタッフ、担当者指定など配慮が必要な相談
- 個人情報を多く含む相談
- AIKAが自信を持てない問い合わせ

原則:

- 迷ったら `approval`
- 判定失敗時も `approval`
- OpenRouterや通知処理のエラー時も安全側に倒す

## 既存手動モードとの切り分け

既存:

- AIKAが「担当者より折り返しご連絡」を発話したら `user_state[uid] = "manual"` に切り替わる
- manual中はAI応答せず、「只今担当者が対応中です。少々お待ちください😊」を返す

Phase 1:

- トリアージで `approval` になった時点で、AIKA応答生成前に待機メッセージを返す
- その後 `user_state[uid] = "manual"` に切り替える
- 既存の手動モード挙動を再利用する

つまり、Phase 1は既存手動モードの入口を増やすだけであり、manual中の挙動は変えない。

## 推奨フロー

```text
LINE webhook
  ↓
署名検証
  ↓
text message取得
  ↓
/reset 判定
  ↓
manual状態判定
  ↓
triage(msg, uid)
  ├─ auto
  │   ↓
  │ call_aika(uid, msg)
  │   ↓
  │ reply_line()
  │
  └─ approval
      ↓
      notify_owner()
      ↓
      user_state[uid] = "manual"
      ↓
      reply_line("担当者に確認して、折り返しご連絡いたします😊")
```

補足:

- auto経路では既存の `call_aika()` → `reply_line()` → `HANDOVER_PHRASE` 検出による事後manual化を残す。
- Phase 1は既存manual化を置き換えず、事前防護を追加する。
- `担当者に相談したい` 固定返答はtriageに回さず、既存処理を優先する。

## JIN通知の最小フォーマット

通知先はLINE Push Message APIにする。新しい外部通知サービスは増やさない。

送信先:

- `OWNER_USER_ID = U521cd38b7f048be84eaa880ccabdc7f9`

送信タイミング:

- triageが `approval` を返した直後
- 同一ユーザーの通知クールダウンに引っかからない場合のみ

通知失敗時:

- `ERRORS` に記録
- ユーザー側には待機メッセージを返す
- manual状態には切り替える

通知本文:

```text
【AIKA確認依頼】
分類: approval
理由: {短い理由}
User: {uid先頭8文字}***
受信: {PIIマスク済み本文}
時刻: YYYY-MM-DD HH:MM JST
```

PII方針:

- 電話番号、メール、生年月日は既存 `mask_pii()` を通す
- 氏名はPhase 1では自動マスク対象外だが、通知本文を短くする
- フルUser IDは通知しない
- 会話全文を通知しない

## 通知ストーム対策

同一ユーザーへのapproval通知は短時間に連発しない。

推奨:

- 同一 `uid` につき10分に1回まで
- manual状態中は追加通知しない
- 連続メッセージはログ保存のみ

## トリアージ実装方針

Phase 1ではハイブリッド方式にする。

目的:

- 明確な危険語はルールで即時approval
- 明確な安全質問はルールでauto
- 曖昧な質問だけLLM分類に回す
- LLM失敗時はapprovalに倒す

推奨順:

1. ルールベースで明確なapproval語を検出
2. ルールベースで明確なauto語を検出
3. 判定不能なら軽量LLM分類
4. LLM分類失敗時はapproval

approval語例:

- 確定
- 今日行っていい
- 今から行っていい
- 駐車場
- 見学
- 休会
- 退会
- 返金
- 割引
- キャンペーン
- 怪我
- 痛い
- 病気
- 妊娠
- 薬
- クレーム
- 苦情
- 迷惑
- 怖い

注意:

- `料金` 単独はdanger_wordsに入れない。料金一般の質問はauto候補。
- `予約` 単独はdanger_wordsに入れない。体験希望のヒアリングはauto候補。
- `キャンセル`、`返金`、`休会`、`退会`、`値引き`、`割引`、`変更` など、契約・例外・確定処理を示す語をapprovalにする。
- 「予約したい」はauto候補、「予約をキャンセルしたい」はapproval。
- 「料金プラン教えて」はauto候補、「料金を変更したい」「割引できますか」はapproval。

auto語例:

- 料金
- 場所
- アクセス
- 住所
- クラス
- スケジュール
- 何曜日
- 何時
- 体験
- キック
- 寝技
- キッズ
- レディース

注意:

- `体験` はautoだが、日時確定要求が含まれる場合はapproval
- `今日` は単独ではautoにしない。文脈によりapprovalに倒す
- 医療語が含まれる場合は必ずapproval

LLM分類プロンプト案:

```text
あなたはFLATUP GYMの問い合わせを「auto/approval」に分類するアシスタントです。

approvalの基準:
- 数字・日付・契約に関わる
- 予約確定、料金例外、休会、退会、返金、キャンペーン例外
- クレーム、トラブル、不快表明
- 医療、怪我、妊娠、持病、診断に関わる
- データにない質問、個別事情、例外対応

autoの基準:
- 料金一般
- 場所、アクセス
- 通常クラス紹介
- 通常スケジュール
- 単純な曜日・時刻質問
- 体験の一般案内

回答は1単語のみ:
auto または approval
```

## 失敗時フォールバック

| 失敗 | 対応 |
|---|---|
| msgがNone/空文字 | `approval`, `empty_message` |
| triage例外 | approval |
| notify失敗 | ユーザーへ待機メッセージ、ERRORSへ記録 |
| LINE返信失敗 | ERRORSへ記録 |
| OpenRouter失敗 | 既存fallback |

デプロイ前の必須検証:

```bash
/root/aika_env/bin/python3 -m py_compile /root/line_webhook.py /root/lib/triage.py /root/lib/notify.py
cd /root && /root/aika_env/bin/python3 -c "from lib import triage, notify; print('import ok')"
/root/aika_env/bin/python3 -c 'import json; json.load(open("/root/config/triage_rules.json")); print("json ok")'
```

## adversarial-review 観点

実装前に以下を検査する。

```text
challenge whether this triage function can:
- misjudge urgent cases as auto
- leak PII to JIN notification channels
- conflict with the existing manual-mode auto-switch
- cause notification storms
- increase OpenRouter cost
- create a state where users never return from manual mode
- block normal low-risk questions
```

## Phase 1 合格条件

- SYSTEM_PROMPT外部化やOWNER_USER_ID周辺を再実装しない
- `flatup-aika.service` 以外を触らない
- `auto` の通常質問は既存通り回答される
- `approval` の問い合わせはAIKAが確定回答しない
- approval時にJIN通知が1回だけ出る
- approval後はmanual状態へ入る
- approval時も履歴には短いマーカーだけ残す
- PIIマスク済みで通知/ログ保存される
- `/reset` でmanualから復帰できる
- `/health` が200
- LINE実機テストで通常応答、approval、manual、resetが通る

approval時の履歴マーカー:

```python
add_to_history(uid, "user", msg)
add_to_history(uid, "assistant", "[担当者確認に切り替え済み]")
```

approvalログ:

```markdown
**AIKA:** [APPROVAL] reason=contract notify=sent
**待機メッセージ:** 確認が必要な内容のため、担当者より折り返しご連絡いたします😊
```

`notify` は `sent` / `throttled` / `failed` の3状態で記録する。

## ファイル構成

VPS:

```text
/root/
├── line_webhook.py
├── config/
│   ├── triage_rules.json
│   └── triage_prompt.txt
└── lib/
    ├── __init__.py
    ├── triage.py
    └── notify.py
```

Vault控え:

```text
6_システム/code/
├── line_webhook.py
├── config/
│   ├── triage_rules.json
│   └── triage_prompt.txt
└── lib/
    ├── __init__.py
    ├── triage.py
    └── notify.py
```

`triage_rules` はYAMLではなくJSONにする。PyYAML依存を増やさず、Python標準の `json` で読む。

## テスト計画

### Pre-Deploy

restart前に必ず実行する。

```bash
/root/aika_env/bin/python3 -m py_compile /root/line_webhook.py /root/lib/triage.py /root/lib/notify.py
cd /root && /root/aika_env/bin/python3 -c "from lib import triage, notify; print('import ok')"
/root/aika_env/bin/python3 -c 'import json; json.load(open("/root/config/triage_rules.json")); print("json ok")'
```

いずれか失敗したらrestartしない。

### Smoke Test

```bash
systemctl restart flatup-aika
sleep 2
systemctl is-active flatup-aika
curl -fsS https://line.flatupnarita.jp/health
journalctl -u flatup-aika -n 50 --no-pager | grep -iE 'error|exception|traceback' || true
```

### LINE実機テスト

| # | メッセージ | 期待 |
|---|---|---|
| 1 | `こんにちは` | auto。通常応答。JIN通知なし |
| 2 | `料金教えて` | auto。通常応答。JIN通知なし |
| 3 | `キャンセルしたいです` | approval(contract)。JIN Push + 待機メッセージ |
| 4 | `ひどい対応されました` | approval(complaint)。JIN Push + 待機メッセージ |
| 5 | `駐車場ありますか` | approval(unknown)。JIN Push + 待機メッセージ |
| 6 | 10分以内に `退会したい` | approval。待機メッセージ。Pushはthrottled |
| 7 | `料金プラン教えて` | auto。通常応答。JIN通知なし |

本番でOpenRouterキーやLINE Access Tokenを一時無効化するテストは行わない。

## ロールアウト計画

### Phase A: 準備

Phase A-1のバックアップは、Phase 1ファイルをscpする前に必ず実行する。
ここで保存する `/root/line_webhook.py.bak_20260511_phase1` は、Phase 1適用前の純粋なv5でなければならない。

```bash
cp /root/line_webhook.py /root/line_webhook.py.bak_20260511_phase1
mkdir -p /root/lib /root/config
systemctl cat flatup-aika | head -10
crontab -l | head
```

`linebot.service` と `flatup-bot.service` は旧構成。2026-05-16時点で停止・無効化済みのため、再起動しない。

デプロイ前のJIN確認:

- JINのスマホでAIKA Botのトーク画面を開けること
- 友だち追加されていない場合、LINE Push通知は届かない
- Push通知が届かない状態ではPhase 1の主目的を満たせないため、デプロイ前に友だち状態を確認する

### Phase B: 配置

Mac側:

```bash
cd "/Users/jin/Documents/Obsidian Vault/6_システム/code"

scp -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes \
  lib/__init__.py lib/triage.py lib/notify.py \
  root@162.43.90.71:/root/lib/

scp -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes \
  config/triage_rules.json config/triage_prompt.txt \
  root@162.43.90.71:/root/config/

scp -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes \
  line_webhook.py \
  root@162.43.90.71:/root/line_webhook.py
```

配置直前の再確認:

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "ls -la /root/line_webhook.py.bak_20260511_phase1 && cmp -s /root/line_webhook.py /root/line_webhook.py.bak_20260511_phase1 && echo BACKUP_MATCHES_CURRENT"
```

`BACKUP_MATCHES_CURRENT` が出ない場合、すでに `/root/line_webhook.py` が変更されている可能性があるため、配置を止めて差分確認する。

### Phase C: 静的検証

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "/root/aika_env/bin/python3 -m py_compile /root/line_webhook.py /root/lib/triage.py /root/lib/notify.py && echo SYNTAX_OK"

ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "cd /root && /root/aika_env/bin/python3 -c 'from lib import triage, notify; print(\"import ok\")'"

ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "/root/aika_env/bin/python3 -c 'import json; json.load(open(\"/root/config/triage_rules.json\")); print(\"json ok\")'"
```

### Phase D: 本番反映

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "systemctl restart flatup-aika && sleep 2 && systemctl is-active flatup-aika"
```

### Phase E: 動作確認

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "systemctl is-active flatup-aika"

curl -fsS https://line.flatupnarita.jp/health

ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "journalctl -u flatup-aika -n 50 --no-pager | grep -iE 'error|exception|traceback' || true"
```

その後、JINのLINEで実機6ケースを確認する。

## ロールバック

問題発生時:

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 << 'EOF'
systemctl stop flatup-aika
cp /root/line_webhook.py.bak_20260511_phase1 /root/line_webhook.py

ts="$(date +%Y%m%d-%H%M%S)"
mkdir -p "/root/phase1_disabled_$ts"
mv /root/lib/triage.py /root/lib/notify.py /root/lib/__init__.py "/root/phase1_disabled_$ts/" 2>/dev/null || true
mv /root/config/triage_rules.json /root/config/triage_prompt.txt "/root/phase1_disabled_$ts/" 2>/dev/null || true

systemctl start flatup-aika
sleep 2
systemctl is-active flatup-aika
EOF

curl -fsS https://line.flatupnarita.jp/health
```

`/root/config` や `/root/lib` 全体は消さず、Phase 1用ファイルだけ退避する。

## デプロイ推奨時間

- 平日22時以降
- 日曜・祝日

平日10〜20時は会員問い合わせと干渉しやすいため避ける。

## デプロイ後の事後作業

1. `LINE_BOT_仕様.md` の実装済み機能にPhase 1を追加
2. `CLAUDE.md` の実装済み機能にtriageを追加
3. `PHASE1_DESIGN.md` を実装実態に合わせて更新
4. `6_システム/code/` のPhase 1ファイルをGit管理

## 実装前のJIN承認事項

- approval判定語の初期リスト
- ユーザー向け待機メッセージ文面
- JIN通知先はLINE Pushでよいか
- 通知クールダウン時間は10分でよいか
- LLM分類を使うか、初期版はルールのみで始めるか

## 推奨判断

現時点では、すぐ本番実装せず、まずこの設計を確認する。

JIN承認後、Phase 1実装は「トリアージ + 通知」のみに限定して行う。
