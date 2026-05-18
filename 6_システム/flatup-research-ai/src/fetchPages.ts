import type { FetchedPage, ManualCompetitorInput } from "./types.js";

function assertPublicHttpUrl(rawUrl: string): URL {
  const url = new URL(rawUrl);
  if (!["http:", "https:"].includes(url.protocol)) {
    throw new Error(`HTTP/HTTPS以外のURLは取得しません: ${rawUrl}`);
  }
  if (url.username || url.password) {
    throw new Error(`認証情報を含むURLは取得しません: ${rawUrl}`);
  }
  return url;
}

function stripHtml(html: string): string {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 20000);
}

function extractTitle(html: string, fallback: string): string {
  const match = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  return (match?.[1]?.replace(/\s+/g, " ").trim() || fallback).slice(0, 120);
}

export async function fetchCompetitorPages(competitors: ManualCompetitorInput[]): Promise<FetchedPage[]> {
  const pages: FetchedPage[] = [];

  for (const competitor of competitors) {
    const fetchedAt = new Date().toISOString();
    try {
      const url = assertPublicHttpUrl(competitor.url);
      const response = await fetch(url, {
        headers: {
          "user-agent": "flatup-research-ai/0.1 (+public marketing research; low frequency)"
        },
        signal: AbortSignal.timeout(12000)
      });
      const html = await response.text();
      pages.push({
        url: url.toString(),
        title: extractTitle(html, competitor.name ?? url.hostname),
        text: response.ok ? stripHtml(html) : "",
        fetchedAt,
        error: response.ok ? undefined : `HTTP ${response.status}`
      });
    } catch (error) {
      pages.push({
        url: competitor.url,
        title: competitor.name ?? competitor.url,
        text: "",
        fetchedAt,
        error: error instanceof Error ? error.message : String(error)
      });
    }
  }

  return pages;
}
