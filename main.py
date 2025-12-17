import feedparser
import datetime
import os

# 1. 設定新聞來源
feeds = {
    "Yahoo 財經焦點": "https://tw.stock.yahoo.com/rss?category=tw-market",
    "鉅亨網頭條": "https://news.cnyes.com/rss/headline",
    "MoneyDJ 理財網": "https://www.moneydj.com/rss/fnews.htm"
}

# 2. 生成 HTML
def generate_html(news_data):
    # 設定為台灣時間 (UTC+8)
    tz = datetime.timezone(datetime.timedelta(hours=8))
    today = datetime.datetime.now(tz).strftime("%Y-%m-%d")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>每日財經早報 ({today})</title>
        <style>
            body {{ font-family: -apple-system, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 15px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
            h1 {{ text-align: center; color: #2c3e50; font-size: 22px; margin-bottom: 20px; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            .source-title {{ font-size: 18px; font-weight: bold; color: #e67e22; margin-top: 25px; margin-bottom: 10px; border-left: 4px solid #e67e22; padding-left: 10px; }}
            .news-item {{ border-bottom: 1px solid #eee; padding: 12px 0; }}
            .news-item:last-child {{ border-bottom: none; }}
            .news-title {{ font-size: 16px; font-weight: 600; display: block; margin-bottom: 5px; color: #2980b9; text-decoration: none; }}
            .news-summary {{ font-size: 14px; color: #666; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
            .footer {{ text-align: center; font-size: 12px; color: #999; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📈 每日財經早報<br><span style="font-size:14px; color:#7f8c8d">{today}</span></h1>
    """

    for source, items in news_data.items():
        html_content += f'<div class="source-title">{source}</div>'
        for item in items[:5]: 
            summary = item.get('summary', '無摘要').split('<')[0]
            html_content += f"""
            <div class="news-item">
                <a href="{item['link']}" target="_blank" class="news-title">{item['title']}</a>
                <div class="news-summary">{summary}</div>
            </div>
            """
            
    html_content += """
            <div class="footer">每日 07:30 自動更新 • GitHub Actions</div>
        </div>
    </body>
    </html>
    """
    return html_content

def main():
    all_news = {}
    for name, url in feeds.items():
        try:
            feed = feedparser.parse(url)
            all_news[name] = feed.entries
        except:
            pass
    
    html = generate_html(all_news)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
