# LINE広告データ自動取得GAS設定ガイド

このガイドでは、LINE広告のパフォーマンスデータをGoogle Apps Script (GAS) を使用してGoogleスプレッドシートに自動で取り込むための設定手順を説明します。

## 1. LINE Ads APIの認証情報取得

LINE Ads APIを利用するには、**LINE Business Center**で開発者登録を行い、APIの認証情報を取得する必要があります。

### 1.1. LINE Business Centerでの開発者登録

1.  [LINE Business Center](https://account.line.biz/) にアクセスし、LINEアカウントでログインします。
2.  「開発者向け」セクションに進み、開発者登録を完了させます。

### 1.2. Messaging APIチャネルの作成とアクセストークンの発行

LINE Ads APIの認証には、**JWS (JSON Web Signature) トークン**を使用します。このトークンを生成するために、`API_KEY_ID` (Access Key) と `API_KEY_SECRET` (Secret Key) が必要です。これらは、LINE Business Centerで作成する「チャネル」から取得します。

1.  LINE Business Centerで「プロバイダー」を作成し、その下に「Messaging APIチャネル」を作成します。
2.  作成したチャネルの「チャネル設定」タブに移動します。
3.  「LINE Ads API設定」セクションで、`Access Key` と `Secret Key` を確認し、控えておきます。これらがスクリプトの `API_KEY_ID` と `API_KEY_SECRET` になります。

### 1.3. 広告アカウントIDの確認

LINE広告の管理画面で、データを取得したい広告アカウントのIDを確認します。これは通常、URLや管理画面の表示で確認できます。スクリプトの `AD_ACCOUNT_ID` に設定します。

## 2. Googleスプレッドシートの準備

データを書き込むためのGoogleスプレッドシートを準備します。

1.  Googleドライブで新しいGoogleスプレッドシートを作成します。
2.  スプレッドシートのURLからシートIDを控えておきます。URLは `https://docs.google.com/spreadsheets/d/` の後に続く文字列です。これがスクリプトの `SPREADSHEET_ID` になります。
3.  スプレッドシートの1行目に、以下のヘッダーを設定することを推奨します。
    `日付`, `キャンペーン名`, `表示回数`, `クリック数`, `消化金額`, `コンバージョン数`
    （スクリプトはAPIから取得したCSVのヘッダーを元に列を特定しますが、事前に設定しておくと分かりやすいです。）

## 3. Google Apps Script (GAS) の設定

### 3.1. スクリプトエディタの起動

1.  準備したGoogleスプレッドシートを開きます。
2.  メニューバーから「拡張機能」>「Apps Script」を選択し、スクリプトエディタを開きます。

### 3.2. スクリプトの貼り付け

以下のGASスクリプトをコピーし、スクリプトエディタに貼り付けます。既存の `コード.gs` の内容をすべて削除し、貼り付けてください。

```javascript
function getLineAdsReport() {
  // --- 設定項目 --- //
  const SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'; // GoogleスプレッドシートのID
  const API_KEY_ID = 'YOUR_API_KEY_ID';         // LINE Ads APIのAccess Key
  const API_KEY_SECRET = 'YOUR_API_KEY_SECRET'; // LINE Ads APIのSecret Key
  const AD_ACCOUNT_ID = 'YOUR_AD_ACCOUNT_ID';   // LINE広告のアカウントID (例: 'A123456789')

  // --- 日付設定（前日のデータを取得） --- //
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);
  const YESTERDAY_STR = Utilities.formatDate(yesterday, Session.getScriptTimeZone(), 'yyyy-MM-dd');

  // --- レポート作成リクエストボディの生成 --- //
  const reportRequestBody = JSON.stringify({
    level: 'CAMPAIGN', // キャンペーンレベルのレポート
    since: YESTERDAY_STR,
    until: YESTERDAY_STR,
    breakdown: { time: 'DAY' }, // 日別でブレイクダウン
    filtering: { idType: 'ADACCOUNT', ids: [AD_ACCOUNT_ID] }, // 特定のアカウントIDでフィルタリング
    fileFormat: 'CSV', // CSV形式で取得
    locale: 'ja' // 日本語ロケール
  });

  // --- JWSトークン生成 --- //
  const jwsToken = generateJwsToken(API_KEY_ID, API_KEY_SECRET, AD_ACCOUNT_ID, reportRequestBody);
  if (!jwsToken) {
    Logger.log('JWSトークンの生成に失敗しました。');
    return;
  }

  // --- レポート作成リクエスト --- //
  const reportId = createLineAdsReport(jwsToken, AD_ACCOUNT_ID, reportRequestBody);
  if (!reportId) {
    Logger.log('レポート作成リクエストに失敗しました。');
    return;
  }

  // --- レポートダウンロード --- //
  const reportData = downloadLineAdsReport(jwsToken, AD_ACCOUNT_ID, reportId);
  if (!reportData) {
    Logger.log('レポートデータのダウンロードに失敗しました。');
    return;
  }

  // --- スプレッドシートに書き込み --- //
  writeToSpreadsheet(SPREADSHEET_ID, reportData);
}

/**
 * JWS (JSON Web Signature) トークンを生成します。
 * @param {string} apiKeyId LINE Ads APIのAccess Key
 * @param {string} apiKeySecret LINE Ads APIのSecret Key
 * @param {string} adAccountId LINE広告のアカウントID
 * @param {string} requestBodyJson レポート作成リクエストのJSON文字列
 * @return {string|null} 生成されたJWSトークン、またはnull
 */
function generateJwsToken(apiKeyId, apiKeySecret, adAccountId, requestBodyJson) {
  const method = 'POST'; // レポート作成はPOST
  const canonicalUri = `/api/v3/adaccounts/${adAccountId}/pfreports`;
  const contentType = 'application/json';

  // DateヘッダーとPayloadDateの生成
  const date = Utilities.formatDate(new Date(), 'GMT', 'EEE, dd MMM yyyy HH:mm:ss z');
  const payloadDate = Utilities.formatDate(new Date(), 'GMT', 'yyyyMMdd');

  // SHA256ダイジェストの計算
  const hexDigest = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, requestBodyJson).map(byte => ('0' + (byte & 0xFF).toString(16)).slice(-2)).join('');

  // JWSヘッダーのBase64エンコード
  const jwsHeader = Utilities.base64EncodeWebSafe(JSON.stringify({
    alg: 'HS256',
    kid: apiKeyId,
    typ: 'text/plain',
  })).replace(/=/g, ''); // パディングを削除

  // JWSペイロードの生成とBase64エンコード
  const payload = `${hexDigest}\n${contentType}\n${payloadDate}\n${canonicalUri}`;
  const jwsPayload = Utilities.base64EncodeWebSafe(payload).replace(/=/g, ''); // パディングを削除

  // 署名入力の生成
  const signingInput = `${jwsHeader}.${jwsPayload}`;
  
  // HMAC-SHA256署名の計算とBase64エンコード
  const signature = Utilities.computeHmacSignature(Utilities.MacAlgorithm.HMAC_SHA_256, signingInput, apiKeySecret);
  const encodedSignature = Utilities.base64EncodeWebSafe(signature).replace(/=/g, ''); // パディングを削除

  return `${jwsHeader}.${jwsPayload}.${encodedSignature}`;
}

/**
 * LINE広告のレポート作成をリクエストします。
 * @param {string} jwsToken JWSトークン
 * @param {string} adAccountId LINE広告のアカウントID
 * @param {string} payload レポート作成リクエストのJSON文字列
 * @return {string|null} 作成されたレポートのID、またはnull
 */
function createLineAdsReport(jwsToken, adAccountId, payload) {
  const url = `https://ads.line.me/api/v3/adaccounts/${adAccountId}/pfreports`;

  const options = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'Authorization': `Bearer ${jwsToken}`,
      'Date': Utilities.formatDate(new Date(), 'GMT', 'EEE, dd MMM yyyy HH:mm:ss z'),
    },
    payload: payload,
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(url, options);
    const responseCode = response.getResponseCode();
    const responseBody = response.getContentText();

    if (responseCode === 200) {
      const jsonResponse = JSON.parse(responseBody);
      Logger.log('レポート作成リクエスト成功: ' + JSON.stringify(jsonResponse));
      return jsonResponse.id; // レポートIDを返す
    } else {
      Logger.log(`レポート作成リクエスト失敗: コード ${responseCode}, レスポンス: ${responseBody}`);
      return null;
    }
  } catch (e) {
    Logger.log('レポート作成リクエスト中にエラーが発生しました: ' + e.toString());
    return null;
  }
}

