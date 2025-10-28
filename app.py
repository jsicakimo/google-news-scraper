from flask import Flask, render_template, request, send_file, url_for
import feedparser
import pandas as pd
from datetime import datetime
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import os
import traceback

try:
    from wordcloud import WordCloud, STOPWORDS

    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False
    print("⚠️ 未安裝 wordcloud 模組，詞雲功能將被禁用")

try:
    from snownlp import SnowNLP

    SENTIMENT_AVAILABLE = True
except ImportError:
    SENTIMENT_AVAILABLE = False
    print("⚠️ 未安裝 snownlp 模組，情感分析功能將被禁用")

# 🔧 確保 static 資料夾存在
os.makedirs("static", exist_ok=True)
print(f"✅ Static 資料夾路徑: {os.path.abspath('static')}")

app = Flask(__name__)


def build_rss_url(keyword):
    base = "https://news.google.com/rss/search"
    return f"{base}?q={keyword}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"


def fetch_rss_news(keyword, start_date, end_date, logic="AND"):
    """
    抓取 RSS 新聞，支援多關鍵字和 AND/OR 邏輯
    :param keyword: 關鍵字（可為逗號或空格分隔的多個關鍵字）
    :param start_date: 開始日期
    :param end_date: 結束日期
    :param logic: 邏輯運算符（AND/OR）
    :return: 新聞列表
    """
    keywords = [k.strip() for k in keyword.replace(",", " ").split() if k.strip()]
    results = []

    for kw in keywords:
        rss_url = build_rss_url(kw)
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            published = datetime(*entry.published_parsed[:6])
            if start_date <= published.date() <= end_date:
                news_item = {
                    "標題": entry.title,
                    "連結": entry.link,
                    "發布時間": published.strftime("%Y-%m-%d %H:%M:%S"),
                    "來源": entry.source.title if "source" in entry else "未知",
                    "關鍵字": kw,
                }
                results.append(news_item)

    # 根據邏輯運算符過濾結果
    if logic == "AND" and len(keywords) > 1:
        # 只保留包含所有關鍵字的新聞
        filtered_results = []
        for item in results:
            if all(kw in item["標題"] for kw in keywords):
                filtered_results.append(item)
        results = filtered_results

    return results


def generate_pie_chart(df):
    """生成圓餅圖並返回檔案名稱（相對於 static 資料夾）"""
    try:
        print("🎨 開始生成圓餅圖...")

        count_data = df["來源"].value_counts()
        print(f"📊 統計資料: {count_data.to_dict()}")

        # 建立圖表
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)

        # 設定中文字體
        plt.rcParams["font.sans-serif"] = [
            "Microsoft JhengHei",
            "SimHei",
            "Arial Unicode MS",
            "sans-serif",
        ]
        plt.rcParams["axes.unicode_minus"] = False

        # 生成顏色方案
        colors = plt.cm.Set3(range(len(count_data)))

        # 繪製圓餅圖
        wedges, texts, autotexts = ax.pie(
            count_data.values,
            labels=count_data.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=colors,
            textprops={"fontsize": 11},
            pctdistance=0.85,
        )

        # 設定標題
        ax.set_title("各新聞來源篇數統計", fontsize=18, pad=20, fontweight="bold")

        # 美化百分比文字
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")
            autotext.set_fontsize(11)

        # 添加圖例
        legend_labels = [f"{source}: {count}篇" for source, count in count_data.items()]
        ax.legend(
            legend_labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=11
        )

        # 確保圓餅圖是正圓形
        ax.axis("equal")

        plt.tight_layout()

        # 生成唯一的檔案名稱
        chart_filename = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        chart_path = os.path.join("static", chart_filename)

        print(f"💾 準備儲存圖表到: {os.path.abspath(chart_path)}")

        # 儲存圖表
        plt.savefig(chart_path, dpi=120, bbox_inches="tight", facecolor="white")
        plt.close(fig)

        # 驗證檔案是否成功創建
        if os.path.exists(chart_path):
            file_size = os.path.getsize(chart_path)
            print(f"✅ 圓餅圖已成功生成: {chart_path} (大小: {file_size} bytes)")
            return chart_filename
        else:
            print(f"❌ 錯誤：圖表檔案未能創建！")
            return None

    except Exception as e:
        print(f"❌ 生成圓餅圖時發生錯誤: {str(e)}")
        print(f"詳細錯誤訊息:\n{traceback.format_exc()}")
        return None


