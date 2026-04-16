# 【FLATUP AI OS】完全引き継ぎドキュメント
## 対話式・論理構造版

---

## 🎯 序論：あなたが引き継ぐミッション

**JIN（松元仁志）は何を実現したいのか？**

```
「自分の脳（知識・思想・経営ノウハウ・マーケティング戦略）をAIに完全外部化し、
　24時間自動稼働する『第2の松元仁志』を創造する。
　
　その実体は、ジムのオーナー兼店長『AIKA』というAIペルソナであり、
　LINE・SNS・営業・イベント企画・広告戦略まで、
　すべての顧客接点で JIN の思想を自動展開する『経営OS』である。」
```

**つまり、あなたのタスクは：**
- 単なる「LINE チャットボット」構築ではない
- 単なる「FAQ 自動応答」ではない
- **JINの思想そのものをデジタル化し、24時間体制で全ビジネス活動を自動実行するAIシステム**の完成

---

## 📐 第1章：FLATUP GYMの本質（理念層）

### Q1: FLATUP GYMとは何か？

**A: ジムの定義**
```
会社名：FLATUP GYM
所在地：千葉県成田市
経営者：松元仁志（JIN）
事業形態：個人事業主

【コンセプト】
「世界一やさしい格闘技ジム」

【ターゲット】
- 初心者（経験ゼロ）
- 女性（強化・体力向上目的）
- キッズ（3歳〜中学生）
- シニア（50代以上）

【否定する対象】
- 格闘技の「強そう」「怖い」イメージ
- 「ついていけない」という挫折感
- 性別・年齢による制限
```

### Q2: FLATUP GYMの指導哲学（FLATUPメソッド）は？

**A: 3つの原則**
```
1. 否定しない
   → 「できない」ではなく「今はそういう段階」
   → 初心者の失敗を指摘しない文化

2. 小さな成功を作る
   → 週1回で楽しさを感じる設計
   → 「続ける理由」を毎回提供

3. 必ず褒める
   → どんな小さな工夫にも言及
   → 自己肯定感の醸成
```

### Q3: 現在のスタッフ構成は？

**A: インストラクター4名**
```
1. AIKA（女性オーナー）→ ジムのAIペルソナのベースキャラ
2. HITOSHI
3. MIICHI
4. MASAKI
```

---

## 🧠 第2章：FLATUP AI OSの全体アーキテクチャ（システム層）

### Q4: なぜ「AI OS」が必要か？

**A: JINが直面する問題と解決戦略**
```
【問題】
- オーナー1人で営業・マーケティング・SNS・LINE対応をやっている
- 手動作業が増えるたびに時間が奪われ、本来のジム運営（指導）に集中できない
- スケーリングできない（時間の壁）

【解決方法】
→ AIが「営業・マーケティング・顧客対応」の99%を自動化
→ JINは「戦略・新しいコンセプト立案・顧客体験設計」だけに集中
→ 結果：24時間体制の営業活動 + JINの人間にしかできない仕事の融合
```

### Q5: FLATUP AI OSの3層構造は何か？

**A: 知識 → エンジン → インターフェース**

```
【第1層】MASTER BRAIN（知識・思想層）
  ツール：Obsidian
  役割：JINの脳そのもの。すべての意思決定・ノウハウ・思想の原典
  
  フォルダ構造：
  00_CORE/              ← 理念・ミッション・ブランドコア
  01_PHILOSOPHY/        ← AIKAペルソナ設定・AIの行動規範
  02_GYM_SYSTEM/        ← 料金・クラス・スケジュール・大会情報
  03_MARKETING/         ← 営業戦略・SNS戦略・広告
  04_CONTENT/           ← TikTok・Instagram・YouTube素材
  05_EVENTS/            ← イベント企画・大会企画
  06_AI/                ← AI実装ノート（Dify・AnythingLLM設定）
  07_DAILY_LOG/         ← 日々の更新・試行錯誤の記録

【第2層】AI ENGINE（処理・判断層）
  ツール：Ollama + AnythingLLM
  役割：Obsidianをベクトル化（RAG）し、知識を AI の脳に吸収
  
  詳細：
  - Ollama：MacBook Pro (M2, 8GB) で駆動する軽量 LLM エンジン
  - モデル：Gemma 2 27B（量子化版）/ Qwen 2.5 32B（検討中）
  - AnythingLLM：Obsidian Vault をベクトルDB（Qdrant）に同期
    → 「FLATUP_BRAIN ドキュメント」を AI が常に参照可能な状態に
  - テスト中：OpenRouter 経由で Mistral 7B も並用（重要な判断は Claude 併用）

【第3層】APP INTERFACE（接点層）
  ツール A：Dify + Exbrain
  役割：LINE・SNS・営業メール・自動提案をAIが実行
  
  具体的フロー：
  1. LINE ユーザーからメッセージ受信
  2. Dify が LINE Messaging API で捕捉
  3. AnythingLLM (Obsidian 知識) から最新情報取得
  4. Claude / Mistral が「AIKAらしい返信」を生成
  5. LINE に自動投稿
  
  ツール B：Exbrain（魔改造版）
  役割：AIが自主的に「提案・営業・SNS投稿」を行う自律エージェント化
  
  コンセプト：SOUL / MEMORY / DREAMS サイクル
  - SOUL.md：AIKAの人格・判断ルール・倫理観
  - MEMORY：過去の対話・顧客情報・施策結果
  - DREAMS：「次に提案すべき営業施策」をAIが自動立案
```

