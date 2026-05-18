# OPENQLOW / FLATUP GYM AI 引き継ぎ憲法

> このファイルは Jin の思想・確定要件・実装状態・運用規範を統合した正本です。
> 思想(§1-§11)、状態(§12-§13)、運用(§14-§17)を別レイヤーで読んでください。
> 最終更新: 2026-05-19

---

## §0. 用語集

| 用語 | 意味 |
|------|------|
| FLATUP GYM | 千葉県成田市の格闘技ジム。「世界一優しい格闘技ジム」 |
| AIKA | 既存 LINE Bot の人格(守りのAI) |
| FLATUP AI OS | AIKA を動かす TypeScript エンジン |
| OPENQLOW | 攻めのAI(本プロジェクトの新規実装) |
| 守りのAI | FLATUP 公式 LINE BOT(既存)。来た人を受ける |
| 攻めのAI | OPENQLOW。理念を外へ伝える(営業しない) |
| ClawX | OPENQLOW の土台ランタイム |
| MOLTBOT @817nsdhr | OPENQLOW 専用 LINE 公式アカウント(承認チャネル) |
| FG-ID | 投稿の人間可読ID。形式 `FG-YYYYMMDD-NNN` |
| 優しさスコア | 5軸 各0〜5点 計25点のブランド整合性スコア |
| 正本マップ | `6_システム/FLATUPGYM_AI_正本マップ.md`。Vault内の正本ファイル位置 |

---

## §1. プロジェクトを一文で

> **OPENQLOW は、FLATUP GYM の理念と空気を SNS に翻訳する攻めのAI。営業しない。Jin が LINE で承認したものだけ下書きにする。**

---

## §2. ジムの中心思想

> 世界一優しい格闘技ジム。
> 強い人を作るためではなく、弱い自分と向き合うための場所。

価値観:

- 怒鳴らない / 威圧しない
- 勝ち負けより、挑戦する勇気
- 初心者・女性・子ども・保護者が安心できる
- 強い人が偉い世界にしない
- 弱い自分でも、ここならいていいと思える空気

---

## §3. 攻めのAI(OPENQLOW)

**目的:** FLATUP の理念と空気を、SNS という外の世界に翻訳する。

**やる:** YouTube Shorts / Instagram / TikTok / Threads / X / SNS投稿企画 / 動画台本 / 字幕 / キャプション / 発信テーマ / 投稿候補 / 素材の見せ方 / ブランドの空気づくり。

**やらない:**

- 強引な営業 / DM営業
- 「体験に来てください」「LINE登録してください」「今だけ」「無料」「限定」
- コンプレックス煽り / 強さ自慢 / 根性論 / 怖い格闘技ジム感

**狙う読後感:**

> なんかこのジム、怖くなさそう。
> ここにいる人たち、幸せそう。
> 弱い自分でも、ここならいていい気がする。

---

## §4. 守りのAI(既存 FLATUP LINE BOT / AIKA)

**役割:** SNS を見て LINE に来た人を丁寧に受ける → 不安を減らす → 体験へ自然に誘導 → 必要なら人間に引き継ぐ。

**OPENQLOW(攻め)と LINE BOT(守り)は分離する。** チャネルも別のLINE公式アカウントを使う。

---

## §5. 全体構造と LINE 連携

```text
SNS / Shorts / Threads / TikTok / Instagram / YouTube
        ↓
[OPENQLOW] 理念翻訳 — 営業しない
        ↓
興味を持った人が自発的に LINE に来る
        ↓
[既存 FLATUP LINE BOT] 守りのAIが丁寧に受ける
        ↓
体験 / 見学 / 相談 へつなぐ
```

LINE は2チャネル:

| 用途 | アカウント | 触る人 |
|------|-----------|--------|
| 守り(顧客対応) | 既存 FLATUP 公式 LINE | お客さん |
| 攻め(承認チャネル) | **MOLTBOT @817nsdhr** | Jin だけ |

混ぜない。混ぜると顧客体験が壊れる。