# def generate_trend_chart(df):
#     """生成時間趨勢圖並返回檔案名稱（相對於 static 資料夾）"""
#     try:
#         print("📈 開始生成時間趨勢圖...")

#         # 將發布時間轉換為日期格式
#         df["日期"] = pd.to_datetime(df["發布時間"]).dt.date

#         # 統計每日新聞數量
#         trend_data = df["日期"].value_counts().sort_index()
#         print(f"📊 時間趨勢資料: {trend_data.to_dict()}")

#         # 建立圖表
#         fig = plt.figure(figsize=(12, 6))
#         ax = fig.add_subplot(111)

#         # 繪製折線圖
#         ax.plot(
#             trend_data.index, trend_data.values, marker="o", linestyle="-", color="b"
#         )
#         ax.set_title("新聞數量時間趨勢")
#         ax.set_xlabel("日期")
#         ax.set_ylabel("新聞數量")
#         plt.xticks(rotation=45)

#         # 儲存圖表
#         chart_filename = "trend_chart.png"
#         chart_path = os.path.join("static", chart_filename)
#         plt.savefig(chart_path, bbox_inches="tight")
#         plt.close()

#         # 返回相對於 static 的檔案名稱
#         return chart_filename
#     except Exception as e:
#         print(f"❌ 生成時間趨勢圖失敗: {e}")
#         traceback.print_exc()
#         return None


def generate_word_cloud(df):
    """生成關鍵字雲並返回檔案名稱（相對於 static 資料夾）"""
    if not WORDCLOUD_AVAILABLE:
        print("⚠️ 詞雲功能未啟用，請安裝 wordcloud 模組")
        return None
    try:
        print("☁️ 開始生成關鍵字雲...")

        # 提取所有標題
        titles = " ".join(df["標題"].tolist())

        # 🔧 修復：正確建立停用詞集合
        # STOPWORDS.update() 返回 None，應該使用集合運算
        chinese_stopwords = {
            "的",
            "是",
            "在",
            "了",
            "和",
            "有",
            "也",
            "為",
            "與",
            "等",
            "將",
            "及",
            "或",
            "但",
            "而",
            "對",
            "於",
            "以",
            "中",
            "到",
            "從",
            "被",
            "把",
            "讓",
            "使",
            "由",
            "向",
            "就",
            "都",
            "要",
            "會",
            "能",
            "可",
            "不",
            "沒",
            "很",
            "更",
            "最",
            "非",
            "再",
            "又",
            "還",
            "已",
            "曾",
            "正",
            "該",
            "此",
            "其",
            "這",
            "那",
            "些",
            "個",
            "位",
            "名",
        }

        # 合併英文和中文停用詞
        # 正確寫法（返回集合）
        all_stopwords = STOPWORDS | chinese_stopwords
        
        # 🎨 嘗試多個可能的中文字體路徑（跨平台兼容）
        font_paths = [
            "C:\\Windows\\Fonts\\msjh.ttc",  # Windows - 微軟正黑體
            "C:\\Windows\\Fonts\\msyh.ttc",  # Windows - 微軟雅黑
            "/System/Library/Fonts/PingFang.ttc",  # macOS - 蘋方
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",  # Linux
            "msyh.ttc",  # 相對路徑
        ]

        font_path = None
        for path in font_paths:
            if os.path.exists(path):
                font_path = path
                print(f"✅ 找到字體檔案: {path}")
                break

        if not font_path:
            print("⚠️ 未找到中文字體，使用預設字體（可能無法正確顯示中文）")

        # 使用 wordcloud 生成詞雲
        wordcloud_params = {
            "width": 1200,
            "height": 600,
            "background_color": "white",
            "stopwords": all_stopwords,
            "max_words": 100,
            "relative_scaling": 0.3,
            "min_font_size": 10,
        }

        # 只在找到字體時才設定 font_path
        if font_path:
            wordcloud_params["font_path"] = font_path

        wordcloud = WordCloud(**wordcloud_params).generate(titles)

        # 🔧 生成唯一的檔案名稱（避免覆蓋）
        wordcloud_filename = f"wordcloud_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        wordcloud_path = os.path.join("static", wordcloud_filename)
        wordcloud.to_file(wordcloud_path)

        # 驗證檔案是否成功創建
        if os.path.exists(wordcloud_path):
            file_size = os.path.getsize(wordcloud_path)
            print(f"✅ 詞雲已成功生成: {wordcloud_path} (大小: {file_size} bytes)")
            return wordcloud_filename
        else:
            print(f"❌ 錯誤：詞雲檔案未能創建！")
            return None

    except Exception as e:
        print(f"❌ 生成關鍵字雲失敗: {e}")
        traceback.print_exc()
        return None


