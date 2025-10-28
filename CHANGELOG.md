# 更新日誌

## [v3.1] - 2025-10-27

### 🐛 Bug 修復

#### 詞雲 Stopwords Bug（重大修復）

**問題：** 詞雲的停用詞設定失效，導致生成的詞雲包含大量無意義的詞（如「的」、「是」、「在」等）。

**原因：** 使用了 `STOPWORDS.update()` 方法，該方法返回 `None` 而非更新後的集合。

**修復：**
```python
# 修復前（錯誤）
stopwords=STOPWORDS.update(["的", "是", "在", "了", "和", "有", "也", "為"])
# 結果：stopwords = None ❌

# 修復後（正確）
chinese_stopwords = {"的", "是", "在", "了", ...}
all_stopwords = STOPWORDS | chinese_stopwords
# 結果：stopwords = 完整的停用詞集合 ✅
```

**影響範圍：** `generate_word_cloud()` 函數

**相關檔案：**
- `app.py` (第 199-325 行)
- `BUGFIX_WORDCLOUD.md` (詳細修復報告)

---

### ✨ 功能改進

#### 1. 擴充中文停用詞庫

- **修復前：** 8 個中文停用詞
- **修復後：** 50+ 個中文停用詞

新增的停用詞類別：
- 助詞：的、是、在、了、和、有、也、為
- 連接詞：與、等、將、及、或、但、而
- 介詞：對、於、以、中、到、從、被、把、讓、使、由、向
- 副詞：就、都、要、會、能、可、不、沒、很、更、最、非、再、又、還、已、曾、正
- 代詞：該、此、其、這、那、些、個、位、名

#### 2. 跨平台字體支援

新增多個字體路徑自動偵測：

```python
font_paths = [
    "C:\\Windows\\Fonts\\msjh.ttc",      # Windows - 微軟正黑體
    "C:\\Windows\\Fonts\\msyh.ttc",      # Windows - 微軟雅黑
    "/System/Library/Fonts/PingFang.ttc", # macOS - 蘋方
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",  # Linux
    "msyh.ttc",  # 相對路徑
]
```

**優點：**
- ✅ 自動偵測可用字體
- ✅ 支援 Windows / macOS / Linux
- ✅ 找不到字體時優雅降級

#### 3. 唯一檔案名稱

**修復前：**
```python
wordcloud_path = os.path.join("static", "wordcloud.png")
# 問題：每次都覆蓋同一個檔案
```

**修復後：**
```python
wordcloud_filename = f"wordcloud_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
# 優點：每次生成唯一檔名，不會覆蓋
```

#### 4. 增強錯誤處理

新增：
- ✅ 檔案存在驗證
- ✅ 檔案大小檢查
- ✅ 詳細的日誌輸出
- ✅ 字體偵測狀態提示

#### 5. 優化詞雲品質

| 參數 | 修復前 | 修復後 |
|------|--------|--------|
| 寬度 | 800 | 1200 |
| 高度 | 400 | 600 |
| 最大詞數 | 未設定 | 100 |
| 相對縮放 | 未設定 | 0.3 |
| 最小字體 | 未設定 | 10 |

---

### 📦 依賴更新

#### requirements.txt

新增：
```
wordcloud==1.9.3
```

**注意：** 如果使用 Python 3.14，可能需要安裝 Visual C++ Build Tools 或使用較舊的 Python 版本（3.11/3.12）。

---

### 🧪 測試

新增測試檔案：

1. **test_stopwords_fix.py** - 驗證 stopwords 修復邏輯
   ```bash
   python test_stopwords_fix.py
   ```

2. **test_wordcloud.py** - 完整詞雲功能測試
   ```bash
   python test_wordcloud.py
   ```

---

### 📝 文檔

新增文檔：

1. **BUGFIX_WORDCLOUD.md** - 詳細的 bug 修復報告
2. **CHANGELOG.md** - 本更新日誌

---

### 🔄 向後兼容性

✅ **完全向後兼容**

- 所有現有功能保持不變
- 如果 wordcloud 未安裝，功能會自動降級
- 不影響其他圖表生成功能

---

### 📊 修復效果對比

#### 修復前的詞雲
- ❌ 包含大量「的」、「是」、「在」等無意義詞
- ❌ 關鍵資訊被淹沒
- ❌ 視覺效果差

#### 修復後的詞雲
- ✅ 正確過濾停用詞
- ✅ 突出關鍵詞彙
- ✅ 視覺效果佳
- ✅ 更高解析度（1200x600）

---

### 🎯 下一步計劃

建議的後續改進（未包含在此版本）：

1. 使用 jieba 分詞改進中文詞雲
2. 新增詞雲顏色主題選項
3. 支援自訂停用詞列表
4. 新增詞雲互動功能
5. 優化大量新聞的處理效能

---

### 👥 貢獻者

- Bug 發現與修復：AI Assistant
- 測試與驗證：AI Assistant

---

### 📧 問題回報

如有任何問題或建議，歡迎回報！

---

**完整修復報告請參閱：** [BUGFIX_WORDCLOUD.md](BUGFIX_WORDCLOUD.md)

