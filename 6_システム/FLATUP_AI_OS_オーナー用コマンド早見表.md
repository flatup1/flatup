# FLATUP AI OS オーナー用コマンド早見表

本体:

```bash
cd "/Users/jin/Desktop/OPENQLOW HelMES/flatup-ai-os"
```

コマンド一覧:

```bash
npm run list
```

基本形:

```bash
npm run dev -- コマンド名 "状況を書く"
```

## よく使うコマンド

| やりたいこと | コマンド |
|---|---|
| LINE返信 | `npm run dev -- line_reply "問い合わせ文"` |
| 今日やること整理 | `npm run dev -- daily_manager "今日の予定"` |
| 体験後フォロー | `npm run dev -- followup "体験者の様子"` |
| SNS投稿 | `npm run dev -- sns_post "投稿テーマ"` |
| リスク整理 | `npm run dev -- risk_check "匿名化した状況"` |
| 口コミ依頼 | `npm run dev -- review_request "相手の状況"` |
| 動画台本 | `npm run dev -- video_script "動画テーマ"` |
| スタッフ用マニュアル | `npm run dev -- training_manual "指導テーマ"` |
| HP/LP差別化文 | `npm run dev -- differentiation "伝えたい強み"` |
| 初心者向け案内 | `npm run dev -- uizin "届けたい相手"` |

## コピペ用

```bash
npm run dev -- line_reply "明日18時に体験できますか？女性で初心者です"
```

```bash
npm run dev -- daily_manager "今日18:00から体験3名。SNS投稿予定。月末請求準備あり"
```

```bash
npm run dev -- followup "30代女性。初心者で不安そうだったが、ミット打ちは楽しそうだった"
```

```bash
npm run dev -- sns_post "初心者歓迎の体験紹介投稿。怖くない雰囲気を伝えたい"
```

```bash
npm run dev -- sns_post "X向け。弱い自分と戦う人へ届ける短いスレッド"
```

```bash
npm run dev -- risk_check "会員さん同士の距離感で少し心配なことがある。個人名は書かずに状況だけ整理"
```

```bash
npm run dev -- review_request "入会2ヶ月の男性。ミット打ちで自信がついた様子"
```

```bash
npm run dev -- video_script "体験トレーニングの流れを紹介する短い動画"
```

```bash
npm run dev -- training_manual "初心者へのミットの持ち方。怖がらせない声かけも入れる"
```

```bash
npm run dev -- differentiation "ガチスパー強制なし。初心者・女性・キッズが安心できるジム"
```

```bash
npm run dev -- uizin "格闘技未経験のお母さん向け。キッズクラスの安心感を伝える"
```

## 忘れないルール

- AIKAは下書き担当。送信・投稿は人間が確認してから。
- X投稿はTypefullyに下書き保存して、人間が確認してから公開・予約する。
- X投稿は1日5本まで。オリジナル比率70%以上。
- Typefully APIキーはObsidianやGitに書かない。
- 本名、電話番号、住所などの個人情報は入れない。
- 料金やルールが変わったら `src/data/` を直す。
- 不安な話はまず `risk_check`。
- 良かった下書きは `src/data/templates.md` に足す。

## 詳しい説明

リポジトリ側:

- `/Users/jin/Desktop/OPENQLOW HelMES/flatup-ai-os/docs/easy_start.md`
- `/Users/jin/Desktop/OPENQLOW HelMES/flatup-ai-os/docs/owner_commands.md`
- `/Users/jin/Desktop/OPENQLOW HelMES/flatup-ai-os/docs/typefully_x_ops.md`
- `/Users/jin/Documents/Obsidian Vault/02_SKILLS_MARKETING/SNS/Typefully_X運用メモ_FLATUP.md`
