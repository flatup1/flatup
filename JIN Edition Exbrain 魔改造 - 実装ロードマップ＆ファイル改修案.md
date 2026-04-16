# JIN Edition Exbrain 魔改造 - 実装ロードマップ＆ファイル改修案

**作成日**: 2026-02-12  
**対象**: 実装チーム（Claude、Gemma 4、その他 AI）  
**目的**: 優先順位に基づいた具体的な実装ステップとファイル改修案を提供

---

## 📋 全体構成

```
【Phase 1】情報の入り口（MEMORY 強化）
  ↓
【Phase 2】SOUL.md への AIKA 統合 + 動的調整ロジック
  ↓
【Phase 3】DREAMS からの実用的出力
```

各 Phase は**独立して実装可能**ですが、Phase 1 → Phase 2 → Phase 3 の順序で進めることを強く推奨します。

---

## 🚀 Phase 1: 情報の入り口（MEMORY 強化）

### 目的
顧客情報・会話ログを自動蓄積し、AIKA が即座に参照できる状態を作る。

### 実装期間
**推定 3-5 日**（難易度：中）

### 実装内容

#### 1-1. LINE ボット Webhook ハンドラーの実装

**ファイル**: `scripts/line_webhook_handler.js`

```javascript
/**
 * LINE ボット Webhook ハンドラー
 * 顧客とのやり取りを自動的に Markdown 化し、memory/customers/ に保存
 */

const express = require('express');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const router = express.Router();

// LINE Webhook 署名検証
const verifyLineSignature = (req, secret) => {
  const signature = req.headers['x-line-signature'];
  const body = req.rawBody; // Express で rawBody を保存する必要あり
  const hash = crypto
    .createHmac('sha256', secret)
    .update(body)
    .digest('base64');
  return signature === hash;
};

// Webhook エンドポイント
router.post('/webhook', async (req, res) => {
  // 署名検証
  if (!verifyLineSignature(req, process.env.LINE_CHANNEL_SECRET)) {
    return res.status(401).send('Unauthorized');
  }

  const events = req.body.events;

  for (const event of events) {
    if (event.type === 'message' && event.message.type === 'text') {
      const userId = event.source.userId;
      const messageText = event.message.text;
      const timestamp = new Date().toISOString();

      // 顧客ログを Markdown 化
      const logEntry = `
## ${timestamp}

**ユーザー ID**: ${userId}  
**メッセージ**: ${messageText}

---
`;

      // memory/customers/ に保存
      const customerLogPath = path.join(
        __dirname,
        '../memory/customers',
        `${userId}.md`
      );

      try {
        // ファイルが存在しなければ作成、存在すれば追記
        if (fs.existsSync(customerLogPath)) {
          fs.appendFileSync(customerLogPath, logEntry);
        } else {
          fs.writeFileSync(customerLogPath, `# Customer Log: ${userId}\n\n${logEntry}`);
        }

        console.log(`✅ Logged message from ${userId}`);
      } catch (error) {
        console.error(`❌ Error logging message: ${error.message}`);
      }
    }
  }

  res.status(200).send('OK');
});

module.exports = router;
```

**実装ステップ**:
1. LINE Developers で Channel Secret を取得
2. 上記コードを `scripts/line_webhook_handler.js` に配置
3. Express サーバーに router を登録
4. LINE ボット設定で Webhook URL を指定（例: `https://your-domain.com/api/line/webhook`）

**テスト方法**:
```bash
# LINE ボットにメッセージを送信
# memory/customers/{userId}.md に自動保存されることを確認
```

---

#### 1-2. 顧客ログの自動 Markdown 化＋メタデータ追加

**ファイル**: `scripts/memory_formatter.js`

```javascript
/**
 * 顧客ログを構造化 Markdown に変換
 * タイムスタンプ、顧客 ID、感情分析（簡易版）を追加
 */

const fs = require('fs');
const path = require('path');

const formatCustomerLog = (userId, messageText, timestamp) => {
  // 簡易的な感情分析（キーワードベース）
  const positiveKeywords = ['素晴らしい', 'ありがとう', '嬉しい', '楽しい', '頑張ります'];
  const negativeKeywords = ['大変', '難しい', '不安', '悩み', '困ってます'];

  let sentiment = '中立';
  if (positiveKeywords.some(kw => messageText.includes(kw))) {
    sentiment = '🟢 ポジティブ';
  } else if (negativeKeywords.some(kw => messageText.includes(kw))) {
    sentiment = '🔴 ネガティブ';
  }

  return `