/**
 * LINE広告のレポートダウンロードをリクエストし、CSVデータを取得します。
 * レポートが準備できるまでポーリングします。
 * @param {string} jwsToken JWSトークン
 * @param {string} adAccountId LINE広告のアカウントID
 * @param {string} reportId 作成されたレポートのID
 * @return {string|null} CSV形式のレポートデータ、またはnull
 */
function downloadLineAdsReport(jwsToken, adAccountId, reportId) {
  const checkStatusUrl = `https://ads.line.me/api/v3/adaccounts/${adAccountId}/pfreports/${reportId}`;
  const downloadUrl = `https://ads.line.me/api/v3/adaccounts/${adAccountId}/pfreports/${reportId}/download`;

  const options = {
    method: 'get',
    headers: {
      'Authorization': `Bearer ${jwsToken}`,
      'Date': Utilities.formatDate(new Date(), 'GMT', 'EEE, dd MMM yyyy HH:mm:ss z'),
    },
    muteHttpExceptions: true
  };

  // レポートが準備できるまでポーリング
  let status = '';
  let attempts = 0;
  const maxAttempts = 30; // 最大30回 (30秒 * 30 = 15分)
  const interval = 30 * 1000; // 30秒ごとにチェック

  while (status !== 'READY' && attempts < maxAttempts) {
    try {
      const response = UrlFetchApp.fetch(checkStatusUrl, options);
      const responseCode = response.getResponseCode();
      const responseBody = response.getContentText();

      if (responseCode === 200) {
        const jsonResponse = JSON.parse(responseBody);
        status = jsonResponse.status;
        Logger.log(`レポートID ${reportId} のステータス: ${status}`);
        if (status === 'READY') {
          break;
        } else if (status === 'FAILED') {
          Logger.log('レポート作成が失敗しました。');
          return null;
        }
      } else {
        Logger.log(`レポートステータスチェック失敗: コード ${responseCode}, レスポンス: ${responseBody}`);
        return null;
      }
    } catch (e) {
      Logger.log('レポートステータスチェック中にエラーが発生しました: ' + e.toString());
      return null;
    }
    attempts++;
    if (attempts < maxAttempts) {
      Utilities.sleep(interval);
    }
  }

  if (status !== 'READY') {
    Logger.log('レポートが時間内に準備できませんでした。');
    return null;
  }

  // レポートダウンロード
  try {
    const response = UrlFetchApp.fetch(downloadUrl, options);
    const responseCode = response.getResponseCode();
    const responseBody = response.getContentText();

    if (responseCode === 200) {
      Logger.log('レポートダウンロード成功。');
      return responseBody; // CSVデータを返す
    } else {
      Logger.log(`レポートダウンロード失敗: コード ${responseCode}, レスポンス: ${responseBody}`);
      return null;
    }
  } catch (e) {
    Logger.log('レポートダウンロード中にエラーが発生しました: ' + e.toString());
    return null;
  }
}

