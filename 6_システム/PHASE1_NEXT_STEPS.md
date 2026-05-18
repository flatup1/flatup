# AIKA Phase 1 Next Steps

作成日: 2026-05-11

## 現在の採点

総合: 82 / 100

実用体感: 88〜90 / 100

```text
セキュリティ        35 / 40
可用性              14 / 20
運用性              13 / 15
機能完成度          15 / 15
自動化・PII保護      6 / 10
```

## 実装済み

| 領域 | 状態 |
|---|---|
| APIキー再発行 + 環境変数化 | 完了 |
| SSH鍵認証のみ | 完了 |
| ログ権限・PIIマスク・180日削除 | 完了 |
| Git履歴クリーニング | 完了 |
| P4-1 監視・自動修復（5分cron） | 完了 |
| AIKA 時刻認識・営業状態・日曜祝日 | 完了 |
| 応答情報量調整（曜日だけ返す） | 完了 |
| CLAUDE.md v4.0 + 開発フロー + 仕様書 v4 | 完了 |
| Phase 1 設計 | 完了、未実装 |

## 次回最優先

Phase 1 トリアージ + JIN通知の実装。

目的:

```text
AIKAが回答を生成する前に、事故りやすい問い合わせを検知し、
JIN確認へ回してmanual状態に切り替える。
```

## ステップ0: ヘルスチェック

Macから:

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "systemctl status flatup-aika --no-pager | head -3 && curl -fsS https://line.flatupnarita.jp/health && echo"
```

期待値:

```text
Active: active (running)
{"aika":"v5","status":"ok"}
```

## ステップ1: 設計再読

```text
6_システム/PHASE1_DESIGN.md
```

違和感があれば実装前に修正する。

## ステップ2: 実装手順書作成

作成先:

```text
6_システム/PHASE1_IMPLEMENTATION_PLAN.md
```

内容:

- ファイル作成順
- line_webhook.pyの差分位置
- 静的検証
- デプロイ
- 実機テスト
- ロールバック

## ステップ3: 実装ファイル作成

Vault側:

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

## ステップ4: デプロイ

### Phase A: バックアップ

Phase 1ファイルをscpする前に必ず実行する。

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "cp /root/line_webhook.py /root/line_webhook.py.bak_20260511_phase1 && ls -la /root/line_webhook.py.bak_20260511_phase1"
```

### Phase A': 配置直前ガード

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "cmp -s /root/line_webhook.py /root/line_webhook.py.bak_20260511_phase1 && echo BACKUP_MATCHES_CURRENT"
```

`BACKUP_MATCHES_CURRENT` が出なければscpしない。

### Phase B: scp配置

```bash
cd "/Users/jin/Documents/Obsidian Vault/6_システム/code"

ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "mkdir -p /root/lib /root/config"

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

### Phase C: 静的検証

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "/root/aika_env/bin/python3 -m py_compile /root/line_webhook.py /root/lib/triage.py /root/lib/notify.py && echo SYNTAX_OK"

ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "cd /root && /root/aika_env/bin/python3 -c 'from lib import triage, notify; print(\"import ok\")'"

ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "/root/aika_env/bin/python3 -c 'import json; json.load(open(\"/root/config/triage_rules.json\")); print(\"json ok\")'"
```

3つともOKなら次へ。1つでもNGならrestartしない。

### Phase D: 本番反映

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "systemctl restart flatup-aika && sleep 2 && systemctl is-active flatup-aika"
```

### Phase E: smoke test

```bash
curl -fsS https://line.flatupnarita.jp/health
```

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "journalctl -u flatup-aika -n 50 --no-pager | grep -iE 'error|exception|traceback' || true"
```

## ステップ5: 実機テスト

| # | メッセージ | 期待 |
|---|---|---|
| 1 | `こんにちは` | auto、JIN通知なし |
| 2 | `料金教えて` | auto、JIN通知なし |
| 3 | `料金プラン教えて` | auto、JIN通知なし |
| 4 | `キャンセルしたいです` | approval + JIN通知 |
| 5 | `ひどい対応されました` | approval + JIN通知 |
| 6 | `駐車場ありますか` | approval + JIN通知 |
| 7 | 5分以内に `退会したい` | approval + throttled、Pushなし |

## ステップ6: 仕様書更新 + commit

Mac側:

```bash
cd "/Users/jin/Documents/Obsidian Vault"
git add CLAUDE.md README.md 6_システム/ 99_REFERENCE/vault_structure.md
git commit -m "feat: Phase 1 トリアージ + JIN通知を本番反映"
git push origin main
```

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

`/root/lib` と `/root/config` 全体は退避しない。Phase 1用ファイルだけ退避する。

## 推奨デプロイ時間帯

| 時間 | 推奨度 | 理由 |
|---|---|---|
| 平日22時以降 | 高 | 営業終了後、JINがスマホで通知確認可能 |
| 日曜・祝日 | 最高 | 定休日で会員影響が少ない |
| 平日10〜20時 | 非推奨 | 会員問い合わせと干渉 |

## Phase 1完了後の予測

```text
現在:          82 / 100
Phase 1完了:  87 / 100 目安
```

ただし正式スコアは、実機7ケースとログ確認後に再採点する。
