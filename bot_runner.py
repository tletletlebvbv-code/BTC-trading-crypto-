"""
BTC Discord Bot — GitHub Actions version
==========================================
Runs ONCE per invocation (GitHub Actions calls this on a schedule, e.g. every 5 min).
No server needed — completely free via GitHub Actions.

- Sends BTC price every run (every 5 min)
- Sends London / New York session summaries at start/mid/end (Asia skipped)
- Sends fresh Trump+crypto news (published in the last ~7 minutes)
"""

import os
import requests
import feedparser
from datetime import datetime, timezone

# ---------------- CONFIG ----------------

WEBHOOK_URL_DEFAULT = os.getenv("WEBHOOK_URL_DEFAULT", "")
WEBHOOK_URL_PRICE = os.getenv("WEBHOOK_URL_PRICE", "") or WEBHOOK_URL_DEFAULT
WEBHOOK_URL_SESSIONS = os.getenv("WEBHOOK_URL_SESSIONS", "") or WEBHOOK_URL_DEFAULT
WEBHOOK_URL_NEWS = os.getenv("WEBHOOK_URL_NEWS", "") or WEBHOOK_URL_DEFAULT

# Session hours in UTC (shift ~1h during EU/US daylight-saving changes)
LONDON_START_UTC = 7
LONDON_END_UTC = 16
NY_START_UTC = 13
NY_END_UTC = 22

NEWS_QUERY = "Trump bitcoin OR crypto OR cryptocurrency"
NEWS_RSS_URL = f"https://news.google.com/rss/search?q={requests.utils.quote(NEWS_QUERY)}&hl=en-US&gl=US&ceid=US:en"
NEWS_FRESHNESS_MINUTES = 7  # only send news published within this window

# ---------------- HELPERS ----------------

def send_discord(webhook_url: str, embed: dict = None, content: str = None):
    if not webhook_url:
        print("[WARN] No webhook configured, skipping message.")
        return
    payload = {}
    if content:
        payload["content"] = content
    if embed:
        payload["embeds"] = [embed]
    r = requests.post(webhook_url, json=payload, timeout=15)
    if r.status_code >= 300:
        print(f"[ERROR] Discord send failed ({r.status_code}): {r.text}")


def get_btc_price():
    # CoinGecko — works reliably from GitHub Actions runners (Binance blocks them).
    r = requests.get(
        "https://api.coingecko.com/api/v3/coins/bitcoin"
        "?localization=false&tickers=false&market_data=true"
        "&community_data=false&developer_data=false&sparkline=false",
        timeout=15,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    data = r.json()["market_data"]
    price = float(data["current_price"]["usd"])
    change_pct = float(data["price_change_percentage_24h"])
    high = float(data["high_24h"]["usd"])
    low = float(data["low_24h"]["usd"])
    return price, change_pct, high, low


# ---------------- PRICE ----------------

def do_price():
    try:
        price, change_pct, high, low = get_btc_price()
        arrow = "🟢" if change_pct >= 0 else "🔴"
        embed = {
            "title": f"{arrow} BTC/USDT: ${price:,.2f}",
            "description": f"تغيير 24h: {change_pct:+.2f}%\nأعلى: ${high:,.2f}  |  أدنى: ${low:,.2f}",
            "color": 0x2ecc71 if change_pct >= 0 else 0xe74c3c,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        send_discord(WEBHOOK_URL_PRICE, embed=embed)
    except Exception as e:
        print(f"[ERROR] price: {e}")


# ---------------- SESSIONS ----------------

def do_sessions(now_utc: datetime):
    if now_utc.minute >= 5:
        return  # only fire in the first 5-min window of the target hour

    hour = now_utc.hour
    london_mid = (LONDON_START_UTC + LONDON_END_UTC) // 2
    ny_mid = (NY_START_UTC + NY_END_UTC) // 2

    mapping = {
        LONDON_START_UTC: ("London", "بداية"),
        london_mid: ("London", "منتصف"),
        LONDON_END_UTC: ("London", "نهاية"),
        NY_START_UTC: ("New York", "بداية"),
        ny_mid: ("New York", "منتصف"),
        NY_END_UTC: ("New York", "نهاية"),
    }
    if hour not in mapping:
        return

    session_name, stage = mapping[hour]
    try:
        price, change_pct, high, low = get_btc_price()
        desc = f"BTC: ${price:,.2f} ({change_pct:+.2f}%)\nأعلى (24h): ${high:,.2f} | أدنى: ${low:,.2f}"
    except Exception as e:
        desc = "(تعذر جلب السعر)"
        print(f"[ERROR] session price: {e}")

    embed = {
        "title": f"📊 موجز جلسة {session_name} — {stage}",
        "description": desc,
        "color": 0x3498db,
        "timestamp": now_utc.isoformat(),
    }
    send_discord(WEBHOOK_URL_SESSIONS, embed=embed)


# ---------------- NEWS ----------------

def do_news(now_utc: datetime):
    try:
        feed = feedparser.parse(NEWS_RSS_URL)
        for entry in feed.entries[:10]:
            if not hasattr(entry, "published_parsed") or entry.published_parsed is None:
                continue
            published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            age_minutes = (now_utc - published).total_seconds() / 60
            if 0 <= age_minutes <= NEWS_FRESHNESS_MINUTES:
                embed = {
                    "title": f"📰 {entry.title}",
                    "url": entry.link,
                    "color": 0xf1c40f,
                    "timestamp": published.isoformat(),
                }
                send_discord(WEBHOOK_URL_NEWS, embed=embed)
    except Exception as e:
        print(f"[ERROR] news: {e}")


# ---------------- MAIN ----------------

def main():
    now_utc = datetime.now(timezone.utc)
    print(f"Run at {now_utc.isoformat()}")
    do_price()
    do_sessions(now_utc)
    do_news(now_utc)


if __name__ == "__main__":
    main()