---

## §6. 承認モデルと承認文法

**原則:** 安全領域は自動、危険領域は人間承認。**OPENQLOW は SNS に直接投稿しない。** 承認後も下書き保存まで。

**承認文法(MOLTBOT で Jin が打つ):**

| 返信 | 動作 |
|------|------|
| `OK FG-20260518-001` | 承認。X→Typefully、IG/Threads→ローカル+Vault下書き保存 |
| `修正 FG-20260518-001: コメント` | 再生成依頼 |
| `× FG-20260518-001` または `やめる FG-20260518-001` | 却下。ログだけ残す |

**LINE 通知の実物サンプル:**

```text
投稿候補です。
投稿ID: FG-20260518-001
目的: FLATUPの安全思想、初心者へのやさしさ、挑戦する勇気に接続する。
媒体: x / instagram / threads
公開レベル: Level 2: draft package
内容: 弱い自分と戦う人へ - 格闘技は相手を倒す前に、自分の不安と向き合う練習になる
優しさスコア: 24/25 (strong)
ひっかかる点: なし

--- X ---
弱い自分と戦う人へ

格闘技は相手を倒す前に、自分の不安と向き合う練習になる

強く見せるためじゃなく、今日の自分から逃げなかったことを静かに認める。
FLATUP GYM は、そういう一日がちゃんと残る場所です。
#FLATUPGYM #成田市 #格闘技

これ投稿する?
承認する場合: OK FG-20260518-001
修正する場合: 修正 FG-20260518-001: 直したい内容
やめる場合: やめる FG-20260518-001
```

---

## §7. やる / やらない

| 領域 | 方針 |
|------|------|
| 体験→予約ループ | **既存システムで完結。OPENQLOWは触らない** |
| X 下書き | Typefully `draft` のみ(schedule API は呼ばない) |
| Instagram 下書き | ローカル+Vault Markdown。公開は手動 |
| Threads 下書き | ローカル+Vault Markdown。公開は手動 |
| YouTube | 直接投稿しない。タイトル/概要/Shorts メタ下書きまで |
| 試合動画切り抜き | Phase 2 |
| MMA ネタ | 1日3ネタ、必ず FLATUP 価値観に接続 |
| TikTok / LINE VOOM | Phase 3 以降(BAN/規約リスク高) |
| 自動投稿 API 直叩き | **永久にやらない** |

---

## §8. リスク最小化(3層ガード)

| 層 | 内容 |
|----|------|
| ① 危ない行為をしない | 直接投稿API呼ばない。Typefully は draft のみ。IG/Threads はファイル保存 |
| ② 失敗前に確認する | 生成 → 自動安全チェック → LINE通知 → Jin承認 → 下書き保存 |
| ③ 壊れた時の被害最小化 | logs と Vault に二重記録。冪等。投稿IDで重複防止 |

---

## §9. ブランドルール(禁止 + 代替)

| 禁止 | 代わりに |
|------|---------|
| 「絶対痩せる」「必ず強くなる」 | 「今日来られた自分を、まず褒める」 |
| 「他のジムは最悪」 | 「FLATUP は怒鳴らない、威圧しない」 |
| 「ボコボコにする」「殴られないように」 | 「強さよりも先に、安心がある」 |
| 「ぽっこりお腹を解消」「だらしない体」 | 触れない。体型を題材にしない |
| 「本気の人だけ来い」「覚悟ある人だけ」 | 「初めての一歩を全力で待っています(と言わずに、空気で示す)」 |
| 「○ヶ月で-10kg」「Before/After」 | 個人の体型変化を素材にしない |
| 「努力不足」「甘えてる」 | 「弱い自分と向き合う日もある」 |
| 「ダサい」「情けない」「ひ弱」 | 弱さを題材にするが、嘲笑はしない |
| 「体験に来てください」「LINE登録お願いします」 | CTA を書かない。空気で誘う |

**良い例(X 用):**