### Q6: データの自動同期フローは？

**A: 「編集すれば自動で全システムが賢くなる」パイプライン**

```
【理想的なフロー】
Mac (JIN が Obsidian で編集)
  ↓ (自動 push)
GitHub (flatup1/flatup リポジトリ)
  ↓ (cron で定期 sync)
VPS (Xserver, IP: 162.43.90.71)
  ↓ (AnythingLLM インデックス更新)
Dify (Knowledge Store 更新)
  ↓ (API 経由)
LINE BOT (AIKA が最新情報で返信)
  ↓
顧客に到着

【スピード】
- JIN が Obsidian で「体験料金を 5000 円→3000 円に変更」と書く
- 最短 10 分以内に LINE の自動返信が新料金を反映

【現在の実装状況】
- Obsidian ローカル保存：完了 ✓
- GitHub リポジトリ：完了 ✓
- VPS Docker (AnythingLLM port 3001)：構築済 ✓
- VPS + Dify の API 連携：進行中 🔄
- 自動同期スクリプト（cron）：次のフェーズ ⏳
```

---

## 🔧 第3章：技術仕様・具体的な実装（技術層）

### Q7: 開発環境は？

**A: Mac 完結（最小工数）**
```
【ハードウェア】
- MacBook Pro M2 (8GB メモリ)
- Node.js v24（NVM で管理）

【開発ツール】
- Obsidian：ローカル知識管理
- Git / GitHub：バージョン管理・同期ハブ
- VS Code / Claude Code：コーディング支援

【クラウド / 外部サービス】
- Xserver VPS (Linux, 162.43.90.71)：本番エンジン
- Dify Cloud (cloud.dify.ai)：LINE BOT 本体
- OpenRouter：API 経由で LLM を利用（Mistral・Claude）
- LINE Messaging API：LINE 連携
```

### Q8: VPS上で稼働しているシステムは？

**A: Docker で 2 つのサービス**
```
【1】AnythingLLM (port 3001)
  役割：Obsidian Vault → ベクトル化 → RAG エンジン
  
  構成：
  - Qdrant（ベクトルDB）を内蔵
  - 現在 27 件のObsidian ドキュメントをインデックス済み
  - LLM バックエンド：Ollama（ローカル）/ OpenRouter（クラウド）
  
  操作方法：
  - Mac から SSH → VPS
  - docker-compose up（再起動）
  - http://162.43.90.71:3001 でアクセス（Cloudflare トンネルで HTTPS 化予定）

【2】Dify（現在は cloud.dify.ai で運用）
  役割：LINE BOT のオーケストレーター
  
  構成：
  - LINE Messaging API と連携済み
  - Knowledge Store（Dify 内部）に情報を保存
  - Workflow：ユーザーメッセージ受信 → LLM 処理 → LINE 返信
  
  予定：VPS 自社ホスト版への移行も検討中
```

### Q9: LINE BOT の現在の動作仕様は？

**A: AIKAペルソナで返信するシステム**
```
【ペルソナ設定】
- 名前：AIKA
- 性別：女性
- 性格：知的・余裕がある・親切
- 強み：女性や初心者に優しい対応
- 毅然とした態度：不潔な男性には明確に拒絶
- トーン：敬語と親しみのバランス

【返信の流れ】
1. ユーザーが LINE で「体験レッスンの料金は？」と聞く
2. LINE Messaging API が Dify に転送
3. Dify が AnythingLLM に「料金情報をゲット」と依頼
4. AnythingLLM が Obsidian の「02_GYM_SYSTEM/料金.md」から取得
5. Dify が Claude/Mistral に「AIKAらしく返信を生成」と指示
6. 「体験レッスンは 500 円です。女性・初心者・キッズ大歓迎！」と LINE に返信

【テンプレート状況】
- LINE テンプレート（日付なし・クラス別）：10 種類整備済み
- 毎週更新可能（Obsidian で編集 → 自動反映）
```