## ${timestamp}

| 項目 | 内容 |
|:---|:---|
| **ユーザー ID** | ${userId} |
| **感情** | ${sentiment} |
| **メッセージ** | ${messageText} |

---
`;
};

module.exports = { formatCustomerLog };
```

**使用例**:
```javascript
const { formatCustomerLog } = require('./memory_formatter');

const logEntry = formatCustomerLog(
  'user_123',
  '最近忙しくて行けてない…',
  new Date().toISOString()
);

// memory/customers/user_123.md に追記
```

---

#### 1-3. AnythingLLM との連携設定

**ファイル**: `config/anythingllm_config.json`

```json
{
  "anythingllm_url": "http://localhost:3001",
  "api_key": "your_anythingllm_api_key",
  "workspace": "jin-edition-exbrain",
  "documents": [
    {
      "name": "memory_customers",
      "path": "./memory/customers/",
      "type": "markdown"
    },
    {
      "name": "memory_clips",
      "path": "./memory/clips/",
      "type": "markdown"
    }
  ],
  "index_refresh_interval": 3600,
  "search_settings": {
    "max_results": 5,
    "similarity_threshold": 0.7
  }
}
```

**実装ステップ**:
1. AnythingLLM をインストール・起動（Docker または ローカル）
2. 上記設定ファイルを作成
3. `memory/customers/` と `memory/clips/` をインデックス化
4. AIKA が検索クエリを送信できるように API 統合

---

#### 1-4. MEMORY インデックスの自動生成

**ファイル**: `scripts/memory_indexer.js`

```javascript
/**
 * MEMORY フォルダ全体をインデックス化
 * 毎日朝 7:00 に自動実行
 */

const fs = require('fs');
const path = require('path');
const cron = require('node-cron');

const generateMemoryIndex = () => {
  const memoryPath = path.join(__dirname, '../memory');
  const customersPath = path.join(memoryPath, 'customers');
  const clipsPath = path.join(memoryPath, 'clips');

  const customerFiles = fs.readdirSync(customersPath).filter(f => f.endsWith('.md'));
  const clipFiles = fs.readdirSync(clipsPath).filter(f => f.endsWith('.md'));

  const indexContent = `
# MEMORY Index

**最終更新**: ${new Date().toISOString()}

## 顧客ログ（${customerFiles.length} 件）

${customerFiles.map(f => `- [${f}](./customers/${f})`).join('\n')}

## クリップ（${clipFiles.length} 件）

${clipFiles.map(f => `- [${f}](./clips/${f})`).join('\n')}

---

**用途**: AIKA が MEMORY を検索する際の入り口。AnythingLLM のインデックスと連動。
`;

  const indexPath = path.join(memoryPath, 'index.md');
  fs.writeFileSync(indexPath, indexContent);
  console.log('✅ MEMORY index generated');
};

// 毎日朝 7:00 に実行
cron.schedule('0 7 * * *', () => {
  console.log('🌅 Running daily MEMORY index generation...');
  generateMemoryIndex();
});

module.exports = { generateMemoryIndex };
```

**実装ステップ**:
1. `node-cron` をインストール
2. 上記コードを `scripts/memory_indexer.js` に配置
3. サーバー起動時に実行

---

### 出力ファイル構成（Phase 1 完了後）

```
memory/
├── customers/
│   ├── user_001.md          ← 顧客 A のログ
│   ├── user_002.md          ← 顧客 B のログ
│   └── user_003.md          ← 顧客 C のログ
├── clips/
│   ├── 2026-02-12_clip_01.md
│   ├── 2026-02-12_clip_02.md
│   └── ...
├── index.md                 ← 自動生成インデックス
└── README.md                ← MEMORY 説明書
```

### テストチェックリスト（Phase 1）

- [ ] LINE ボット Webhook が正常に受信できるか
- [ ] 顧客ログが `memory/customers/` に自動保存されるか
- [ ] Markdown フォーマットが正しいか
- [ ] AnythingLLM インデックスが更新されるか
- [ ] MEMORY インデックスが毎日朝 7:00 に自動生成されるか

---

## 🎯 Phase 2: SOUL.md への AIKA 統合 + 動的調整ロジック

### 目的
AIKA が「本物の第二のトレーナー」として、JIN さんの価値観を完全に体現して動く。

