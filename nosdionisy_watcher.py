import requests
from bs4 import BeautifulSoup
import os

BLOG_URL = "https://nosdionisy.com/blog"
WEBHOOK_URL = "https://discord.com/api/webhooks/1423962434426769511/6UCWwp_L4-KApsmPPgy3cWA7Yn7UbUTN4hrm3kbBazENlmbmVa_umj2PWW1w5Sc5i6je"
NEWS_FILE = "last_news.txt"

def get_last_news():
    if not os.path.exists(NEWS_FILE):
        return ""
    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def save_news(content):
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        f.write(content.strip())

def extract_article():
    response = requests.get(BLOG_URL)
    if response.status_code != 200:
        print("Error fetching the blog page.")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Try to find the first blog post container
    post = soup.find("div", class_="blog-post") or soup.find("div", class_="post") or soup.find("article")
    if not post:
        print("No blog post found.")
        return None

    # Extract title and content
    title_tag = post.find("h1") or post.find("h2") or post.find("h3")
    title = title_tag.text.strip() if title_tag else "Untitled"

    paragraphs = post.find_all("p")
    content = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())

    full_text = f"{title}\n\n{content}"
    return full_text

def send_to_discord(message):
    payload = {
        "content": f"📰 **New Blog Post**\n\n{message[:1900]}"  # Discord max is 2000 chars
    }
    response = requests.post(WEBHOOK_URL, json=payload)
    return response.status_code == 204

def check_blog():
    article = extract_article()
    if not article:
        return

    last_news = get_last_news()
    if article != last_news:
        if send_to_discord(article):
            print("New article sent to Discord.")
            save_news(article)
        else:
            print("Failed to send message to Discord.")
    else:
        print("No new article detected.")

if __name__ == "__main__":
    check_blog()