### Q10: Exbrain とは何か？

**A: 茶圓氏のリポジトリをベースにした「AI 自律エージェント化プロジェクト」**

```
【概要】
https://github.com/chaenmasahiro0425/exbrain
→ Mac にローカルクローン済み

【Exbrain の役割】
単なる「返信ボット」ではなく、AI が自主的に：
- 営業提案を立案
- SNS 投稿を生成
- DM を自動送信
- 大会企画を提案

→ 「AI が経営者になる」レベルの自律性

【3 つのサイクル】
1. SOUL.md
   - AIKAの人格定義（知的・女性優先・毅然）
   - 判断ルール（誰に営業する？何を提案する？）
   - 倫理観（やってはいけないこと）

2. MEMORY
   - 過去 30 日間の顧客対話ログ
   - LINE・DM・メール全履歴
   - 顧客の属性・購買履歴

3. DREAMS（自動立案モジュール）
   - 「次の営業ターゲット」を自動選定
   - 「提案内容」を自動生成
   - 「SNS 投稿ネタ」を自動抽出
   → n8n（自動化エンジン）で実行

【現在の実装状況】
- git clone 済み：✓
- SOUL.md の 初期版：未着手
- MEMORY サイクル実装：未着手
- DREAMS の自動立案：未着手
```

### Q11: 使用している LLM は？

**A: 複数モデルの使い分け**

```
【メイン】
- Mistral 7B（OpenRouter 経由）
  理由：軽量・日本語対応OK・コスト安
  用途：日常的な LINE 返信・SNS 生成

【重要判断用】
- Claude 3.5 Sonnet（OpenRouter 経由）
  理由：思考力が必要な営業提案・戦略立案
  用途：「どの顧客に何を売るか」の判断

【ローカル環境】
- Gemma 2 27B（Ollama）
  導入済み
  用途：プライベートな判断・テスト運用

【検討中】
- Qwen 2.5 32B（量子化版）
  理由：マルチランガル・軽量
```

### Q12: API キーの管理は？

**A: OpenRouter / Dify 経由**

```
【OpenRouter】
- API キー：保有済
- 月額：従量課金（数千円程度目安）
- 複数モデルを 1 つのキーで利用可能

【Gmail（将来の計画）】
- Gmail MCP 統合を予定
- OAuth 2.0 で認証
- 使用アカウント：yuusannoai0528@gmail.com
- 目的：メール自動返信・営業メール自動生成

【LINE Messaging API】
- 連携済み
- チャネルアクセストークン設定済み

【GitHub】
- SSH キー設定済み（VPS から push/pull 可能）
```

---

## 📱 第4章：マーケティング・営業の自動化（運用層）

### Q13: SNS 戦略（TikTok・Instagram）は？

**A: Exbrain との連携で自動投稿**

```
【TikTok】
- 現在のステータス：Shop 承認取得済み
- 投稿時間帯：19:00 〜 22:00（ゴールデンタイム）
- コンテンツ戦略：
  * AIKA（インストラクター）のテクニック動画
  * 体験者のビフォーアフター
  * リフレックスボール・格闘技体験
  
- 動画制作：CapCut AI を活用
  * 自動字幕・効果音・テンプレート
  * 週 2 〜 3 本の投稿ペース

- ローカルハッシュタグ：#成田格闘技ジム #Narita #初心者歓迎

【Instagram】
- ショップ機能：Japan では「在庫チェックアウト」未対応
  → 外部 EC へのリダイレクト構成
- コンテンツ：リール・ストーリーズ・フィード
- 自動化：Exbrain から毎日 1 〜 2 本投稿

【次のフェーズ】
- Exbrain が「今日の投稿ネタ」を自動立案
- Claude がキャプション・ハッシュタグを生成
- n8n が TikTok・Instagram API に自動投稿
```

### Q14: 「OpenClaw」自動営業システムとは？

**A: アウトバウンド営業の完全自動化**

