# FLATUP AI OS 完全修復マニュアル

**最終更新：2026年4月14日**
**管理者：JIN（仁志）**

---

## システム構成図

```
LINEユーザー
    ↓ (HTTPS)
LINE Platform
    ↓ (POST)
https://api.flatupnarita.jp/webhook
    ↓ (Cloudflare Tunnel)
中継スクリプト (localhost:8765)
    ↓ (HTTP POST /v1/chat-messages)
Dify nginx (localhost:80)
    ↓
Dify API → AIKA が回答
    ↓
LINE に返信
```

---

## サーバー情報

| 項目 | 値 |
|------|-----|
| VPS | Xserver VPS (Ubuntu) |
| IP | 162.43.90.71 |
| SSH | `ssh root@162.43.90.71` |
| ドメイン | flatupnarita.jp (Cloudflare管理) |
| Webhook URL | https://api.flatupnarita.jp/webhook |
| Tunnel ID | 0eee1b69-7bee-46ee-bb9e-048c07fcf4d7 |

---

## 3つのサービス一覧

| サービス | 役割 | ポート | 自動起動 | 自動復旧 |
|----------|------|--------|----------|----------|
| Docker (Dify) | AI エンジン | 80 | ✅ enabled | ✅ restart: always |
| cloudflared | HTTPS トンネル | - | ✅ enabled | ✅ systemd Restart |
| line-webhook | LINE↔Dify 中継 | 8765 | ✅ enabled | ✅ systemd Restart |

---

## トラブル発生時：最初にやること

### ステップ1：全サービスの状態を一括確認

```bash
ssh root@162.43.90.71
```

```bash
echo "=== Docker ===" && systemctl is-active docker && echo "=== Dify コンテナ ===" && docker ps --format "table {{.Names}}\t{{.Status}}" | grep docker && echo "=== Cloudflare Tunnel ===" && systemctl is-active cloudflared && echo "=== LINE Webhook ===" && systemctl is-active line-webhook
```

全部 `active` なら正常。どれかが `inactive` や `failed` なら以下の個別対応へ。

---

## 障害パターン別 修復手順

---

### 障害1：LINE から返信が来ない（全体停止）

**原因の切り分け**

```bash
# 1. 中継スクリプトのログ確認
journalctl -u line-webhook --since "10 minutes ago" --no-pager

# 2. Cloudflare Tunnelのログ確認
journalctl -u cloudflared --since "10 minutes ago" --no-pager

# 3. Difyの稼働確認
curl -s -o /dev/null -w "%{http_code}" http://localhost:80
```

**全部再起動（最速の復旧方法）**

```bash
cd /root/dify/docker && docker compose restart
systemctl restart cloudflared
systemctl restart line-webhook
```

---

### 障害2：Dify が落ちている

**症状**
- `docker ps` でコンテナが少ない or STATUSが `Exited`
- `curl http://localhost:80` が応答しない

**修復**

```bash
cd /root/dify/docker
docker compose down
docker compose up -d
```

**確認**

```bash
docker ps | grep -c "Up"
# 11個前後のコンテナが Up なら正常
```

**ディスク容量不足の場合**

```bash
df -h /
# 90%超えていたら以下でDocker不要イメージ削除
docker system prune -f
```

---

### 障害3：Cloudflare Tunnel が落ちている

**症状**
- `systemctl status cloudflared` が `failed` or `inactive`
- ブラウザで `https://api.flatupnarita.jp` にアクセスすると 502 や接続エラー

**修復**

```bash
systemctl restart cloudflared
systemctl status cloudflared
```

**設定ファイルが壊れた場合**

```bash
cat > /etc/cloudflared/config.yml << 'EOF'
tunnel: 0eee1b69-7bee-46ee-bb9e-048c07fcf4d7
credentials-file: /root/.cloudflared/0eee1b69-7bee-46ee-bb9e-048c07fcf4d7.json

ingress:
  - hostname: api.flatupnarita.jp
    service: http://localhost:8765
  - service: http_status:404
EOF

systemctl restart cloudflared
```

---

### 障害4：中継スクリプト（line-webhook）が落ちている

**症状**
- `systemctl status line-webhook` が `failed`
- LINE検証で 502 Bad Gateway

**修復**

```bash
systemctl restart line-webhook
systemctl status line-webhook
```

**スクリプトにエラーがある場合**

```bash
# ログでエラー内容を確認
journalctl -u line-webhook --since "30 minutes ago" --no-pager

# Pythonの依存パッケージが消えた場合
pip install flask requests --break-system-packages

systemctl restart line-webhook
```

---

### 障害5：Dify APIキーが無効になった

**症状**
- LINEで「ただいま混み合っております」と返ってくる
- line-webhook のログに `401` エラー

**修復**
1. ブラウザで Dify ダッシュボード（`http://162.43.90.71:80`）を開く
2. AIKA アプリ → API アクセス → 新しいAPIキーを発行
3. スクリプトを更新：