```text
弱い自分と戦う人へ。
格闘技は相手を倒す前に、自分の不安と向き合う練習になる。
強く見せるためじゃなく、今日の自分から逃げなかったことを静かに認める。
FLATUP GYM は、そういう一日がちゃんと残る場所です。
```

**悪い例(直すべき):**

```text
キックボクシングで-10kg!成田で一番安い体験500円!今すぐ公式LINEへ!
本気の人だけ来てください。
```

---

## §10. 優しさスコア(自動採点)

| 軸 | 内容 | 範囲 |
|----|------|------|
| notScary | 怖く見えないか | 0〜5 |
| beginnerFriendly | 初心者が入りやすいか | 0〜5 |
| noShameOrPressure | 人を傷つけないか | 0〜5 |
| memberDignity | 会員の尊厳を守っているか | 0〜5 |
| flatupLike | FLATUP らしいか | 0〜5 |

| 合計 | 決定 | 動作 |
|------|------|------|
| 22-25 | strong | 承認候補として LINE 通知 |
| 18-21 | revise_lightly | 通知するが警告つき |
| 12-17 | revise_before_showing | block(再生成) |
| 〜11 | reject | block(別ネタへ) |

---

## §11. MMA ネタ方針

> 単なる格闘技ニュース速報にしない。必ず FLATUP 価値観に接続する。

接続軸:

- 初心者に何を伝えるか
- 女性に何を伝えるか
- 子ども・保護者に何を伝えるか
- FLATUP の安全思想にどうつながるか
- 挑戦する勇気にどうつながるか
- 「世界一優しい格闘技ジム」にどうつながるか

実装上は `ContentIdea.valueConnection` を必須化。

---

## §12. 実装済み(2026-05-19 時点 / コードで確認可能)

| カテゴリ | 実体 |
|---------|------|
| プロジェクト | `openqlow/`(TypeScript ES Modules、依存ゼロ運用) |
| 朝のオーケストレータ | `src/scheduler/daily.ts` の `runDaily / approveRecord / rejectRecord / requestRevision` |
| ネタ生成 | `src/generators/mma_topic.ts` / `daily_three.ts` |
| 媒体展開 | `src/distribution/expand.ts`(X/IG/Threads/LINE) |
| 安全チェック | `src/safety/check.ts`(12種のブランド違反検出 + 優しさスコア) |
| 承認文 | `src/approval/message.ts`(投稿IDつき、優しさスコア表示) |
| 投稿IDの採番 | `FG-YYYYMMDD-NNN`(連番) |
| 状態保存 | `state/<record-id>.json`(pending_approval / approved / rejected / needs_revision / saved) |
| ローカル下書き | `drafts/{x,instagram,threads}/` Markdown + index.jsonl |
| Vault ミラー | `src/adapters/vault_mirror.ts` → `6_システム/openqlow_drafts/` |
| Vault ログ | `src/adapters/vault_log.ts` → `6_システム/openqlow_logs/YYYY-MM-DD.md` |
| Vault レジスタ | `src/adapters/vault_register.ts`(approval event / draft save / performance placeholder) |
| 正本マップ | `src/sources/canon_map.ts`(`parseCanonMap / selectCanonReferences / resolveCanonPath`) |
| 生ネタ採用 | `src/sources/obsidian_inbox.ts`(`30_INBOX/openqlow/`) |
| ブランド知識 | `src/sources/brand_knowledge.ts`(`flatup-ai-os/src/data/`) |
| LINE 通知 | `src/line_bot/notifier.ts`(`pushLineMessage / pushApprovalNotification / pushAlert`) |
| LINE Webhook | `src/line_bot/webhook.ts`(OK / 修正 / × / やめる) |
| 死活監視 | `src/monitor/healthcheck.ts`(OpenRouter / LINE webhook / ngrok / launchd) |
| launchd | `daily` / `serve` / `monitor` の3 plist |
| CLI | `generate` / `approve` / `reject` / `revise` / `monitor` |

**環境設定(コード外で確認済み):**