```
【コンセプト】
Google Maps・Twitter・Instagram から「見込み客」を自動抽出
→ DM・メール を自動生成・自動送信
→ 営業成約まで自動フロー

【フロー】
1. データ取得フェーズ
   - Google Maps：成田市内で「格闘技」「フィットネス」のクエリで検索
   - Twitter：#成田 #初心者向け などで見込み客検出
   - Instagram：フォロワー 100 〜 1000 人の地域インフルエンサー抽出

2. AI 営業メール生成フェーズ
   - 相手のプロフィール分析
   - 「このユーザーなら『女性向けキッズクラス』が刺さるな」と判定
   - 個別カスタマイズされた営業 DM 自動生成

3. 自動送信フェーズ
   - n8n で定期実行（1 日 20 件程度、スパム回避）
   - Twitter・Instagram DM・Gmail で送信
   - 返信があれば LINE 連携

【現在の状況】
- 設計フェーズ：完了 ✓
- 実装フェーズ：次 ⏳
```

### Q15: LINE 販売・診断システムは？

**A: 顧客プロファイリング + パーソナライズ提案**

```
【フロー】
1. 初回接触
   - ユーザーが LINE で「体験したい」と入力

2. 診断フェーズ（自動）
   - 「年齢は？」「目的は？」「経験は？」
   - 10 問の自動質問（テンプレート化）
   - 回答から顧客属性を自動判定

3. プロファイリング（AI が実行）
   - 「30 代女性・初心者・ストレス解消目的」と分類
   - Obsidian の顧客セグメント情報をマッチング

4. パーソナライズ提案（自動生成）
   - 「あなたなら『女性向けキックボクシング体験』がおすすめ！」
   - 体験料金・日程・持ち物を自動提示
   - LINE 決済で予約完了

【現在の状況】
- LINE テンプレート（診断用）：設計中 🔄
- 自動判定ロジック：設計中 🔄
```

### Q16: 大会戦略は？

**A: 「小さな成功」の連続供給**

```
【大会の役割】
- ジムメンバー向けの「目標設定」の場
- 初心者が「達成感」を感じるイベント
- SNS 投稿コンテンツの宝庫

【現在の実施状況】
- 月 1 回程度の内部大会
- 女性・キッズ向けのエキシビション
- 不潔な男性を排除（AIKAメソッド）

【AI による自動化】
- 大会日程を Obsidian で管理
- LINE で参加者に自動通知
- 結果を SNS で自動投稿
- 動画を CapCut AI で自動編集
```

---

## 🎬 第5章：現在の実装進捗と残タスク

### Q17: 何が完成しているのか？

**A: インフラとプロトタイプ**

```
✅ 【完了】
1. Obsidian ローカル保存
   - フォルダ構造完成（00_CORE ～ 07_DAILY_LOG）
   - ブランドコアドキュメント完成
   - 基本ノート（体験料金修正含む）

2. GitHub リポジトリ
   - flatup1/flatup 作成済み
   - ローカル push・pull 動作確認済み

3. VPS 環境（Xserver）
   - ドメイン：flatupnarita.jp（ホスティング済み）
   - AnythingLLM Docker：port 3001 で稼働
   - Obsidian ドキュメント 27 件をインデックス済み
   - OpenRouter API キー認証完了（Unicode エラー解決済み）

4. Dify 連携
   - Dify Cloud で LINE BOT 基本構成済み
   - Knowledge Store に初期データ入力
   - テンプレート（日付なし・クラス別 10 種）整備済み

5. LINE 公式アカウント
   - @jfl0054o（連携済み）
   - AIKA ペルソナでテスト返信成功

6. Claude Code の遠隔制御
   - Mac（NVM / Node v24）での起動成功
   - Tailscale IP（100.72.211.24）経由の iPhone アクセス確認
   - セッション再起動時のキャッシュクリア手順確立

7. TikTok 関連
   - Shop 承認取得済み
   - CapCut AI 活用体制構築
```

### Q18: 何が未完成か？

**A: 自動化・自律化フェーズ**

```
⏳ 【進行中 / 未着手】

【短期（1 〜 2 週間）】
1. Exbrain 魔改造
   - SOUL.md のリライト（AIKAペルソナ完全定義）
   - MEMORY サイクル実装
   - DREAMS（自動立案モジュール）

2. VPS Cloudflare トンネル化
   - HTTPS 化（セキュリティ強化）
   - 外部からの安全なアクセス

3. Gmail MCP 統合
   - OAuth 2.0 認証（yuusannoai0528@gmail.com）
   - メール自動返信スクリプト

【中期（1 ヶ月）】
4. LINE 診断・販売システム
   - テンプレート完成化
   - 自動判定ロジック実装

5. 自動同期パイプライン（cron）
   - Obsidian → GitHub → VPS → Dify の完全自動化
   - 更新間隔：30 分ごと

【長期（3 ヶ月）】
6. OpenClaw（アウトバウンド自動営業）
   - リード取得スクリプト
   - AI 営業メール生成・自動送信

7. マーケティング AI の自律提案
   - 広告戦略の自動立案
   - SNS コンテンツ企画の自動生成
```

