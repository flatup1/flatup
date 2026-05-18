import { analyzeCompetitors } from "./analyzeCompetitors.js";
import { fetchCompetitorPages } from "./fetchPages.js";
import { generateMarketingIdeas } from "./generateMarketingIdeas.js";
import { generateReportMarkdown, saveReport } from "./generateReport.js";
import { buildSearchTasks, loadKeywords, loadManualCompetitors } from "./search.js";
import { assertSafeTask } from "./safety.js";
import { getBrowserbaseStatus, todayIso } from "./config.js";

async function main(): Promise<void> {
  assertSafeTask("public competitor research and markdown marketing draft generation");

  const keywords = await loadKeywords();
  const manualCompetitors = await loadManualCompetitors();
  const browserbase = getBrowserbaseStatus();
  const searchTasks = buildSearchTasks(keywords);
  const pages = await fetchCompetitorPages(manualCompetitors);
  const competitors = analyzeCompetitors(manualCompetitors, pages);
  const ideas = generateMarketingIdeas(competitors);
  const date = todayIso();
  const markdown = generateReportMarkdown(date, competitors, ideas);
  const outputPath = await saveReport(date, markdown);

  console.log(`Research tasks prepared: ${searchTasks.length}`);
  console.log(`Browserbase available: ${browserbase.available ? "yes" : "no"} - ${browserbase.reason}`);
  console.log(`Manual competitor URLs fetched: ${manualCompetitors.length}`);
  console.log(`Report written: ${outputPath}`);
  console.log("このMVPはLINE送信・予約確定・請求変更・内部API解析を行いません。");
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
