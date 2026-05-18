# flatup-research-ai

FLATUP GYMの競合調査、口コミ傾向整理、広告ネタ作成、LINE配信文、Instagramリール台本をMarkdownレポートにまとめるNode.js CLIです。

このMVPは「確認・整理・下書き」専用です。送信、予約確定、請求変更、会員情報変更は実行しません。

## できること

- `data/keywords.json` の調査キーワードを読み込む
- `data/competitors.manual.json` に登録した公開URLを低頻度でFetchする
- 公開ページから料金、体験料金、キッズ訴求、女性訴求、初心者訴求の手がかりを抽出する
- 競合の強み、弱み、FLATUPの勝ち筋を整理する
- LINE配信用文章、Instagramリール台本、広告コピーを生成する
- `reports/YYYY-MM-DD_weekly_research.md` にMarkdownレポートを保存する

## できないこと

このツールは以下を自動実行しません。

- LINE送信
- メール送信
- 予約確定
- 予約変更
- 退会処理
- 休会処理
- 請求変更
- 会員情報変更
- 他社サイトの内部API利用
- 無断ログイン
- CAPTCHA回避
- 個人情報の保存

## 安全ルール

- 公開情報だけを扱う
- ログインが必要なページは扱わない
- 内部APIのリバースエンジニアリングはしない
- CAPTCHA回避はしない
- 高頻度アクセスはしない
- 不明な情報は推測せず「不明」と出す
- LINE文、広告文、投稿案は必ず人間が確認してから使う

人間確認が必要な処理では、以下の文言を使います。

```text
この内容で実行・送信してよろしいですか？
```

## セットアップ

```bash
npm install
cp .env.example .env
```

`.env` にAPIキーを直書きしないでください。`.env` はGit管理外です。

## 実行方法

```bash
npm run research
```

開発中は以下でも実行できます。

```bash
npm run dev
```

## レポート出力先

```text
reports/YYYY-MM-DD_weekly_research.md
```

## 競合URLの追加

`data/competitors.manual.json` に公開URLを追加します。

```json
[
  {
    "name": "競合ジム名",
    "url": "https://example.com",
    "area": "成田市",
    "category": "キックボクシング"
  }
]
```

初期状態は空配列です。URL未登録でも、マーケティング下書きと調査用レポートは生成されます。

## Browserbaseを使う場合の注意

Browserbaseは、動的ページで公開情報の確認が必要な場合だけ検討します。

```bash
npm install -g @browserbasehq/cli
```

このMVPでは、Browserbaseによるログイン、CAPTCHA回避、内部API解析、browser-to-api的な解析は実装していません。導入する場合も、公開ページの通常閲覧に限定してください。

## 今後の拡張案

1. Googleスプレッドシート出力
2. Gmail問い合わせ下書き生成
3. Googleカレンダー空き枠確認
4. LINE返信下書き生成
5. UIZIN大会運営チェックリスト生成