def analyze_sentiment(text):
    """
    分析文本的情感傾向
    :param text: 要分析的文本
    :return: 情感分數 (0-1)，越接近1表示越正面
    """
    if not SENTIMENT_AVAILABLE:
        return None
    try:
        s = SnowNLP(text)
        return s.sentiments
    except Exception as e:
        print(f"❌ 情感分析失敗: {e}")
        return None


def classify_sentiment(score):
    """
    根據情感分數分類
    :param score: 情感分數 (0-1)
    :return: 情感分類 ('正面', '中立', '負面')
    """
    if score is None:
        return "未知"
    if score >= 0.6:
        return "正面"
    elif score <= 0.4:
        return "負面"
    else:
        return "中立"


def analyze_news_sentiment(df):
    """
    分析新聞列表的情感傾向
    :param df: 新聞 DataFrame
    :return: 包含情感分析結果的 DataFrame
    """
    if not SENTIMENT_AVAILABLE:
        print("⚠️ 情感分析功能未啟用")
        return df

    try:
        print("💭 開始進行情感分析...")

        # 分析每條新聞的情感
        sentiment_scores = []
        sentiment_labels = []

        for title in df["標題"]:
            score = analyze_sentiment(title)
            sentiment_scores.append(score)
            sentiment_labels.append(classify_sentiment(score))

        df["情感分數"] = sentiment_scores
        df["情感分類"] = sentiment_labels

        print(f"✅ 情感分析完成")
        print(f"📊 情感分佈: {pd.Series(sentiment_labels).value_counts().to_dict()}")

        return df
    except Exception as e:
        print(f"❌ 情感分析失敗: {e}")
        traceback.print_exc()
        return df


def generate_sentiment_chart(df):
    """生成情感分析圖表並返回檔案名稱"""
    if not SENTIMENT_AVAILABLE or "情感分類" not in df.columns:
        print("⚠️ 無法生成情感分析圖表")
        return None

    try:
        print("📊 開始生成情感分析圖表...")

        # 統計情感分佈
        sentiment_counts = df["情感分類"].value_counts()
        print(f"📊 情感統計: {sentiment_counts.to_dict()}")

        # 建立圖表
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        # 設定中文字體
        plt.rcParams["font.sans-serif"] = [
            "Microsoft JhengHei",
            "SimHei",
            "Arial Unicode MS",
            "sans-serif",
        ]
        plt.rcParams["axes.unicode_minus"] = False

        # 定義顏色
        colors = {
            "正面": "#2ecc71",
            "中立": "#f39c12",
            "負面": "#e74c3c",
            "未知": "#95a5a6",
        }
        bar_colors = [colors.get(label, "#95a5a6") for label in sentiment_counts.index]

        # 繪製柱狀圖
        bars = ax.bar(
            sentiment_counts.index,
            sentiment_counts.values,
            color=bar_colors,
            edgecolor="black",
            linewidth=1.5,
        )

        # 設定標題和標籤
        ax.set_title("新聞情感分析分佈", fontsize=16, fontweight="bold", pad=20)
        ax.set_xlabel("情感分類", fontsize=12, fontweight="bold")
        ax.set_ylabel("新聞數量", fontsize=12, fontweight="bold")

        # 在柱子上添加數值
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontweight="bold",
                fontsize=11,
            )

        # 添加網格
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        ax.set_axisbelow(True)

        plt.tight_layout()

        # 生成唯一的檔案名稱
        chart_filename = f"sentiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        chart_path = os.path.join("static", chart_filename)

        # 儲存圖表
        plt.savefig(chart_path, dpi=120, bbox_inches="tight", facecolor="white")
        plt.close(fig)

        if os.path.exists(chart_path):
            file_size = os.path.getsize(chart_path)
            print(f"✅ 情感分析圖表已成功生成: {chart_path} (大小: {file_size} bytes)")
            return chart_filename
        else:
            print(f"❌ 錯誤：情感分析圖表檔案未能創建！")
            return None

    except Exception as e:
        print(f"❌ 生成情感分析圖表時發生錯誤: {str(e)}")
        print(f"詳細錯誤訊息:\n{traceback.format_exc()}")
        return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scrape", methods=["POST"])
