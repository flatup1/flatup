# OpenClaw 本番環境セットアップ — ステップバイステップ作業指示

明日から1日ずつ、この順で進めてください。各ステップが終わったら ✓ を付けて進みます。

---

## 【Day 1】準備：Mac 側の確認と VPS 接続

### 1-1. Mac の OpenClaw を止める
- ターミナルで OpenClaw を起動している場合は **Ctrl+C** で停止する
- 念のため: `pkill -9 -f openclaw` を実行してプロセスが残っていないか確認

### 1-2. 設定ファイルのバックアップ
- Finder で **書類** または **デスクトップ** にフォルダ `openclaw-backup` を作成
- 以下をコピーして保存する:
  - `~/.openclaw/openclaw.json`
  - `~/.openclaw/config.json`（あれば）

### 1-3. VPS に SSH でログインできるか確認
- ターミナルで: `ssh ユーザー名@162.43.90.71`（IP・ユーザー名は自分の環境に合わせる）
- パスワードまたは鍵でログインできれば OK。ログインできたら一度 `exit` で抜ける

**Day 1 のゴール:** バックアップ完了 & VPS にログインできる状態

---

## 【Day 2】VPS 上で OpenClaw を最新版にする

### 2-1. VPS に SSH ログイン
```bash
ssh ユーザー名@162.43.90.71
```

### 2-2. 既存の OpenClaw を止める
```bash
pkill -9 -f openclaw
```

### 2-3. Node のバージョン確認
```bash
node -v
```
- 表示が **v22 以上** ならそのまま次へ
- それ以外なら、先に Node 22 のインストール手順（別途案内）を実施

### 2-4. OpenClaw を最新版でインストール
```bash
npm install -g openclaw@latest
```

### 2-5. バージョン確認
```bash
openclaw --version
```
- バージョンが表示されれば OK

**Day 2 のゴール:** VPS で `openclaw --version` が動くこと

---

## 【Day 3】VPS で OpenClaw を起動する

### 3-1. VPS に SSH ログイン（まだログイン中ならそのまま）

### 3-2. 起動用トークン（パスワード）を決める
- 例: `MyOpenClaw2026!` など、自分だけが知っている文字列
- メモしておく（ブラウザログインで使う）

### 3-3. トークン付きで起動
```bash
openclaw gateway --allow-unconfigured --token ここに決めたトークンを入れる
```
例:
```bash
openclaw gateway --allow-unconfigured --token MyOpenClaw2026!
```

### 3-4. ログを確認
- `Gateway failed to start` が出ず、何かしら「待ち受け」や「listening」のようなメッセージが出ていれば成功
- エラーが出た場合は、そのメッセージをそのままコピーして保存（後で原因調査に使う）

### 3-5. 起動確認後、一度止める
- **Ctrl+C** で停止
- （次の Day 4 でパケットフィルターを開けてから、再度起動する）

**Day 3 のゴール:** `openclaw gateway --allow-unconfigured --token ...` でエラーなく起動すること

---

## 【Day 4】パケットフィルター設定とブラウザアクセス

### 4-1. XServer VPS パネルにログイン
- ブラウザで XServer VPS の管理画面を開く

### 4-2. パケットフィルターでポート開放
1. 左メニュー **「パケットフィルター設定」** をクリック
2. **「パケットフィルター設定を追加する」** を選ぶ
3. 次を入力:
   - **ポート番号:** `18789`
   - **プロトコル:** `TCP`
   - **コメント:** `OpenClaw用`
4. 保存

### 4-3. VPS で OpenClaw を再度起動
- SSH で VPS に接続し、Day 3 と同じコマンドを実行:
```bash
openclaw gateway --allow-unconfigured --token あなたのトークン
```

### 4-4. Mac のブラウザからアクセス
- アドレスバーに入力: `http://162.43.90.71:18789`（IP は自分の VPS に合わせる）
- ログイン画面が出たら、Day 3 で決めたトークンを入力
- ダッシュボードが表示されれば成功

**Day 4 のゴール:** ブラウザで VPS の OpenClaw ダッシュボードにログインできること

---

## 【Day 5】設定を VPS に反映する（OpenRouter・Telegram）

### 5-1. Mac の設定を VPS に持っていく方法を選ぶ

**方法 A: ファイルをコピーする**
- Mac の `~/.openclaw/openclaw.json` を VPS の `~/.openclaw/openclaw.json` にコピー
  - 例: `scp ~/.openclaw/openclaw.json ユーザー名@162.43.90.71:~/.openclaw/`
- VPS で `openclaw.json` に OpenRouter API キー・Telegram の botToken が入っているか確認

**方法 B: VPS で onboard をやり直す**
- VPS で `openclaw onboard` を実行
- 画面の指示に従い、OpenRouter の API キー・Telegram のボットトークンなどを入力

### 5-2. VPS で設定を読み込ませて起動
- 設定を置いたら、いったん gateway を止める（Ctrl+C）
- 今度は **トークンだけ** 指定して起動（設定ファイルを読むため）:
```bash
openclaw gateway --token あなたのトークン
```
- `--allow-unconfigured` は付けない（設定済みのため）

### 5-3. Telegram で動作確認
- Telegram でボットにメッセージを送る
- 返信が返ってくれば OK  
- **409 Conflict** が出たら、Mac 側で OpenClaw が動いていないかもう一度確認

**Day 5 のゴール:** VPS の OpenClaw が OpenRouter と Telegram で動いていること

---

## 【Day 6】常時起動（オプション）

VPS からログアウトしても OpenClaw が止まらないようにする場合:

### 6-1. systemd でサービス化（Ubuntu の場合）
- サービス用の unit ファイルを作成し、`openclaw gateway --token あなたのトークン` をサービスとして登録
- 詳細は別途「OpenClaw systemd サービス化」で検索 or 依頼

### 6-2. または screen / tmux で起動したままにする
```bash
screen -S openclaw
openclaw gateway --token あなたのトークン
```
- **Ctrl+A → D** でデタッチ。再接続後は `screen -r openclaw` で復帰

**Day 6 のゴール:** 切断後も OpenClaw が動き続けること（どちらか一方でOK）

---

## 進捗チェックリスト（コピーして使う）

```
[ ] Day 1: バックアップ & VPS ログイン確認
[ ] Day 2: VPS で openclaw@latest インストール
[ ] Day 3: トークン付きで gateway 起動
[ ] Day 4: パケットフィルター設定 & ブラウザログイン
[ ] Day 5: OpenRouter・Telegram 設定反映 & 動作確認
[ ] Day 6: 常時起動（screen/systemd）
```

---

つまずいたステップがあれば、**その日の番号**と**出たエラーメッセージ**をメモして質問してください。