- macOS sleep 抑止(`pmset -a sleep 0` 他、Amphetamine セッション稼働)
- MOLTBOT @817nsdhr: チャット ON / あいさつ OFF / Webhook ON / 応答時間内 = 手動チャット
- LINE Developers Messaging API: 応答メッセージ「無効」/ あいさつ「無効」

**動作確認コマンド:**

```bash
cd "/Users/jin/Desktop/OPENQLOW HelMES/openqlow"
npm run test                                                     # 全テスト通過
npm run daily                                                    # 3ネタ生成+Vaultログ+LINE通知
npm run dev -- approve FG-20260518-001 "OK FG-20260518-001"      # 承認+ミラー
npm run dev -- reject  FG-20260518-002 "今日は出さない"           # 却下
npm run dev -- revise  FG-20260518-003 "もっと初心者向けに"      # 再生成依頼
npm run monitor                                                  # 4チェック+異常時アラート
```

---

## §13. 未実装 / 次にやること

**A. Jin の手でやる(コード側は完成済み):**

1. LINE Developers の Webhook URL に OPENQLOW 公開URL(ngrok / Cloudflare Tunnel)を入れる
2. チャネルアクセストークン(長期)発行 → `.env` の `LINE_CHANNEL_ACCESS_TOKEN`
3. Jin の LINE userId → `.env` の `JIN_LINE_USER_ID`
4. launchd plist 3種を `~/Library/LaunchAgents/` にコピー+`launchctl load`

**B. 別セッションで(本番影響あり):**

- 守りのAI(既存 FLATUP LINE BOT)の応答方針プロンプト固定
- `line_webhook.py` / `closed_mode.py` 差分整理

**C. Phase 2:**

- 試合動画切り抜き(yt-dlp + ffmpeg + 区切り検出)
- 媒体別差別化(Shorts ≠ TikTok ≠ IG ≠ Threads)
- 素材管理台帳 + 使用許可

**D. Phase 3:**

- 反応分析(30投稿以降)
- Instagram Graph API
- TikTok / LINE VOOM
- ClawX 強化
- 改善ループ

---

## §14. 失敗モードと自動対応

