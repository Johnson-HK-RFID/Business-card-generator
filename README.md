# EmbuilDed 名片工作室

一個不需要修改程式碼的名片編輯器。使用者在表單輸入資料，名片會即時更新，並可下載約 300 DPI PNG 或 90 × 43.5 mm 雙面 PDF。版面採用參考圖的長形比例；送印前請確認尺寸與出血要求。

正面隱藏原 Logo 下方的 Built World Intelligence 小字，保留主標誌；QR Code 帶有中央金色 E 圖標、四模組留白及 H 級錯誤更正。背面沿用 TRACI 原圖的主標誌輪廓，五項文字獨立排版，底部附註的「·」或「|」會顯示為金色分隔線。員工已有的瀏覽器資料會繼續保留。

## 立即使用

直接雙擊 `index.html` 即可開啟。首次載入 QR Code、PNG、PDF 輸出功能時需要網絡連線。

本機 `file://` 匯出已使用內嵌圖片與獨立的空白文件，無需關閉瀏覽器安全限制或啟動網站伺服器。`assets/export-resources.js` 必須一起保留。更改 `styles.css` 或 Logo 圖片後，請執行 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools/build-export-resources.ps1` 更新匯出素材；此命令只為該次程序設定執行原則。

維護測試：開啟 `index.html?export-test=1` 可在同一頁測試正常本機檔案權限下的正反面 PNG 與雙面 PDF 生成，不需放寬 Chrome 安全設定。這個模式不修改員工資料。

## 分享給公司同事

### 從 GitHub 部署到 Vercel

目標倉庫：https://github.com/Johnson-HK-RFID/Business-card-generator

在 Vercel 選擇 Add New → Project，匯入以上 GitHub 倉庫。Framework Preset 使用 Other，Root Directory 使用倉庫根目錄；`vercel.json` 已設定不需建置、直接提供根目錄靜態網站。无需環境變數或資料庫。按 Deploy 後，以 Vercel 實際產生的網址分享給同事或外部使用者。

若外部訪客遇到 Vercel 登入要求，請檢查該部署的 Deployment Protection 與分享設定。網站目前沒有員工登入功能，取得可公開存取網址的人均可使用編輯器；資料仍各自儲存在瀏覽器，不是多人同步編輯。

`.gitignore` 僅允許網站原始碼、所需 Logo、轉換腳本與測試程式入庫，排除本機瀏覽器設定、測試下載與員工匯出檔。`.vercelignore` 額外排除測試工具、原始 JPG 與開發文件。

設定參考：https://vercel.com/docs/project-configuration/vercel-json

### 最快方式：放到現有網站

把整個資料夾上傳到公司網站的一個目錄，例如 `https://tools.embuilded.com/name-card/`。這是一個純前端工具，不需要資料庫。

每位同事可填寫自己的資料，資料只會自動儲存在各自的瀏覽器。按「複製分享連結」可以把已填好的資料放入網址，交給別人繼續編輯。

### 免費靜態部署

也可以將檔案拖放到 Cloudflare Pages、Netlify 或 GitHub Pages。部署後，全公司只需開啟同一個網址。

## 關於「多人即時協作」

目前版本是「輸入即時預覽」，而不是多人同時編輯同一份記錄。若要中央員工名錄、登入權限、多人同步和管理員鎖定品牌欄位，需要再接 Supabase/Firebase 或公司內部 API。介面已把資料集中成簡單 JSON，方便下一階段接後端。

## 檔案

- `index.html`：頁面結構
- `styles.css`：版面、名片設計與列印樣式
- `app.js`：即時編輯、QR Code、下載與分享功能
- `assets/embuilded-logo.png`：由指定 EmbuilDed 原圖提取的透明 Logo
- `assets/traci-logo.png`：由指定 TRACI 原圖提取的透明原色 Logo
- `assets/traci-logo-on-dark.png`：保留原字形與黃色、供深色背面使用的白字版本
- `tools/convert-logos.ps1`：可從兩張原始 JPG 重新產生以上透明素材
