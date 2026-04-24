# FLATUP GYM LINE Bot — 仕様書 (v3.0 / 2026-04-23診断反映)

## 1. 稼働環境(確定情報)

| 項目 | 値 |
|---|---|
| VPS | Ubuntu 24.04 LTS (162.43.90.71) |
| SSH接続 | `ssh root@162.43.90.71` |
| ドメイン | line.flatupnarita.jp (HTTPS済み) |
| リバースプロキシ | nginx → port 5000 |
| Webhook URL | https://line.flatupnarita.jp/webhook |
| プロセス管理 | systemd (flatup-aika.service) |

## 2. 稼働中のBot実態

### flatup-aika サービス(本命・稼働中)
- 実行ファイル: `/root/line_webhook.py` (v5、9916バイト超)
- フレームワーク: **Flask**(port 5000)
- venv: `/root/aika_env/bin/python3`
- 環境変数: `/root/flatup_config.env`
- ログ出力: `/var/log/flatup_aika.log` + journald

### 環境変数(`/root/flatup_config.env`)
```
LINE_CHANNEL_SECRET
LINE_ACCESS_TOKEN
OPENROUTER_API_KEY
OBSIDIAN_PATH  (デフォルト: /root/flatup_brain)
```

### 主要定数(コード内)
- `MODEL`: `anthropic/claude-haiku-4-5`
- `OWNER_USER_ID`: `U521cd38b7f048be84eaa880ccabdc7f9`
- `MAX_HISTORY`: 10ターン
- `HANDOVER_PHRASE`: "担当者より折り返しご連絡"
- `MAPS_URL`: Googleマップ(土屋516-4 青柳ビル2F)

## 3. 既存実装機能一覧

### 応答ロジック(48-92行目のSYSTEM_PROMPT)
- 人格: クールで知的、女性・子供・初心者に優しい
- ジム情報ハードコード済み(場所・料金・クラス・スケジュール)
- 体験アポ誘導: 名前・希望種目・希望日時を聞き出す
- データ外質問は手動誘導
- 出力制約: 200文字・絵文字1〜2個・マークダウン禁止

### 会話履歴管理
- `conversation_history[uid]` にuser/assistant交互保存
- 最大10ターン保持
- **インメモリ(systemctl restartで消失)**

### 状態管理
- `user_state[uid] = "active" | "manual"`
- 「担当者より折り返しご連絡」発話で自動manual切替
- `/reset` でactive復帰(オーナーのみ)

### Quick Reply
5つのQRセット定義済み:
- QR_TOP: 体験/料金/クラス/場所/相談
- QR_MAP: Googleマップ/体験/相談
- QR_DAY: 平日/土曜/相談
- QR_WEEKDAY_TIME: 10-12時/18-20時
- QR_SATURDAY_TIME: 10キック/11寝技/13キッズ/14レディース

### Obsidian連携(書き込みのみ)
- `/root/flatup_brain/LOGS/`: 会話ログ保存
- `/root/flatup_brain/ERRORS/`: エラーログ保存
- **読み込み連携は未実装**

## 4. 改修ロードマップ

### 工程1: 現状凍結(最優先・30分)
```bash
cd /root/
git init
git add line_webhook.py
git commit -m "初期コミット:現行稼働版v5スナップショット"
# GitHubのprivateリポジトリにpush
```

### 工程2: requirements.txt生成(5分)
```bash
/root/aika_env/bin/pip freeze > /root/requirements.txt
```

### 工程3: 幽霊サービス退役(10分)
```bash
mv /home/flatup /root/_archive_flatup_main
mv /etc/systemd/system/flatup.service /root/_archive_flatup_main/
systemctl daemon-reload
```

### 工程4: SYSTEM_PROMPT外部ファイル化(1日)
48-92行目を抽出 → `/root/flatup_brain/1_AIKA人格_本番.md` として保存
line_webhook.pyを改修し起動時読み込みに変更
JINはObsidianで編集 → git push → VPS git pull → restartで反映

### 工程5: OWNER_USER_IDバグ修正(15分)
```python
# 修正前(常にTrue疑い)
if OWNER_USER_ID == "U521cd38b7f048be84eaa880ccabdc7f9" or uid == OWNER_USER_ID:
# 修正後
if uid == OWNER_USER_ID:
```

### 工程6: プロンプトキャッシング有効化(30分)
OpenRouterリクエストに `cache_control` ヘッダー追加
月コスト90%削減

### 工程7: Mac-VPS Obsidian同期ライン(2時間)
- GitHub privateリポジトリ `flatup1/flatup-brain` 作成
- Mac側: FLATUP_BRAINをpush
- VPS側: `/root/flatup_brain` をclone
- `update_aika.sh` ワンコマンド化

## 5. 手動返信との共存(実装不要)
LINE標準「手動チャット」機能(60分タイマー)を使用。
加えて、AIKAが「担当者より折り返しご連絡」を発話すると
自動で手動モードに切替わる既存ロジックも活用。追加実装は不要。

## 6. 既知リスク
- インメモリ状態管理: systemctl restartで会話履歴・状態消失
- `User=root`動作: セキュリティリスク、将来的に専用ユーザー化推奨
- 239行目ロジックバグ疑い: 工程5で修正予定
- requirements.txt不在: 工程2で解決
