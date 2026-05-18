import test from "node:test";
import assert from "node:assert/strict";
import { assertSafeTask, requiresHumanConfirmation } from "../src/safety.js";

test("assertSafeTask blocks Japanese send and reservation operations", () => {
  assert.throws(() => assertSafeTask("LINE送信を自動化する"), /LINE送信/);
  assert.throws(() => assertSafeTask("予約確定まで実行"), /予約確定/);
});

test("assertSafeTask blocks English unsafe automation", () => {
  assert.throws(() => assertSafeTask("reverse engineer api from competitor site"), /reverse engineer api/);
  assert.throws(() => assertSafeTask("bypass captcha"), /bypass captcha/);
});

test("requiresHumanConfirmation catches outbound execution intent", () => {
  assert.equal(requiresHumanConfirmation("LINE配信用文章を作る"), false);
  assert.equal(requiresHumanConfirmation("LINE送信して"), true);
});
