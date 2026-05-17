# FLATUPGYM AI 使い方

最終更新: 2026-05-17

このメモは、JINが「何をどう頼めばいいか」で迷わないための説明書です。

## 一言でいうと

FLATUPGYM AIは、JINの分身として働く下書き・整理・改善アシスタントです。

ただし、最後に決めるのは必ずJINです。

## 最初に開く場所

Obsidianではここを開きます。

```text
00_CORE/FLATUPGYM_AI_HOME.md
```

パソコンでAIOSを動かす時はここへ移動します。

```bash
cd "/Users/jin/Desktop/OPENQLOW HelMES/flatup-ai-os"
```

使えるコマンドを見る:

```bash
npm run list
```

## 基本の頼み方

```bash
npm run dev -- コマンド名 "状況を書く"
```

例:

```bash
npm run dev -- line_reply "明日18時に体験できますか？女性で初心者です"
```

## よく使うコマンド

| やりたいこと | コマンド |
|---|---|
| LINE返信を作る | `npm run dev -- line_reply "問い合わせ文"` |
| 今日やることを整理する | `npm run dev -- daily_manager "今日の予定"` |
| 体験後フォローを作る | `npm run dev -- followup "体験者の様子"` |
| SNS投稿を作る | `npm run dev -- sns_post "投稿テーマ"` |
| X投稿案を作る | `npm run dev -- sns_post "X向け。短いスレッドにしたい内容"` |
| リスクを整理する | `npm run dev -- risk_check "匿名化した状況"` |
| 口コミ依頼文を作る | `npm run dev -- review_request "相手の状況"` |
| 動画台本を作る | `npm run dev -- video_script "動画テーマ"` |
| スタッフ用マニュアルを作る | `npm run dev -- training_manual "指導テーマ"` |
| HP/LPの差別化文を作る | `npm run dev -- differentiation "伝えたい強み"` |
| 初心者向け案内を作る | `npm run dev -- uizin "届けたい相手"` |

## コピペ例

### LINE返信

```bash
npm run dev -- line_reply "明日18時に体験できますか？女性で初心者です"
```

### SNS投稿

```bash
npm run dev -- sns_post "初心者歓迎の体験紹介投稿。怖くない雰囲気を伝えたい"
```

### X / Typefully用スレッド

```bash
npm run dev -- sns_post "X向け。弱い自分と戦う人へ届ける短いスレッド"
```

Typefully運用メモ:

```text
02_SKILLS_MARKETING/SNS/Typefully_X運用メモ_FLATUP.md
```

### 今日やること

```bash
npm run dev -- daily_manager "今日18時から体験3名。SNS投稿予定。月末請求準備あり"
```

### リスクチェック

```bash
npm run dev -- risk_check "会員さん同士の距離感で少し心配なことがある。個人名は書かずに状況だけ整理"
```

## Obsidianに残す時

| 内容 | 保存先 |
|---|---|
| AIの入口・憲法 | `00_CORE/` |
| 顧客対応・LINE返信 | `01_SKILLS_CUSTOMER/` |
| SNS・広告・動画 | `02_SKILLS_MARKETING/` |
| AIの振る舞いルール | `03_SKILLS_INTERNAL/` |
| JINのメモ・再開ログ | `4_日記/` |
| 古い資料 | `5_アーカイブ/` |
| システム・開発・GitHub運用 | `6_システム/` |
| 参考資料 | `99_REFERENCE/` |

## GitHubに残す時

基本の流れ:

```bash
cd "/Users/jin/Documents/Obsidian Vault"
git status --short
git add "変更したファイル"
git commit -m "docs: update flatup ai knowledge base"
git push origin main
```

AIに頼む時:

```text
この変更を確認して、秘密情報がないか見て、GitHubにpushして。
```

## やっていいこと

- 下書きを作る。
- メモを整理する。
- 使い方をわかりやすくする。
- 学習ログを書く。
- GitHubに変更履歴を残す。
- 次回のAIが迷わないようにリンクを整える。

## 勝手にやらないこと

- LINE送信。
- SNS公開。
- Typefullyの即時公開。
- 予約確定。
- 料金や営業時間の変更。
- APIキーや個人情報の記録。
- VPS本番反映。
- 本番サービス再起動。

## 迷った時の頼み方

```text
FLATUPGYM AI HOMEを読んで、今やるべきことを3つだけ出して。
```

```text
このメモをObsidianのどこに保存すべきか整理して。
```

```text
前回の続きから再開できるように、JIN_AI_RESUMEを更新して。
```

```text
今まで作った機能一覧を見て、足りないものを教えて。
```
