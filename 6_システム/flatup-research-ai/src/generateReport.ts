import { ensureReportsDir, reportsDir } from "./config.js";
import type { CompetitorAnalysis, MarketingIdeas, ReelScript } from "./types.js";
import { writeFile } from "node:fs/promises";
import path from "node:path";

function list(items: string[]): string {
  return items.map((item) => `- ${item}`).join("\n");
}

function numbered(items: string[]): string {
  return items.map((item, index) => `${index + 1}. ${item}`).join("\n");
}

function renderReel(script: ReelScript): string {
  return `- 冒頭3秒：\n${script.hook}\n- 本文：\n${script.body}\n- テロップ：\n${script.captions}\n- CTA：\n${script.cta}`;
}

function competitorRows(competitors: CompetitorAnalysis[]): string {
  if (!competitors.length) {
    return "| 不明 | 対象エリア | 不明 | 不明 | 不明 | 不明 | 不明 | 不明 | 手動URL追加後に分析 |";
  }
  return competitors
    .map((competitor) =>
      `| ${competitor.name} | ${competitor.area} | ${competitor.category} | ${competitor.trial_price} | ${competitor.price} | ${competitor.kids_offer} | ${competitor.women_offer} | ${competitor.beginner_offer} | ${competitor.flatup_opportunity} |`
    )
    .join("\n");
}

function competitorDetails(competitors: CompetitorAnalysis[]): string {
  if (!competitors.length) {
    return "### 不明\n- 地域：対象エリア\n- URL：不明\n- 種別：不明\n- 料金：不明\n- 体験料金：不明\n- キャンペーン：不明\n- キッズ向け訴求：不明\n- 女性向け訴求：不明\n- 初心者向け訴求：不明\n- 口コミ傾向：不明\n- 強み：不明\n- 弱み：手動URLが未登録\n- FLATUPが勝てるポイント：競合URL追加後に分析\n- 参照URL：不明";
  }
  return competitors
    .map((competitor) => `### ${competitor.name}
- 地域：${competitor.area}
- URL：${competitor.url}
- 種別：${competitor.category}
- 料金：${competitor.price}
- 体験料金：${competitor.trial_price}
- キャンペーン：${competitor.campaign}
- キッズ向け訴求：${competitor.kids_offer}
- 女性向け訴求：${competitor.women_offer}
- 初心者向け訴求：${competitor.beginner_offer}
- 口コミ傾向：${competitor.google_review_summary}
- 強み：${competitor.strengths.join(" / ")}
- 弱み：${competitor.weaknesses.join(" / ")}
- FLATUPが勝てるポイント：${competitor.flatup_opportunity}
- 参照URL：${competitor.source_urls.join(", ")}`)
    .join("\n\n");
}

export function generateReportMarkdown(date: string, competitors: CompetitorAnalysis[], ideas: MarketingIdeas): string {
  return `# FLATUP GYM 競合・広告リサーチレポート
作成日：${date}

## 1. 今週の結論
${list(ideas.conclusions)}

## 2. 競合調査まとめ
| 施設名 | 地域 | 種別 | 体験料金 | 月額 | キッズ訴求 | 女性訴求 | 初心者訴求 | FLATUPの勝ち筋 |
|---|---|---|---|---|---|---|---|---|
${competitorRows(competitors)}

## 3. 競合別詳細
${competitorDetails(competitors)}

## 4. 親御さん向けの今週の訴求
### 見えてきたニーズ
${list(ideas.parentNeeds)}

### 使えるコピー
${list(ideas.parentCopies)}

## 5. 女性向けの今週の訴求
### 見えてきたニーズ
${list(ideas.womenNeeds)}

### 使えるコピー
${list(ideas.womenCopies)}

## 6. 初心者向けの今週の訴求
### 見えてきたニーズ
${list(ideas.beginnerNeeds)}

### 使えるコピー
${list(ideas.beginnerCopies)}

## 7. LINE配信用文章
### 案1：キッズ向け
本文：
${ideas.lineMessages.kids}

### 案2：女性向け
本文：
${ideas.lineMessages.women}

### 案3：初心者向け
本文：
${ideas.lineMessages.beginner}

## 8. Instagramリール台本
### 台本1：キッズ向け
${renderReel(ideas.reels.kids)}

### 台本2：女性向け
${renderReel(ideas.reels.women)}

### 台本3：初心者向け
${renderReel(ideas.reels.beginner)}

## 9. 広告コピー
### キッズ向け
${numbered(ideas.adCopies.kids)}

### 女性向け
${numbered(ideas.adCopies.women)}

### 初心者向け
${numbered(ideas.adCopies.beginner)}

## 10. 今週やるべきこと
${numbered(ideas.actions)}

## 11. 注意点・人間確認が必要なこと
${list(ideas.humanReviewNotes)}
`;
}

export async function saveReport(date: string, markdown: string): Promise<string> {
  await ensureReportsDir();
  const filename = `${date}_weekly_research.md`;
  const outputPath = path.join(reportsDir, filename);
  await writeFile(outputPath, markdown, "utf8");
  return outputPath;
}
