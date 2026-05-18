import { readJsonFile } from "./config.js";
import type { ManualCompetitorInput, SearchTask } from "./types.js";

const areas = ["成田市", "富里市", "酒々井町", "佐倉市", "印西市", "八街市"];

export async function loadKeywords(): Promise<string[]> {
  return readJsonFile<string[]>("keywords.json");
}

export async function loadManualCompetitors(): Promise<ManualCompetitorInput[]> {
  const competitors = await readJsonFile<ManualCompetitorInput[]>("competitors.manual.json");
  return competitors.filter((competitor) => Boolean(competitor.url));
}

export function buildSearchTasks(keywords: string[]): SearchTask[] {
  return keywords.map((keyword) => ({
    keyword,
    area: areas.find((area) => keyword.includes(area.replace("市", ""))) ?? "対象エリア",
    status: "manual_review_required",
    note: "MVPでは規約リスクを避けるため、検索結果の自動スクレイピングは行わず、手動追加URLをFetch対象にします。"
  }));
}