---

## 🧬 第6章：AI化の思想・こだわり（マインド層）

### Q19: なぜこんなに AI に拘るのか？

**A: JINのビジネス哲学**

```
【問題認識】
- 時間は有限：オーナーが営業・マーケティングに時間を使う = ジムの質が低下
- 人手不足：アルバイトに任せられない判断が多い
- スケーリング不可：24 時間営業できない

【解決方法】
- AI を使って「営業・マーケティング・顧客対応」を完全自動化
- 人間（JIN）は「戦略・ビジョン・商品企画」に専念
- 結果：時間 × クオリティの両立

【最終形態】
「自分専用の AI OS」→ クリック 1 つで「今月の営業戦略」が自動立案・実行される
```

### Q20: ツール選定の原則は？

**A: 3 つのルール**

```
1. 最小工数・最短ルート
   - 不要なツール増やさない
   - Mac 1 台で完結
   - API で既存ツール連携（新サービス導入は最小限）

2. 低コスト優先
   - 無料・OSS・最小ランニングコスト
   - OpenRouter：月数千円で複数モデル利用可能
   - AnythingLLM・Dify・n8n：すべて OSS

3. 思想優先
   - ツールは手段
   - 「世界一やさしいジム」という哲学を表現できるか？
   - AIKAペルソナが「女性・初心者・キッズを守る」ことができるか？
```

### Q21: Exbrain への期待は？

**A: 「AIが経営者になる」ための枠組み**

```
【Exbrain が必要な理由】
- Dify：「受動的」（LINE メッセージ受信 → 返信）
- Exbrain：「能動的」（AI が自主的に営業提案・施策立案）

【理想的な Exbrain の動き】
1. 朝 9 時：MEMORY から「この顧客は 30 日間連絡なし」を検出
2. AI が判断：「そろそろ体験レッスン誘導を送るべきか」
3. SOUL.md をチェック：「この顧客は女性初心者か」
4. DREAMS が施策立案：「キッズ向け体験キャンペーン」の DM を生成
5. n8n で実行：自動送信
6. 返信があったら LINE で対応

【JIN が手作業する部分】
- なし（0%）
- ただし Obsidian で「方針変更」を書き込めば、AI が自動で反応

【SOUL.md の重要性】
- ここが「AIKAの人格」の源泉
- ここが「判断ルール」の基準
- ここが変われば、すべての AI 動作が変わる
```

### Q22: 「不潔な男性への毅然とした態度」とは？

**A: FLATUP メソッドの実装例**

```
【AIKAの判断基準】
- 言葉遣いが下品
- 女性メンバーへの接触が不適切
- ジムの雰囲気を壊す言動

【取るべき行動】
1. 1 回目：「こういった言動は NG です」と明確に伝える
2. 2 回目：「残念ですが継続は難しいです」と退会案内

【SOUL.md での定義】
```
IF: ユーザーの言葉遣い == 下品 OR 女性蔑視
THEN: 
  response = "申し訳ありませんが、当ジムはそのような言動を認めていません。"
  action = "退会案内"
```

【AIKAのトーン】
- 親切だが毅然とした態度
- 説教ではなく「ルール説明」
- 女性・初心者を守る姿勢を貫く
```

### Q23: クラウドか自社ホストか？

**A: ハイブリッド構成**

```
【今の状態】
- Mac（ローカル）：Obsidian + 開発環境
- GitHub：バージョン管理・同期ハブ
- VPS（Xserver）：AnythingLLM + 自動同期スクリプト
- クラウド：Dify Cloud + OpenRouter

【将来の構想】
- Dify を VPS 自社ホスト版に移行（コスト削減・プライバシー強化）
- すべての AI エンジンを VPS に統一
- Mac は「編集ツール」に専念

【メリット】
- 顧客データが完全に自分の手に
- API コスト削減
- VPS スペックさえあれば 24 時間自動稼働
```

---

## 🚀 第7章：次のアクション（タスクリスト）

### Q24: 今すぐ着手すべきことは？

**A: 優先度順**

