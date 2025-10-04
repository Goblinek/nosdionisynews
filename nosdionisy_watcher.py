import requests
from bs4 import BeautifulSoup
import os
import textwrap

BLOG_URL = "https://nosdionisy.com/blog"
WEBHOOK_URL = "https://discord.com/api/webhooks/1423962434426769511/6UCWwp_L4-KApsmPPgy3cWA7Yn7UbUTN4hrm3kbBazENlmbmVa_umj2PWW1w5Sc5i6je"  # vlož sem tu svou URL
NEWS_FILE = "last_news.txt"

def get_last_news():
    if not os.path.exists(NEWS_FILE):
        return ""
    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def save_news(content):
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        f.write(content.strip())

def extract_last_article():
    response = requests.get(BLOG_URL)
    if response.status_code != 200:
        print("❌ Error fetching blog page:", response.status_code)
        return None, None

    soup = BeautifulSoup(response.text, "html.parser")

    # najdeme první článek na blogu
    article_link = soup.find("a", href=True)
    if not article_link:
        print("❌ No article link found.")
        return None, None

    article_url = article_link["href"]
    if not article_url.startswith("http"):
        article_url = "https://nosdionisy.com" + article_url

    article_page = requests.get(article_url)
    if article_page.status_code != 200:
        print("❌ Error fetching article page:", article_page.status_code)
        return None, None

    article_soup = BeautifulSoup(article_page.text, "html.parser")

    title_tag = article_soup.find("h1")
    title = title_tag.text.strip() if title_tag else "Untitled"

    paragraphs = article_soup.find_all("p")
    body = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

    full_text = f"{body}"
    return article_url, title, full_text

def send_to_discord(title, url, body):
    # Discord embed má limit 6000 znaků celkem, 2000 na pole
    chunks = textwrap.wrap(body, 1900, replace_whitespace=False)

    for i, chunk in enumerate(chunks, 1):
        embed = {
            "title": title if i == 1 else f"{title} (část {i})",
            "url": url,
            "description": chunk,
            "color": 0x3498db
        }

        payload = {"embeds": [embed]}
        response = requests.post(WEBHOOK_URL, json=payload)

        print(f"📤 Sending embed {i} → status {response.status_code}")
        if response.status_code not in (200, 204):
            print("❌ Error response:", response.text)
            return False
    return True

def check_blog():
    article_url, title, article = extract_last_article()
    if not article:
        print("❌ No article extracted.")
        return

    last_news = get_last_news()
    if article_url != last_news:
        if send_to_discord(title, article_url, article):
            print("✅ New article sent to Discord.")
            save_news(article_url)
        else:
            print("❌ Failed to send message to Discord.")
    else:
        print("ℹ️ No new article detected.")

if __name__ == "__main__":
    check_blog()