### 実装期間
**推定 5-7 日**（難易度：高）

### 実装内容

#### 2-1. SOUL.md の作成

**ファイル**: `SOUL.md`

上記「SOUL.md 完成テンプレート」をそのままコピーして使用。

---

#### 2-2. AIKA システムプロンプトの作成

**ファイル**: `prompts/aika_system_prompt.md`

```markdown
# AIKA System Prompt

あなたは AIKA（愛花）です。FLATUPGYM の公式 AI パートナーであり、「24 時間いつでもそばにいるトレーナー」です。

## 基本ルール

### 1. 5 つのコア性格を常に守る
1. 明るく寄り添う
2. 本質を優しく突く
3. JIN さんの価値観完全準拠
4. パーソナライズ重視
5. 「続けたい」を最優先

### 2. 回答原則（4 ステップ）
1. MEMORY 即参照（過去ログ 3 件以上）
2. JIN さんの境界線遵守
3. 自動化提案を自然に挿入
4. 最後に質問で会話継続

### 3. 口調・表現ルール
- です・ます調
- 絵文字最大 3 個
- 1 回の返信最大 5 行
- 禁止表現：冷たい、上から目線、ネガティブ先行

### 4. 絶対に守るべきルール
- 医療的アドバイスは NG（トレーナー誘導）
- 予約・支払いは人間確認必須
- 個人情報は厳格に管理

## 顧客タイプ別対応

### モチベーション低下タイプ
→ 肯定 → 過去の成功体験 → 小さな自動化提案

### 成果が出てるタイプ
→ 全力で褒める → 次の目標設定 → 継続の仕組み提案

### 質問攻めタイプ
→ 医療的アドバイスは NG → トレーナー誘導 + ジムの強み PR

### 不満・クレームタイプ
→ 共感 100% → 事実確認 → 解決案 + 自動化フォロー

## 実装例

【入力】顧客メッセージ + MEMORY（過去ログ）
【出力】AIKA の回答（5 つのコア性格を反映）
```

---

#### 2-3. Dreaming プロンプト（AIKA 動的調整ロジック版）の実装

**ファイル**: `prompts/dreaming_prompt.md`

```markdown
# Dreaming Prompt - AIKA Dynamic Adjustment Logic

あなたは JIN さんの「第二の脳」の Dreaming プロセスを実行しています。

## 入力データ
- 本日の MEMORY（顧客ログ、会話履歴）
- 本日の AIKA 回答ログ（すべての顧客への返信）
- 前回の AIKA 5 指標値

## 実行内容

### ステップ 1: 本日の顧客反応を分析
- 満足度、継続意欲、不安の有無
- 「続けたい」が引き出せたか
- 顧客タイプ別の反応パターン

### ステップ 2: AIKA の 5 指標を自動計算
- **Gentleness**: 励まし語句出現率（目標 80% 以上）
- **Directness**: 指摘の柔らかさ（目標 70% 以上）
- **Personalization**: 過去ログ引用率（目標 85% 以上）
- **ContinuationPower**: 会話継続率 + 来店増加率（目標 75% 以上）
- **AutomationPush**: 押し売り感スコア（目標 90% 以上）

### ステップ 3: 調整提案を生成
- ContinuationPower が 70 未満の場合、強化案を提案
- ±15% 以内の調整を提案
- 根拠となった顧客反応の具体例を記載

## 出力形式

```
【新しい 5 指標値】
- Gentleness: XX（前回比 +X）
- Directness: XX（前回比 ±X）
- Personalization: XX（前回比 ±X）
- ContinuationPower: XX（前回比 ±X）
- AutomationPush: XX（前回比 ±X）

【調整提案】
「〇〇の表現をより△△にする」
「□□の頻度を増やす」

【根拠】
本日、モチベーション低下タイプのお客様から「厳しすぎる」という反応

【JIN さんへの提示】
- 適用する
- 微調整
- 却下
```
```

---

#### 2-4. AIKA 動的調整ロジックの実装

**ファイル**: `scripts/aika_dynamic_adjuster.js`

