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

# 讀取上一次的數字
last = None
if os.path.exists("last_count.txt"):
    with open("last_count.txt", "r") as f:
        try:
            last = int(f.read().strip())
        except:
            pass

print("上次車位：", last)

# 只有數量改變且 <=60 才通知
if count <= 60 and count != last:
    webhook = os.environ["DISCORD_WEBHOOK"]

    r = requests.post(
        webhook,
        json={
            "content": f"🚨 USPACE 士林商城(B1~B2) 剩餘 {count} 個車位！"
        },
        timeout=60
    )

    print("Discord 回應：", r.status_code)

else:
    print("車位沒變，不通知")

# 更新記錄
with open("last_count.txt", "w") as f:
    f.write(str(count))
