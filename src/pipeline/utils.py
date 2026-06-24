import random
import pandas as pd
import os
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

async def human_scroll(page):
    for i in range(random.randint(1, 3)):
        await page.mouse.wheel(0, random.randint(300, 800))

def load_urls(filename, start_from=0):
    urls = []
    path = f"data/{filename}.txt"
    with open(path) as f:
        for line in f:
            idx, url = line.strip().split("|", 1)
            if int(idx) >= start_from:
                urls.append((int(idx), url))
    return urls

def save_progress(idx):
    with open("progress.txt", "w") as f:
        f.write(f"last_idx={idx}")

def load_progress():
    try:
        with open("progress.txt") as f:
            return int(f.read().split("=")[1])
    except FileNotFoundError:
        return 0


async def save_record(data, name):
    df = pd.DataFrame(data)
    path = f"data/{name}.csv"
    df.to_csv(f"{path}", mode="a", header=not os.path.exists(
        f"{path}"), index=False)
    print(f"[SUCCESS] Appended {len(data)} records to {name}.csv")


def save_urls_batch(batch, start_idx, filename):
    path = f"data/{filename}"
    if not batch:
        return
    with open(path, "a", encoding="utf-8") as f:
        for i, url in enumerate(batch, start=start_idx):
            f.write(f"{i}|{url}\n")

async def log_error(page, prefix, filename, content ,e, idx=0):
    
    if isinstance(e, PlaywrightTimeoutError):
        print(f"[WARN] Timeout accessing: {content}")
        err_type = "Timeout"
        with open(f"{filename}.txt", "a") as f:
            f.write(f"{content} | {idx} | {err_type} \n")
    else:
        await page.screenshot(path=f"screenshot/error/{prefix}_{content}.png", animations='disabled')
        print(f"[ERROR] Failed to scrape: {content}")
        err_type = type(e).__name__ if e else "Unknown"
        with open(f"{filename}.txt", "a") as f:
            f.write(f"{content} | {e}\n")