```
【🔴 超優先（本週中）】

1. Exbrain SOUL.md 完全リライト
   役割：AIKAペルソナの「思考ロジック」を固定化
   内容：
   - 人格定義（知的・親切・毅然）
   - 判断ルール 30 個（誰に何を営業？何は NG？）
   - 倫理観・タブー
   
   成果物：SOUL.md（500 〜 1000 行の完全版）
   所要時間：4 〜 6 時間

2. Exbrain MEMORY サイクル実装
   役割：LINE・DM の履歴を AI の「記憶」に変換
   内容：
   - 過去 30 日の顧客対話ログを JSON 形式で抽出
   - 顧客セグメント（性別・年齢・目的・購買履歴）を自動判定
   - 「次の営業タイミング」を推定
   
   成果物：memory.json（構造化された顧客データベース）
   所要時間：3 〜 4 時間

【🟠 優先（1 週間以内）】

3. VPS Cloudflare トンネル化
   役割：VPS を安全に外部公開
   内容：
   - cloudflared インストール
   - AnythingLLM port 3001 → HTTPS 化
   - DNS 設定（flatupnarita.jp）
   
   所要時間：1 時間

4. 自動同期スクリプト（cron）実装
   役割：Obsidian の更新を VPS に自動反映
   内容：
   - GitHub Actions または VPS cron ジョブ
   - 30 分ごとに git pull + AnythingLLM インデックス更新
   - エラーハンドリング
   
   所要時間：2 〜 3 時間

【🟡 中期（2 週間以内）】

5. LINE 診断・販売システム実装
   役割：初回顧客を自動分類・提案
   内容：
   - 診断フロー設計（10 問のテンプレート）
   - 自動判定ロジック実装（Dify Workflow）
   - 提案メッセージ自動生成
   
   所要時間：4 〜 5 時間

6. Gmail MCP 統合
   役割：メール自動返信・営業メール自動生成
   内容：
   - OAuth 2.0 認証（yuusannoai0528@gmail.com）
   - Dify または Claude Code から Gmail API 経由でメール作成
   - 署名・フォーマット自動化
   
   所要時間：2 〜 3 時間

【🟢 長期（1 ヶ月）】

7. OpenClaw 実装（アウトバウンド自動営業）
   役割：Google Maps・Twitter から見込み客に自動 DM
   内容：
   - リード取得スクリプト（Web スクレイピング / API）
   - AI 営業メール自動生成（相手の属性に合わせたカスタマイズ）
   - n8n で自動送信（スパム回避のスロットリング）
   
   所要時間：8 〜 10 時間

8. 統計ダッシュボード（自動レポート）
   役割：AI 施策の効果を可視化
   内容：
   - 月別成約数・顧客属性分布
   - SNS リーチ数・エンゲージメント
   - OpenClaw の転換率
   
   所要時間：3 〜 4 時間
```

### Q25: Exbrain 魔改造の具体的な進め方は？

**A: Step by Step**

