import os
import re
import requests

URL = "https://pass.uspace.city/b/823ae623"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("開始抓取...")

r = requests.get(URL, headers=headers, timeout=30)
print("HTTP Status:", r.status_code)

r.raise_for_status()

html = r.text
print("HTML 長度：", len(html))

match = re.search(r"同類型車位僅剩\s*(\d+)\s*個", html)

if not match:
    print("找不到剩餘車位數")
    raise SystemExit(1)

count = int(match.group(1))
print(f"目前剩餘車位：{count}")

STATE_FILE = "last_count.txt"

# 讀取上一次紀錄
last = None
if os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE, "r") as f:
            last = int(f.read().strip())
    except:
        last = None

print("上次車位：", last)

# 第一次執行（999 或沒有紀錄）
if last is None or last == 999:
    print("第一次執行，只記錄，不通知")

# 車位有變化，而且 <=60
elif count != last and count <= 60:
    webhook = os.environ["DISCORD_WEBHOOK"]

    r = requests.post(
        webhook,
        json={
            "content": f"🚨 USPACE 士林商城(B1~B2) 剩餘 {count} 個車位！（原本 {last} 個）"
        },
        timeout=60
    )

    print("Discord 回應：", r.status_code)
    print("Discord 通知已送出")

else:
    print("車位沒變或大於60，不通知")

# 更新最新車位數
with open(STATE_FILE, "w") as f:
    f.write(str(count))
