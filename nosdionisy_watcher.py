import requests

BLOG_URL = "https://nosdionisy.com/blog"
WEBHOOK_URL = "https://discord.com/api/webhooks/1423962434426769511/6UCWwp_L4-KApsmPPgy3cWA7Yn7UbUTN4hrm3kbBazENlmbmVa_umj2PWW1w5Sc5i6je"
EMPTY_TEXT = "No news yet"

def check_blog():
    response = requests.get(BLOG_URL)
    if response.status_code != 200:
        print("Error fetching the page.")
        return

    if EMPTY_TEXT not in response.text:
        data = {
            "content": f"🆕 New update on the NosDionisy blog! Check it out: {BLOG_URL}"
        }
        r = requests.post(WEBHOOK_URL, json=data)
        if r.status_code == 204:
            print("Message sent to Discord.")
        else:
            print(f"Error sending message: {r.status_code}")
    else:
        print("No news yet.")

if __name__ == "__main__":
    check_blog()
