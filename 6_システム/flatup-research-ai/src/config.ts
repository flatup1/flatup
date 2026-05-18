import { mkdir, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const projectRoot = path.resolve(__dirname, "..", "..");
export const dataDir = path.join(projectRoot, "data");
export const reportsDir = path.join(projectRoot, "reports");
export const promptsDir = path.join(projectRoot, "prompts");

export function todayIso(): string {
  return new Intl.DateTimeFormat("sv-SE", {
    timeZone: "Asia/Tokyo",
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  }).format(new Date());
}

export async function ensureReportsDir(): Promise<void> {
  await mkdir(reportsDir, { recursive: true });
}

export async function readJsonFile<T>(filename: string): Promise<T> {
  const raw = await readFile(path.join(dataDir, filename), "utf8");
  return JSON.parse(raw) as T;
}

export const flatupProfile = {
  gym_name: "FLATUP GYM",
  location: "千葉県成田市",
  concept: "世界一やさしい格闘技ジム",
  main_targets: ["初心者", "女性", "キッズ", "シニア"],
  main_services: ["キックボクシング", "ブラジリアン柔術", "キッズクラス", "レディース向けフィットネス", "護身術", "AI活用"],
  brand_values: [
    "怖くない格闘技",
    "強い人が偉い世界にしない",
    "初心者にやさしい",
    "女性が安心して通える",
    "子どもの自己肯定感を育てる",
    "勝ち負けより挑戦する勇気",
    "楽しく続けられる"
  ]
};

export function getBrowserbaseStatus(): { available: boolean; reason: string } {
  const hasApiKey = Boolean(process.env.BROWSERBASE_API_KEY);
  const hasProjectId = Boolean(process.env.BROWSERBASE_PROJECT_ID);
  if (hasApiKey && hasProjectId) {
    return {
      available: true,
      reason: "BROWSERBASE_API_KEY と BROWSERBASE_PROJECT_ID が設定されています。MVPでは公開ページ閲覧が必要な場合のみ利用対象です。"
    };
  }
  return {
    available: false,
    reason: "Browserbase環境変数が未設定です。MVPは手動URLの通常Fetchで動作します。"
  };
}
