const blockedEnglishPatterns = [
  "send line",
  "send email",
  "confirm reservation",
  "cancel membership",
  "change billing",
  "update payment",
  "delete customer",
  "scrape private api",
  "reverse engineer api",
  "bypass captcha",
  "login without permission"
];

const blockedJapanesePatterns = [
  "LINE送信",
  "メール送信",
  "予約確定",
  "予約変更",
  "退会処理",
  "休会処理",
  "請求変更",
  "会員情報変更",
  "内部API",
  "リバースエンジニアリング",
  "CAPTCHA回避",
  "無断ログイン"
];

const confirmationPatterns = [
  ...blockedJapanesePatterns,
  "送信",
  "投稿",
  "公開",
  "実行",
  "予約",
  "請求",
  "会員情報",
  "send",
  "post",
  "publish",
  "execute"
];

export function assertSafeTask(task: string): void {
  const lower = task.toLowerCase();
  for (const pattern of blockedEnglishPatterns) {
    if (lower.includes(pattern)) {
      throw new Error(`安全上の理由により、この操作は自動実行できません: ${pattern}`);
    }
  }

  for (const pattern of blockedJapanesePatterns) {
    if (task.includes(pattern)) {
      throw new Error(`安全上の理由により、この操作は自動実行できません: ${pattern}`);
    }
  }
}

export function requiresHumanConfirmation(task: string): boolean {
  const lower = task.toLowerCase();
  return confirmationPatterns.some((pattern) => {
    if (/^[a-z ]+$/.test(pattern)) {
      return lower.includes(pattern);
    }
    return task.includes(pattern);
  });
}

export const HUMAN_CONFIRMATION_TEXT = "この内容で実行・送信してよろしいですか？";