```
【Step 1】SOUL.md 作成（最優先）
ファイル：Exbrain/SOUL.md
内容テンプレート：

---
# AIKA の SOUL

## 1. 人格プロフィール
- 名前：AIKA
- 年齢：28 歳（設定値）
- 性別：女性
- 職種：格闘技ジム店長・インストラクター
- 性格キーワード：知的・親切・毅然・余裕・母性
- 専門知識：格闘技・フィットネス・女性トレーニング・キッズ教育

## 2. 判断ルール（IF-THEN）
### Rule 1: 初心者対応
IF: ユーザーが「できるか不安」と言及
THEN: 
  - 「みんなそこから始まります」と励ます
  - FLATUPメソッド（否定しない・小さな成功・褒める）を実行
  - 体験日時を提示

### Rule 2: 女性向けキャンペーン
IF: ユーザーが女性 AND 購買意思なし
THEN:
  - 「女性限定キャンペーン」を提案
  - 「女性インストラクターAIKA が直接指導」を強調
  - 安心要素を 3 つ以上記載

### Rule 3: 不適切な言動への対応
IF: ユーザーの言葉 == 下品 OR 女性蔑視
THEN:
  - response = "申し訳ありませんが、当ジムはそのような言動を認めていません。"
  - action = "警告" (初回) / "退会案内" (2 回目)

[以下、30 個のルールを同様に記述]

## 3. タブー（やってはいけないこと）
- 顧客の否定
- 強引な営業
- 安全軽視
- 女性蔑視
- プライバシー侵害

## 4. こだわり（大切にすること）
- 「小さな成功」を毎回作る
- 顧客の self-efficacy（自己効力感）を高める
- 安全第一
- 楽しさを優先
---

【Step 2】MEMORY 実装
ファイル：Exbrain/memory.json
内容テンプレート：

{
  "customers": [
    {
      "user_id": "USER_001",
      "name": "田中花子",
      "attributes": {
        "gender": "female",
        "age": 32,
        "goal": "ストレス解消",
        "experience": "初心者",
        "joined_date": "2024-01-15",
        "last_contact": "2024-04-10"
      },
      "purchase_history": [
        { "date": "2024-01-20", "item": "体験レッスン", "price": 500 }
      ],
      "conversation_log": [
        { "date": "2024-04-10", "message": "レッスン楽しかった！", "sentiment": "positive" }
      ],
      "next_action": {
        "recommendation": "キックボクシング月額コース",
        "timing": "5 日以内",
        "reason": "30 日連絡なし・前回好評"
      }
    }
  ]
}

【Step 3】DREAMS 実装
ファイル：Exbrain/dreams.js
概念：
- MEMORY から「営業すべき顧客」を自動抽出
- SOUL.md の「ルール」に基づいて施策を立案
- n8n で LINE・DM 送信を実行

例：
```javascript
function generateCampaign() {
  const customers = loadMemory();
  const campaigns = [];
  
  for (const customer of customers) {
    if (customer.days_since_contact > 30 && customer.sentiment === "positive") {
      campaigns.push({
        customer_id: customer.user_id,
        message: generatePersonalizedMessage(customer),
        channel: "LINE",
        timing: "09:00", // 朝 9 時
      });
    }
  }
  
  return campaigns;
}
```
```

### Q26: 同期パイプラインの具体的な実装は？

**A: スクリプトと cron ジョブ**

```
【構造】

Mac (Obsidian)
  └─ JIN が編集
     └─ Cmd+S で自動保存
        └─ git add . && git commit && git push
           └─ GitHub に push

GitHub (flatup1/flatup)
  └─ main ブランチ更新
     └─ Webhook トリガー or cron

VPS (Xserver, 162.43.90.71)
  └─ /opt/flatup/FLATUP_BRAIN
     └─ git pull (30 分ごと)
        └─ AnythingLLM インデックス更新
           └─ Dify Knowledge Store 同期

【実装の詳細】

## VPS 上のスクリプト：sync.sh

#!/bin/bash

# リポジトリディレクトリ
REPO_DIR="/opt/flatup/FLATUP_BRAIN"
ANYTHINGLLM_API="http://localhost:3001/api"

# Step 1: Git 同期
cd $REPO_DIR
git pull origin main

# Step 2: Obsidian ドキュメントをベクトル化
curl -X POST "$ANYTHINGLLM_API/v1/document/workspace/update" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace": "flatup",
    "vectorize": true,
    "documents": "'$REPO_DIR'/docs/**/*.md"
  }'

# Step 3: Dify Knowledge Store に同期
curl -X POST "https://cloud.dify.ai/api/knowledge-bases/update" \
  -H "Authorization: Bearer YOUR_DIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "local_obsidian",
    "path": "'$REPO_DIR'/02_GYM_SYSTEM/**/*.md"
  }'

# Step 4: ログ出力
echo "$(date): Sync completed" >> /var/log/flatup_sync.log

## cron ジョブ設定

# VPS 上で：
crontab -e

# 以下を追加：
*/30 * * * * /opt/flatup/sync.sh >> /var/log/flatup_cron.log 2>&1

→ 30 分ごとに自動同期

【テスト方法】
1. Mac の Obsidian で「体験料金」を 5000 円→3000 円に変更
2. Git で commit
3. VPS で「git pull」を実行（またはcron待機）
4. AnythingLLM port 3001 でインデックス更新を確認
5. LINE で「体験料金は？」と聞く
6. 新料金（3000 円）が返信されることを確認 ✓
```

---

## 🎓 第8章：まとめと哲学

### Q27: なぜこのシステムが必要なのか？（最終的な理由）

**A: 時間 × クオリティのジレンマの解決**