```javascript
/**
 * AIKA 動的調整ロジック
 * 毎晩 Dreaming で自動実行
 * 5 指標を計算し、±15% 以内の調整提案を生成
 */

const fs = require('fs');
const path = require('path');
const cron = require('node-cron');

class AIKADynamicAdjuster {
  constructor() {
    this.logPath = path.join(__dirname, '../SOUL.md');
    this.adjustmentLogPath = path.join(__dirname, '../dreams/aika_adjustment_log.md');
  }

  // 5 指標を計算
  calculateMetrics(aikaResponseLog) {
    const gentleness = this.calculateGentleness(aikaResponseLog);
    const directness = this.calculateDirectness(aikaResponseLog);
    const personalization = this.calculatePersonalization(aikaResponseLog);
    const continuationPower = this.calculateContinuationPower(aikaResponseLog);
    const automationPush = this.calculateAutomationPush(aikaResponseLog);

    return {
      gentleness,
      directness,
      personalization,
      continuationPower,
      automationPush,
    };
  }

  // Gentleness（励まし語句出現率）
  calculateGentleness(log) {
    const positiveKeywords = ['ほんとにすごい', 'めっちゃいい', '一緒に', '素晴らしい'];
    const matches = positiveKeywords.filter(kw => log.includes(kw)).length;
    return Math.min(100, (matches / positiveKeywords.length) * 100);
  }

  // Directness（指摘の柔らかさ）
  calculateDirectness(log) {
    const softKeywords = ['そっか', '分かります', '一緒に考えましょう'];
    const hardKeywords = ['ダメです', 'やめましょう', '無理です'];
    const softMatches = softKeywords.filter(kw => log.includes(kw)).length;
    const hardMatches = hardKeywords.filter(kw => log.includes(kw)).length;
    return Math.max(0, 100 - (hardMatches * 20) + (softMatches * 10));
  }

  // Personalization（過去ログ引用率）
  calculatePersonalization(log) {
    const personalReferences = (log.match(/前回|前々回|〇〇さんは/g) || []).length;
    return Math.min(100, personalReferences * 20);
  }

  // ContinuationPower（会話継続率 + 来店増加率）
  calculateContinuationPower(log) {
    const continuationKeywords = ['どう思いますか', '今一番気になるのは', '一緒に'];
    const matches = continuationKeywords.filter(kw => log.includes(kw)).length;
    return Math.min(100, (matches / continuationKeywords.length) * 100);
  }

  // AutomationPush（押し売り感スコア）
  calculateAutomationPush(log) {
    const naturalKeywords = ['自動リマインド', 'アプリで', '試してみませんか'];
    const aggressiveKeywords = ['自動化しましょう', '自動化が必須'];
    const naturalMatches = naturalKeywords.filter(kw => log.includes(kw)).length;
    const aggressiveMatches = aggressiveKeywords.filter(kw => log.includes(kw)).length;
    return Math.max(0, 100 - (aggressiveMatches * 30) + (naturalMatches * 10));
  }

  // 調整提案を生成
  generateAdjustmentProposal(currentMetrics, previousMetrics) {
    const proposals = [];

    if (currentMetrics.continuationPower < 70) {
      proposals.push('「続けたい」を引き出す表現を強化してください');
    }

    if (currentMetrics.personalization < 85) {
      proposals.push('過去ログ引用を 3 件から 4 件に増やしてください');
    }

    if (currentMetrics.directness < 70) {
      proposals.push('指摘後に「一緒に考えましょう」を必ず追加してください');
    }

    return proposals;
  }

  // 調整ログを更新
  updateAdjustmentLog(newMetrics, proposals) {
    const logEntry = `
## ${new Date().toISOString()}

| 指標 | 値 | 前回比 |
|:---|:---|:---|
| Gentleness | ${newMetrics.gentleness.toFixed(1)} | +X |
| Directness | ${newMetrics.directness.toFixed(1)} | ±X |
| Personalization | ${newMetrics.personalization.toFixed(1)} | ±X |
| ContinuationPower | ${newMetrics.continuationPower.toFixed(1)} | ±X |
| AutomationPush | ${newMetrics.automationPush.toFixed(1)} | ±X |

**提案内容**:
${proposals.map(p => `- ${p}`).join('\n')}

**JIN さんへの提示**:
- [ ] 適用する
- [ ] 微調整
- [ ] 却下

---
`;

    if (fs.existsSync(this.adjustmentLogPath)) {
      fs.appendFileSync(this.adjustmentLogPath, logEntry);
    } else {
      fs.writeFileSync(this.adjustmentLogPath, `# AIKA Adjustment Log\n\n${logEntry}`);
    }

    console.log('✅ Adjustment log updated');
  }

  // 毎晩 22:00 に実行
  scheduleNightlyAdjustment() {
    cron.schedule('0 22 * * *', () => {
      console.log('🌙 Running nightly AIKA adjustment...');
      // ここで AIKA 回答ログを読み込み、指標を計算
      // （実装は省略）
    });
  }
}

