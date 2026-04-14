# OpenClaw 本番環境セットアップ（XServer VPS / Ubuntu）

Mac ではなく **XServer VPS（Ubuntu）** で OpenClaw を動かす手順です。

---

## ステップ1：古いプログラムの完全停止

VPS のコンソールで実行：

```bash
pkill -9 -f openclaw
```

---

## ステップ2：VPS の OpenClaw を最新版にする

```bash
npm install -g openclaw@latest
```

---

## ステップ3：VPS で OpenClaw を起動（トークン必須）

`my-pass123` は自分で決めたパスワードに変更してOK：

```bash
openclaw gateway --allow-unconfigured --token my-pass123
```

※ トークンは後でブラウザからログインするときに使います。

---

## ステップ4：XServer VPS のパケットフィルター設定（重要）

これをしないとブラウザから VPS にアクセスできません。

1. XServer VPS パネルにログイン
2. 左メニュー **「パケットフィルター設定」** をクリック
3. **「パケットフィルター設定を追加する」** で以下を追加：
   - **ポート番号:** 18789
   - **プロトコル:** TCP
   - **コメント:** OpenClaw用
4. 保存

---

## ステップ5：ブラウザからアクセス

Mac のブラウザで（IP はあなたの VPS のアドレスに置き換え）：

```
http://162.43.90.71:18789
```

ログイン画面で、ステップ3で決めたトークン（例: `my-pass123`）を入力。  
ダッシュボードが開けば成功です。

---

## 補足

- **Telegram で 409 Conflict が出る場合**  
  Mac 側で OpenClaw が動いていると競合します。Mac のターミナルで `openclaw gateway` を止め、**VPS だけ**で動かしてください（ボットは1箇所でしか動かせません）。

- **設定ファイルを VPS に合わせる**  
  Mac で編集した `openclaw.json` や `config.json` を VPS の `~/.openclaw/` にコピーするか、VPS で `openclaw onboard` を実行してから同じ内容（OpenRouter API キー・Telegram など）を設定してください。

---

まずは **ステップ1〜3** を VPS のコンソールで実行してみてください。
