import type { CompetitorAnalysis, FetchedPage, ManualCompetitorInput } from "./types.js";

const unknown = "不明";

function includesAny(text: string, terms: string[]): boolean {
  return terms.some((term) => text.includes(term));
}

function extractPrice(text: string): string {
  const match = text.match(/(?:月額|月会費|料金|会費)[^。.\n]{0,40}?([0-9０-９,，]{3,6})\s*円/);
  return match?.[1] ? `${match[1].replace("，", ",")}円` : unknown;
}

function extractTrialPrice(text: string): string {
  const match = text.match(/(?:体験|初回)[^。.\n]{0,40}?([0-9０-９,，]{1,6})\s*円/);
  return match?.[1] ? `${match[1].replace("，", ",")}円` : unknown;
}

function yesNoUnknown(text: string, terms: string[]): string {
  if (!text) return unknown;
  return includesAny(text, terms) ? "あり" : unknown;
}

function inferStrengths(text: string): string[] {
  const strengths: string[] = [];
  if (includesAny(text, ["初心者", "未経験", "初めて"])) strengths.push("初心者向け訴求がある");
  if (includesAny(text, ["女性", "レディース", "ダイエット"])) strengths.push("女性向け訴求がある");
  if (includesAny(text, ["キッズ", "子ども", "子供", "小学生"])) strengths.push("キッズ向け訴求がある");
  if (includesAny(text, ["体験", "見学"])) strengths.push("体験・見学導線がある");
  return strengths.length ? strengths : ["公開ページから明確な強みは不明"];
}

function inferWeaknesses(text: string): string[] {
  const weaknesses: string[] = [];
  if (!includesAny(text, ["料金", "月額", "会費", "円"])) weaknesses.push("料金情報が見つけにくい可能性");
  if (!includesAny(text, ["初心者", "未経験", "初めて"])) weaknesses.push("初心者の不安解消訴求が弱い可能性");
  if (!includesAny(text, ["女性", "レディース"])) weaknesses.push("女性向け安心訴求が不明");
  return weaknesses.length ? weaknesses : ["目立つ弱みは公開情報だけでは不明"];
}

function opportunity(text: string): string {
  if (!includesAny(text, ["初心者", "未経験", "初めて"])) {
    return "「怖くない格闘技」「初心者歓迎」を前面に出す";
  }
  if (!includesAny(text, ["キッズ", "子ども", "子供"])) {
    return "キッズの自己肯定感と親御さんの安心を打ち出す";
  }
  if (!includesAny(text, ["女性", "レディース"])) {
    return "女性が不安なく通える雰囲気を具体化する";
  }
  return "FLATUPの「世界一やさしい格闘技ジム」を、コピーと実例で継続発信する";
}

export function analyzeCompetitors(
  manualCompetitors: ManualCompetitorInput[],
  pages: FetchedPage[]
): CompetitorAnalysis[] {
  const pageByUrl = new Map(pages.map((page) => [page.url.replace(/\/$/, ""), page]));

  return manualCompetitors.map((competitor) => {
    const page = pageByUrl.get(competitor.url.replace(/\/$/, ""));
    const text = page?.text ?? "";
    const title = page?.title || competitor.name || unknown;

    return {
      name: competitor.name || title,
      area: competitor.area || unknown,
      url: competitor.url,
      category: competitor.category || unknown,
      price: extractPrice(text),
      trial_price: extractTrialPrice(text),
      campaign: yesNoUnknown(text, ["キャンペーン", "入会金", "無料", "割引"]),
      kids_offer: yesNoUnknown(text, ["キッズ", "子ども", "子供", "小学生"]),
      women_offer: yesNoUnknown(text, ["女性", "レディース"]),
      beginner_offer: yesNoUnknown(text, ["初心者", "未経験", "初めて"]),
      opening_hours: unknown,
      google_review_count: unknown,
      google_review_summary: unknown,
      sns_activity: unknown,
      strengths: inferStrengths(text),
      weaknesses: page?.error ? [`ページ取得エラー: ${page.error}`] : inferWeaknesses(text),
      flatup_opportunity: opportunity(text),
      risk_level: page?.error ? "中" : "低",
      source_urls: [competitor.url]
    };
  });
}