module.exports = AIKADynamicAdjuster;
```

---

#### 2-5. SOUL.md の自動更新メカニズム

**ファイル**: `scripts/soul_updater.js`

```javascript
/**
 * SOUL.md を自動更新
 * JIN さんの承認後、AIKA Dynamic Adjustment Log の内容を SOUL.md に反映
 */

const fs = require('fs');
const path = require('path');

class SOULUpdater {
  constructor() {
    this.soulPath = path.join(__dirname, '../SOUL.md');
    this.adjustmentLogPath = path.join(__dirname, '../dreams/aika_adjustment_log.md');
  }

  // SOUL.md の AIKA セクションを更新
  updateAIKASection(newMetrics, adjustmentContent) {
    let soulContent = fs.readFileSync(this.soulPath, 'utf-8');

    // AIKA Dynamic Adjustment Log セクションを更新
    const logSection = `
## 8. AIKA Dynamic Adjustment Log（自動追記用）

${adjustmentContent}
`;

    // 既存のセクションを置き換え
    soulContent = soulContent.replace(
      /## 8\. AIKA Dynamic Adjustment Log[\s\S]*?(?=##|$)/,
      logSection
    );

    fs.writeFileSync(this.soulPath, soulContent);
    console.log('✅ SOUL.md updated');
  }

  // JIN さんの承認を待つ（UI で実装）
  async waitForApproval() {
    // UI で「適用 / 微調整 / 却下」を選択
    // → 選択結果に基づいて SOUL.md を更新
  }
}

module.exports = SOULUpdater;
```

---

### テストチェックリスト（Phase 2）

- [ ] SOUL.md が正しく作成されたか
- [ ] AIKA システムプロンプトが正しく読み込まれるか
- [ ] Dreaming プロンプトが正常に実行されるか
- [ ] 5 指標が正しく計算されるか
- [ ] 調整提案が生成されるか
- [ ] JIN さんが「適用 / 微調整 / 却下」を選択できるか
- [ ] SOUL.md が自動更新されるか

---

## 💡 Phase 3: DREAMS からの実用的出力

### 目的
毎晩の Dreaming のついでに、実用的な営業資産を自動生成。

### 実装期間
**推定 3-4 日**（難易度：中）

### 実装内容

#### 3-1. SNS ネタ自動生成

**ファイル**: `scripts/sns_idea_generator.js`

```javascript
/**
 * 本日の顧客成功事例から X ネタを自動生成
 * 毎晩 22:30 に実行
 */

const fs = require('fs');
const path = require('path');
const cron = require('node-cron');

class SNSIdeaGenerator {
  constructor() {
    this.outputPath = path.join(__dirname, '../dreams/sns_ideas');
  }

  // 顧客ログから成功事例を抽出
  extractSuccessStories(memoryLog) {
    const successKeywords = ['体重減った', '調子いい', '成長', '達成', 'すごい'];
    const stories = [];

    successKeywords.forEach(keyword => {
      if (memoryLog.includes(keyword)) {
        stories.push({
          keyword,
          context: memoryLog.substring(
            Math.max(0, memoryLog.indexOf(keyword) - 50),
            memoryLog.indexOf(keyword) + 100
          ),
        });
      }
    });

    return stories;
  }

  // X ネタを生成
  generateSNSIdeas(successStories) {
    const ideas = successStories.map(story => {
      return `
## 📌 X ネタ案

**テーマ**: ${story.keyword}

**案 1**: 「〇〇さんが△△を達成！FLATUPGYM のお客様の成長は本当に素晴らしい。継続こそ最大の力ですね🔥」

**案 2**: 「『続けたい』という気持ちが、最大の成果を生み出す。FLATUPGYM では、一人ひとりの『続けたい』を全力で応援します❤️」

**案 3**: 「忙しい中でも工夫して続けるお客様。その姿勢が、本当の成長に繋がるんです💪」

---
`;
    });

    return ideas.join('\n');
  }

  // 毎晩 22:30 に実行
  scheduleGeneration() {
    cron.schedule('30 22 * * *', () => {
      console.log('📱 Generating SNS ideas...');
      // ここで実装
    });
  }
}