```
【従来のジム経営の問題】
営業・マーケティング時間 ↑
→ ジムの質・顧客体験 ↓

JIN の時間は有限：
- オーナー業務：営業・SNS・LINE対応
- インストラクター業務：指導・カリキュラム開発
- 両立は不可能

【FLATUP AI OS による解決】
営業・マーケティング = AI が自動実行
→ JIN は「戦略立案・商品企画・顧客体験設計」に専念
→ 時間 AND クオリティが両立

【最終的な理想形】
JIN が月 1 回 Obsidian で「戦略」を書き込む
  ↓
AI が自動で営業・マーケティング・顧客対応を実行
  ↓
毎月の成約数・顧客満足度が向上
  ↓
ジムの規模拡大
```

### Q28: Obsidian が「真の中枢」である理由は？

**A: シングルソースオブトゥルース（SSOT）の実装**

```
【従来のシステム】
LINE ボットのルール → Dify
SNS 戦略 → TikTok・Instagram（それぞれ異なる設定）
顧客情報 → Google Sheets
営業戦略 → メモ帳
→ データが分散・矛盾発生・更新漏れ

【FLATUP AI OS】
Obsidian = すべての原典
  ↓
Git 経由で VPS に同期
  ↓
Dify・AnythingLLM・n8n が Obsidian を参照
  ↓
「1 つの情報源」で全システムが統一

【メリット】
- 更新が 1 ヶ所で済む
- AI が常に「最新情報」で判断
- 手作業のミスが減る
- 思想が全系に一貫性を持つ
```

### Q29: 「思想優先」の本当の意味は？

**A: ツールの選定 > ツールの完璧性**

```
【よくある間違い】
「Dify が最新バージョンになった」
「AnythingLLM に新機能が追加された」
→ すぐに乗り換え・追加する（新しさへの執着）

【JIN のアプローチ】
「FLATUP GYMの『否定しない・小さな成功・褒める』という思想が
　どのツールなら最も自然に表現できるか？」
→ その視点で選ぶ

【具体例】
- なぜ Exbrain？→ 「AI が経営者になる」という思想を体現できるから
- なぜ Obsidian？→ 「思考の外部メモリ化」が最も シンプルだから
- なぜ Gemma 2？→「軽い・自分の手に」という制御感を保てるから
```

### Q30: 成功の定義は？

**A: 「自分が経営者でなくても、ジムが動く」状態**

```
【最低ライン（3 ヶ月目）】
✓ LINE 返信が 80% 自動化
✓ SNS 投稿が毎日自動生成・投稿
✓ 新規見込み客への自動営業が稼働
✓ 月 10 件以上の新規顧客獲得

【目標（6 ヶ月目）】
✓ LINE・SNS・営業が 100% 自動化
✓ AIKA ペルソナが「経営者」として意思決定
✓ ジムの売上が 50% 向上
✓ JIN は「戦略」だけ担当

【最終形態（12 ヶ月目）】
✓ AI が大会企画を提案「来月は女性向けエキシビション」
✓ AI が広告費配分を自動最適化
✓ AI が「新しいクラス」の企画を立案
✓ JIN は月 10 時間程度の「指導」に専念
  → 時間 × クオリティの完全両立
```

---

## 🔗 参考資料

### ツール・ドキュメントへのリンク

```
【リポジトリ】
- FLATUP AI：https://github.com/flatup1/flatup
- Exbrain：https://github.com/chaenmasahiro0425/exbrain

【API・サービス】
- OpenRouter：https://openrouter.ai
- Dify：https://dify.ai
- AnythingLLM：https://anythingllm.com
- LINE Messaging API：https://developers.line.biz

【ジムの詳細】
- LINE 公式：@jfl0054o
- 住所：千葉県成田市
- ドメイン：flatupnarita.jp
```

---

## 📝 最後に：他の AI への投げ方

このドキュメントを **Claude・GPT-4・Gemini** に投げるときは、以下のテンプレートを使用してください：

```
【命令】
以下は「格闘技ジムのAI自動化システム」の完全仕様書です。

このドキュメントを読んだ上で、次のいずれかをサポートしてください：

1️⃣ Exbrain の SOUL.md を 500 行の完全版に拡張する
2️⃣ VPS の自動同期スクリプト（cron）を実装する
3️⃣ LINE 診断・販売システムを Dify Workflow で実装する
4️⃣ OpenClaw（アウトバウンド営業自動化）の設計書を作る

【制約】
- 思想優先：「世界一やさしいジム」という哲学を貫く
- 最小工数：Mac で完結・新しいツール増やさない
- AIKAペルソナ：知的・親切・毅然・女性を守る

さあ、このドキュメントから「[指定のタスク]」を代行してくれ！
```

---

**作成日：2024年4月16日**
**JIN（松元仁志）の AI パートナーが作成**
**このドキュメントは随時更新されます**
