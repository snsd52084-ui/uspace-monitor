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
    print(html[:1000])  # 印出前1000個字方便檢查
    raise SystemExit(1)

count = int(match.group(1))
print(f"目前剩餘車位：{count}")

if count <= 60:
    webhook = os.environ["DISCORD_WEBHOOK"]

    r = requests.post(
        webhook,
        json={
            "content": f"🚨 USPACE 士林商城(B1~B2) 剩餘 {count} 個車位！"
        },
        timeout=60
    )

    print("Discord 回應：", r.status_code)
    print("Discord 通知已送出")
else:
    print("尚未低於60個，不通知")