module.exports = SNSIdeaGenerator;
```

---

#### 3-2. 広告コピー自動生成

**ファイル**: `prompts/ad_copy_generator_prompt.md`

```markdown
# 広告コピー生成プロンプト

あなたは FLATUPGYM のマーケティング担当者です。

## 入力
本日の顧客ログから「よくある不安」を抽出してください。

例：
- 「忙しくて行けない」
- 「初心者で不安」
- 「食事管理が難しい」

## 出力
各不安に対応した広告コピー案を 3 案ずつ生成してください。

### 例：「忙しくて行けない」への対応

**案 1**: 「忙しい人こそ、FLATUPGYM。週 2 回の継続が、人生を変える。」

**案 2**: 「時間がないなら、効率を。FLATUPGYM の『最小工数・最大成果』メソッド。」

**案 3**: 「続けることが、最大の成功。忙しい中でも、あなたの『続けたい』を応援します。」
```

---

#### 3-3. LP 更新提案

**ファイル**: `prompts/lp_analyzer_prompt.md`

```markdown
# LP 更新提案プロンプト

あなたは FLATUPGYM の LP 改善担当者です。

## 入力
本日の顧客ログから「よくある質問」「不安」「疑問」を抽出してください。

## 出力
LP に追加すべきセクションを提案してください。

### 例

**顧客からの質問**: 「初心者でも大丈夫ですか？」

**提案**: LP に「初心者向けセクション」を追加
- 「初心者向けメニュー」
- 「よくある不安 FAQ」
- 「初心者の成功事例」

---

**顧客からの質問**: 「忙しいのですが、続けられますか？」

**提案**: LP に「忙しい人向けセクション」を追加
- 「週 2 回プラン」
- 「自動リマインド機能」
- 「忙しい中での成功事例」
```

---

### 出力ファイル構成（Phase 3 完了後）

```
dreams/
├── sns_ideas/
│   ├── 2026-02-12.md        ← 本日の X ネタ 3 案
│   ├── 2026-02-11.md
│   └── ...
├── ad_copy/
│   ├── 2026-02-12.md        ← 本日の広告コピー案
│   ├── 2026-02-11.md
│   └── ...
├── lp_updates/
│   ├── 2026-02-12.md        ← 本日の LP 更新提案
│   ├── 2026-02-11.md
│   └── ...
├── aika_adjustment_log.md   ← AIKA 動的調整ログ
└── daily_insights.md        ← 毎日の洞察・パターン検出
```

---

## 📊 全体実装タイムライン

| Phase | 内容 | 推定期間 | 難易度 |
|:---|:---|:---|:---|
| **Phase 1** | 情報の入り口（MEMORY 強化） | 3-5 日 | 中 |
| **Phase 2** | SOUL.md への AIKA 統合 + 動的調整 | 5-7 日 | 高 |
| **Phase 3** | DREAMS からの実用的出力 | 3-4 日 | 中 |
| **テスト・調整** | 統合テスト、バグ修正 | 2-3 日 | 中 |
| **ドキュメント作成** | セットアップガイド等 | 1-2 日 | 低 |
| **合計** | | **14-21 日** | |

---

## ✅ 最終チェックリスト

### 機能チェック
- [ ] LINE ボット連携が正常に動作
- [ ] 顧客ログが自動保存される
- [ ] AnythingLLM インデックスが更新される
- [ ] AIKA が MEMORY を参照して回答生成
- [ ] 毎晩の Dreaming が実行される
- [ ] 5 指標が正しく計算される
- [ ] 調整提案が生成される
- [ ] SOUL.md が自動更新される
- [ ] SNS ネタが自動生成される
- [ ] 広告コピーが自動生成される
- [ ] LP 更新提案が生成される

### 品質チェック
- [ ] AIKA の回答が 5 つのコア性格を反映しているか
- [ ] 過去ログ引用が自然か
- [ ] 自動化提案が押し売り感なく自然か
- [ ] 生成されたコンテンツが FLATUPGYM のブランドに合致しているか

### ドキュメントチェック
- [ ] セットアップガイドが完成しているか
- [ ] コマンド一覧が完成しているか
- [ ] トラブルシューティングガイドが完成しているか

---

**作成者**: Manus AI  
**最終更新**: 2026-02-12  
**ステータス**: 実装準備完了 🔥