/**
 * 取得したCSVデータをGoogleスプレッドシートに書き込みます。
 * @param {string} spreadsheetId GoogleスプレッドシートのID
 * @param {string} csvData CSV形式のレポートデータ
 */
function writeToSpreadsheet(spreadsheetId, csvData) {
  const ss = SpreadsheetApp.openById(spreadsheetId);
  const sheet = ss.getActiveSheet();

  const data = Utilities.parseCsv(csvData);

  // ヘッダー行をスキップしてデータを追加
  // ユーザーの要件: 日付、キャンペーン名、表示回数（imp）、クリック数（click）、消化金額（cost）、コンバージョン数（cv）
  // APIから取得されるCSVのヘッダーは変動する可能性があるため、動的にインデックスを特定する
  const header = data[0];
  const dateIndex = header.indexOf('date');
  const campaignNameIndex = header.indexOf('campaign_name'); 
  const impIndex = header.indexOf('imp');
  const clickIndex = header.indexOf('click');
  const costIndex = header.indexOf('cost');
  const cvIndex = header.indexOf('cv');

  if (dateIndex === -1 || campaignNameIndex === -1 || impIndex === -1 || clickIndex === -1 || costIndex === -1 || cvIndex === -1) {
    Logger.log('必要なヘッダーが見つかりませんでした。CSVヘッダーを確認してください。');
    Logger.log('取得されたヘッダー: ' + header.join(', '));
    return;
  }

  const rows = [];
  for (let i = 1; i < data.length; i++) { // ヘッダー行をスキップ
    const row = data[i];
    rows.push([
      row[dateIndex],
      row[campaignNameIndex],
      parseFloat(row[impIndex] || 0),
      parseFloat(row[clickIndex] || 0),
      parseFloat(row[costIndex] || 0),
      parseFloat(row[cvIndex] || 0)
    ]);
  }

  if (rows.length > 0) {
    sheet.getRange(sheet.getLastRow() + 1, 1, rows.length, rows[0].length).setValues(rows);
    Logger.log(`${rows.length} 行のデータをスプレッドシートに追加しました。`);
  } else {
    Logger.log('追加するデータがありませんでした。');
  }
}
```

### 3.3. スクリプトの設定

貼り付けたスクリプトの冒頭にある設定項目を、ご自身の情報に合わせて編集します。

```javascript
// --- 設定項目 --- //
const SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'; // 2-2で控えたスプレッドシートIDに書き換える
const API_KEY_ID = 'YOUR_API_KEY_ID';         // 1-2で控えたAccess Keyに書き換える
const API_KEY_SECRET = 'YOUR_API_KEY_SECRET'; // 1-2で控えたSecret Keyに書き換える
const AD_ACCOUNT_ID = 'YOUR_AD_ACCOUNT_ID';   // 1-3で確認した広告アカウントIDに書き換える
```

### 3.4. 初回実行と承認

1.  スクリプトを保存します（フロッピーディスクのアイコンをクリック）。
2.  スクリプトエディタの上部にある関数選択メニューで `getLineAdsReport` を選択します。
3.  「実行」ボタンをクリックします。
4.  初回実行時には「承認が必要です」というダイアログが表示されます。「権限を確認」をクリックし、ご自身のGoogleアカウントを選択してください。
5.  「このアプリはGoogleで確認されていません」という警告が表示された場合は、「詳細」をクリックし、「（プロジェクト名）（安全ではないページ）に移動」を選択します。
6.  「（プロジェクト名）がGoogleアカウントへのアクセスをリクエストしています」という画面で、「許可」をクリックします。

これにより、スクリプトがGoogleスプレッドシートへの書き込みや外部APIへのアクセスを許可されます。

### 3.5. トリガーの設定（自動実行）

スクリプトを毎日自動で実行するためにトリガーを設定します。

1.  スクリプトエディタの左側にあるメニューから「トリガー」（時計のアイコン）を選択します。
2.  右下の「トリガーを追加」ボタンをクリックします。
3.  以下の通りに設定します。
    *   **実行する関数を選択**: `getLineAdsReport`
    *   **実行するデプロイを選択**: `Head`
    *   **イベントのソースを選択**: `時間主導型`
    *   **時間ベースのトリガーのタイプを選択**: `日付ベースのタイマー`
    *   **時刻を選択**: `午前 1 時～ 2 時` （など、任意の時間帯を選択）
4.  「保存」をクリックします。

これで、毎日指定した時間帯にスクリプトが自動実行され、前日のLINE広告データがスプレッドシートに追記されます。

## 4. 注意事項

*   **APIの仕様変更**: LINE Ads APIの仕様が変更された場合、スクリプトが正常に動作しなくなる可能性があります。エラーが発生した場合は、LINE Developersの公式ドキュメントをご確認ください。
*   **エラーの確認**: スクリプトの実行でエラーが発生した場合、スクリプトエディタの「実行数」メニューからログを確認できます。エラーメッセージを元に原因を調査してください。
*   **CSVヘッダーの変更**: APIから返されるCSVのヘッダー項目名（`campaign_name`など）が変更されると、データを正しく取得できなくなります。その場合は、`writeToSpreadsheet`関数内の`header.indexOf()`の部分を、新しいヘッダー名に合わせて修正する必要があります。
*   **JWSトークンの有効期限**: このスクリプトでは実行の都度JWSトークンを生成しているため、トークンの有効期限を気にする必要はありません。
