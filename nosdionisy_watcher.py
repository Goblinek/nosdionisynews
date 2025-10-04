import requests
import os

BLOG_URL = "https://nosdionisy.com/blog"
WEBHOOK_URL = "https://discord.com/api/webhooks/1423962434426769511/6UCWwp_L4-KApsmPPgy3cWA7Yn7UbUTN4hrm3kbBazENlmbmVa_umj2PWW1w5Sc5i6je"
EMPTY_TEXT = "No news yet"
NEWS_FILE = "last_news.txt"

def get_last_news():
    if not os.path.exists(NEWS_FILE):
        return ""
    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def save_news(content):
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        f.write(content.strip())

def check_blog():
    response = requests.get(BLOG_URL)
    if response.status_code != 200:
        print("Error fetching the page.")
        return

    if EMPTY_TEXT in response.text:
        print("No news yet.")
        return

    current_news = response.text.strip()
    last_news = get_last_news()

    if current_news != last_news:
        data = {
            "content": f"🆕 New update on the NosDionisy blog! Check it out: {BLOG_URL}"
        }
        r = requests.post(WEBHOOK_URL, json=data)
        if r.status_code == 204:
            print("Message sent to Discord.")
            save_news(current_news)
        else:
            print(f"Error sending message: {r.status_code}")
    else:
        print("No change detected.")

if __name__ == "__main__":
    check_blog()