```bash
nano /root/line-webhook/app.py
# DIFY_API_KEY = "app-xxxxxx" の行を新しいキーに書き換え
# Ctrl+O で保存、Ctrl+X で終了

systemctl restart line-webhook
```

---

### 障害6：LINE アクセストークンが期限切れ

**症状**
- line-webhook のログに LINE API への `401` エラー
- Difyからの回答は取得できているが、LINEに返信できない

**修復**
1. LINE Developers コンソールでチャネルアクセストークンを再発行
2. スクリプトを更新：

```bash
nano /root/line-webhook/app.py
# LINE_ACCESS_TOKEN = "xxxxx" の行を新しいトークンに書き換え

systemctl restart line-webhook
```

---

### 障害7：VPS が再起動された

**通常は自動復旧するが、確認手順：**

```bash
ssh root@162.43.90.71

# 全サービス確認
systemctl is-active docker cloudflared line-webhook

# Difyコンテナ確認（起動に1-2分かかる場合あり）
docker ps | grep -c "Up"

# テスト
curl -s -o /dev/null -w "%{http_code}" http://localhost:80
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/webhook
```

---

### 障害8：メモリ不足 / スワップ不足

**症状**
- サーバーが極端に遅い
- コンテナが勝手に落ちる（OOM Killed）

**確認**

```bash
free -h
```

**応急処置：スワップ拡張**

```bash
# 既存スワップ確認
swapon --show

# 2GBスワップ追加
fallocate -l 2G /swapfile2
chmod 600 /swapfile2
mkswap /swapfile2
swapon /swapfile2

# 永続化
echo '/swapfile2 none swap sw 0 0' >> /etc/fstab
```

---

### 障害9：ディスク容量不足

**確認**

```bash
df -h /
```

**対応**

```bash
# Dockerログの削除
truncate -s 0 /var/lib/docker/containers/*/*-json.log

# 不要イメージの削除
docker system prune -af

# 大きなファイルの特定
du -sh /root/* | sort -rh | head -10
```

---

## 定期メンテナンス（月1回推奨）

```bash
# 1. システム更新
apt update && apt upgrade -y

# 2. Dockerイメージ更新（Dify）
cd /root/dify/docker
docker compose pull
docker compose up -d

# 3. cloudflared更新
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
dpkg -i cloudflared.deb
systemctl restart cloudflared

# 4. ディスク掃除
docker system prune -f

# 5. 全サービス確認
systemctl is-active docker cloudflared line-webhook
```

---

## 重要ファイルの場所

| ファイル | パス |
|----------|------|
| 中継スクリプト | `/root/line-webhook/app.py` |
| Cloudflare設定 | `/etc/cloudflared/config.yml` |
| Cloudflare認証 | `/root/.cloudflared/0eee1b69-7bee-46ee-bb9e-048c07fcf4d7.json` |
| Dify設定 | `/root/dify/docker/.env` |
| Dify compose | `/root/dify/docker/docker-compose.yaml` |
| line-webhook サービス | `/etc/systemd/system/line-webhook.service` |
| cloudflared サービス | `/etc/systemd/system/cloudflared.service` |

---

## 認証情報（要厳重管理）

このドキュメントにAPIキー、トークン、Secretの実値を記載しない。
実値はVPS上の環境変数ファイルまたは各サービス管理画面で確認する。

| 項目 | 値 |
|------|-----|
| LINE Channel Secret | `/root/flatup_config.env` または LINE Developers |
| LINE Access Token | `/root/flatup_config.env` または LINE Developers |
| Dify API Key | Dify管理画面で再発行・確認 |
| VPS SSH | 接続先情報のみ。秘密鍵やパスワードは記載禁止 |

---

## 緊急連絡先

- **Xserver VPS サポート**: https://www.xserver.ne.jp/support/
- **Cloudflare ステータス**: https://www.cloudflarestatus.com/
- **LINE Developers**: https://developers.line.biz/

---

## 完全ゼロからの再構築手順（最終手段）

万が一VPSを初期化した場合：

```bash
# 1. Docker インストール
apt update && apt install -y docker.io docker-compose-v2
systemctl enable docker

# 2. Dify インストール
cd /root
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
docker compose up -d

# 3. cloudflared インストール
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
dpkg -i cloudflared.deb
cloudflared tunnel login
# ※ブラウザで flatupnarita.jp を認証

# 4. トンネル再作成
cloudflared tunnel create flatup-dify
cloudflared tunnel route dns flatup-dify api.flatupnarita.jp
# ※新しいTunnel IDで config.yml を作成

# 5. 中継スクリプト設置
mkdir -p /root/line-webhook
# app.py を配置（認証情報は環境変数ファイルから読み込む）
pip install flask requests --break-system-packages

# 6. サービス登録
# line-webhook.service と cloudflared service install を実行
systemctl enable --now line-webhook cloudflared

# 7. Dify で AIKA アプリを再作成し、APIキーを取得して app.py に設定

# 8. LINE Developers で Webhook URL を設定
# https://api.flatupnarita.jp/webhook
```