def scrape():
    # 🔧 修改：使用 .get() 獲取表單資料，增加程式碼健壯性
    keyword = request.form.get("keyword", "").strip()
    start_date_str = request.form.get("start_date")
    end_date_str = request.form.get("end_date")
    logic = request.form.get("logic", "AND")

    if not all([keyword, start_date_str, end_date_str]):
        return render_template("index.html", error="請確保所有欄位都已填寫！")

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return render_template("index.html", error="日期格式不正確，請使用 YYYY-MM-DD 格式。")
    if start_date > end_date:
        return render_template("index.html", error="起始日期不能晚於結束日期。")

    # 抓取新聞
    news_items = fetch_rss_news(keyword, start_date, end_date, logic)
    df = pd.DataFrame(news_items)

    # 🔧 修復：如果找不到任何新聞，df 會是空的，直接返回結果頁面並顯示提示
    if df.empty:
        print("⚠️ 找不到符合條件的新聞，返回結果頁面。")
        return render_template("results.html", keyword=keyword, count=0, results=[])

    # 進行情感分析
    df = analyze_news_sentiment(df)

    # 🔧 修正：準備給 Chart.js 的圓餅圖數據，而不是生成圖片
    pie_chart_data = None
    if not df.empty:
        source_counts = df["來源"].value_counts()
        pie_chart_data = {
            "labels": source_counts.index.tolist(),
            "data": source_counts.values.tolist(),
        }

    # 🔧 新增：準備給 Chart.js 的時間趨勢圖數據
    trend_chart_data = None
    if not df.empty:
        df["日期"] = pd.to_datetime(df["發布時間"]).dt.date # 確保日期欄位存在
        trend_counts = df["日期"].value_counts().sort_index()
        trend_chart_data = {
            "labels": [date.strftime("%Y-%m-%d") for date in trend_counts.index], # 日期格式化為字串
            "data": [int(count) for count in trend_counts.values], # 轉換為 Python 原生 int
        }

    # 🔧 新增：準備給 Chart.js 的情感長條圖數據
    sentiment_chart_data = None
    if "情感分類" in df.columns:
        sentiment_counts = df["情感分類"].value_counts()
        # 為了固定的顏色順序，我們定義一個標籤順序
        # 確保 '未知' 情感分類也包含在內，即使沒有數據，以便顏色映射一致
        # 這裡的 labels_order 應該與 classify_sentiment 函式中的分類一致
        labels_order = ["正面", "中立", "負面", "未知"]
        chart_labels = [label for label in labels_order if label in sentiment_counts.index]
        # 🔧 修正：將 numpy.int64 轉換為 python 原生的 int
        chart_data = [int(sentiment_counts[label]) for label in chart_labels]
        sentiment_chart_data = {
            "labels": chart_labels,
            "data": chart_data,
        }

    # 生成其他圖表
    # pie_chart = generate_pie_chart(df) # 不再需要生成靜態圓餅圖
    # trend_chart = generate_trend_chart(df) # 不再需要生成靜態趨勢圖
    wordcloud = generate_word_cloud(df)
    # sentiment_chart = generate_sentiment_chart(df) # 不再需要生成靜態情感圖

    # 儲存為 Excel
    file_name = f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(os.path.join("static", file_name), index=False)

    # 獲取所有新聞來源
    sources = df["來源"].unique().tolist()

    # 計算情感統計
    sentiment_stats = {}
    if "情感分類" in df.columns:
        sentiment_counts = df["情感分類"].value_counts()
        sentiment_stats = sentiment_counts.to_dict()

    # 將 DataFrame 轉換回列表，包含情感分析結果
    results_with_sentiment = df.to_dict("records")

    return render_template(
        "results.html",
        keyword=keyword,
        results=results_with_sentiment,
        count=len(results_with_sentiment),
        file_name=file_name,
        pie_chart_data=pie_chart_data,
        trend_chart_data=trend_chart_data, # 傳遞數據
        wordcloud=wordcloud,
        sentiment_chart_data=sentiment_chart_data, # 傳遞數據
        sentiment_stats=sentiment_stats,
        sources=sources,
    )


@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join("static", filename), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)