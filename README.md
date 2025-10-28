# Google 新聞 RSS 擷取工具

## 📋 專案說明
這是一個基於 Flask 的網頁應用程式，可以從 Google 新聞 RSS 擷取指定關鍵字和日期範圍的新聞，並提供統計圖表和 Excel 下載功能。

## ✨ 主要功能
- 🔍 關鍵字搜尋台灣新聞
- 📅 自訂日期範圍篩選
- 📊 自動生成新聞來源統計圖表
- 📁 匯出 Excel 檔案
- 🎨 美觀的網頁介面

## 🚀 安裝步驟

### 1. 安裝 Python
確保已安裝 Python 3.8 或以上版本

### 2. 安裝相依套件
```bash
pip install -r requirements.txt
```

### 3. 執行應用程式
```bash
python app.py
```

### 4. 開啟瀏覽器
訪問 `http://127.0.0.1:5000`

## 📦 專案結構
```
google_news_rss_scraper/
│
├── app.py                 # 主程式
├── requirements.txt       # 相依套件清單
├── README.md             # 說明文件
│
├── templates/            # HTML 模板
│   ├── index.html       # 首頁
│   └── results.html     # 結果頁面
│
└── static/              # 靜態檔案（圖表儲存位置）
```

## 🛠️ 技術棧
- **後端**: Flask
- **資料處理**: Pandas
- **圖表**: Matplotlib
- **RSS 解析**: Feedparser
- **前端**: Bootstrap 5

## 📝 使用說明
1. 在首頁輸入搜尋關鍵字
2. 選擇起始和結束日期
3. 點擊「開始擷取新聞」
4. 查看結果頁面的統計圖表和新聞列表
5. 下載 Excel 檔案進行進一步分析

## ⚠️ 注意事項
- 建議選擇較短的日期範圍以獲得更精確的結果
- 圖表檔案會自動儲存在 `static/` 資料夾
- Excel 檔案會儲存在專案根目錄

## 📧 問題回報
如有任何問題或建議，歡迎回報！

---
開發日期: 2025年10月