| 失敗 | 検出 | 自動対応 | 人手 |
|------|------|---------|------|
| ngrok URL 変動 | `monitor` の ngrok チェック | LINE Alert で新URL通知 | LINE Developers の Webhook URL 更新 |
| OpenRouter 5xx | daily 実行時の例外 | 翌朝再試行(冪等) | 連続2日失敗で別モデルへ手動切替 |
| LINE Push 401 | notifier の戻り値 | ローカルログに残す | トークン再発行+`.env` 更新 |
| LINE webhook 落ち | `monitor` の line_webhook チェック | launchd KeepAlive で自動再起動 | 3回連続失敗で `serve.err.log` 確認 |
| launchd 未登録 | `monitor` の launchd チェック | LINE Alert で「未インストール」通知 | `scripts/install_launchd.sh` 実行 |
| Jin が3日承認しない | state の pending_approval が3日分 | 新しい朝の生成は止めない(冪等) | Jin が「却下まとめ」コマンドで一括処理 |
| 安全チェック block 連発 | safety.ok = false の連続 | 別角度で再生成 | プロンプト調整 or data/*.md 更新 |
| 優しさスコア低下傾向 | 7日移動平均が 18 未満 | LINE Alert で通知 | ブランド知識 / 生ネタを補強 |

---

## §15. 成功指標(SLA)

| 指標 | 目標 | 計測 |
|------|------|------|
| 毎朝3ネタ生成 | 7日連続 | Vault logs に 3 件/日 |
| 朝の承認所要時間 | 1分以内 | LINE タイムスタンプ差分 |
| 優しさスコア | 平均 18+ | Vault logs から集計 |
| 営業CTA混入 | 0 件 | safety logs の `salesy_cta` |
| 誤投稿 / BAN / 規約違反 | 0 件 | Jin の目視 |
| X フォロワー | +200 / 30日 | X analytics(参考) |
| 体験予約 | +5件 / 30日 | 既存システム(参考) |

---

## §16. 決定の根拠ログ(なぜそうしたか)

| 決定 | 理由 |
|------|------|
| 営業しない | Jin の明示指示「営業はしなくていい。よかったら来てくださいとか言わないでいい」 |
| X から開始 | Typefully API が既に接続済み・規約安全・MVPを最短で回せる |
| TikTok を後回し | BAN/規約変更リスク高、子ども・女性の映り込み懸念 |
| Mac 上で動かす | VPS 必要になるほどの規模ではない・Jin の手元で完結する |
| MOLTBOT を別アカウント | 既存 FLATUP LINE BOT(守り)と混ぜると顧客体験が壊れる |
| 投稿IDを `FG-YYYYMMDD-NNN` | 人間が打ちやすい・並び順で時系列が読める・冪等鍵 |
| Typefully は draft のみ | 直接公開のリスクを取らない・schedule API も意図的に呼ばない |
| Obsidian Vault 統合 | Jin の運用に馴染む・検索可能・横断資産化 |
| 優しさスコア導入 | ブランド毀損の自動検出・しきい値で運用可能 |

---

## §17. 次AIへの行動規範

**従う:**

- §1〜§11 の思想を変えない
- §9 の禁止リストを破らない(良い/悪い例で判定)
- §6 の承認文法を勝手に変えない
- §12 の実装済みを再実装しない(コードを読んで確かめる)
- §13 の優先順を守る(A → B → C → D)

**してはいけない:**

- 「営業」「キャンペーン」「フォロー必須」系のコピーを混ぜない
- 会員氏名・電話・メールを下書きに含めない
- Typefully の schedule API を呼ばない
- Jin の承認なしに公開系 API を叩かない
- `line_webhook.py` を勝手に編集しない(本番影響)
- 安全チェックを「迂回」しない(無視 / コメントアウト禁止)

**Jin が黙っている時:**

- 承認待ちは滞留してよい(冪等)
- 新しい朝の生成は止めない
- 異常を発見したら LINE Alert に流す
- 仕様変更を勝手にしない

**Jin が次に何をしたいか分からない時:**

- §13 の A(LINE 結線)が未完なら、まずそれを Jin に促す
- A が完了していれば、Phase 2 設計を提案する

---

## §18. コード配置

```text
/Users/jin/Desktop/OPENQLOW HelMES/
├── flatup-ai-os/             # 既存 AIKA(守り、触らない)
│   └── src/data/             # ブランド正本
└── openqlow/                 # 攻め(本プロジェクト)
    ├── src/
    │   ├── index.ts          # CLI: generate / approve / reject / revise / monitor
    │   ├── scheduler/        # runDaily
    │   ├── generators/       # 3ネタ + MMA角度
    │   ├── sources/          # inbox / brand / canon_map
    │   ├── distribution/     # 媒体展開
    │   ├── safety/           # 3層ガード + 優しさスコア
    │   ├── approval/         # LINE承認文
    │   ├── adapters/         # x_typefully / instagram_draft / threads_draft /
    │   │                       vault_log / vault_mirror / vault_register
    │   ├── state/            # JSONファイル状態
    │   ├── line_bot/         # webhook / notifier
    │   ├── monitor/          # healthcheck
    │   └── utils/
    ├── drafts/ logs/ state/
    └── launchd/              # 3 plist
```

---

## §19. 最終定義

**OPENQLOW とは:**

> FLATUP GYM の理念と空気を、SNS という外の世界に翻訳する AI。
> 営業しない。押し売りしない。怖くしない。弱さを笑わない。会員を素材扱いしない。
> ただ、最高に楽しくて優しくて、通っているみんなが幸せそうなジムの姿を考え抜いて発信する。

**最終目標:**

> 「世界一優しい格闘技ジム」という思想が、SNS 上で自然に伝わる状態を作る。
> 営業臭くなく、押し売りせず、見た人が「ここ、なんかいいな」と感じる発信を、継続的に、自動で、生み出す。
