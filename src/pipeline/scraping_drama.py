from playwright.async_api import async_playwright
from playwright.async_api  import TimeoutError as PlaywrightTimeoutError
import asyncio
import pandas as pd
import random
import os
from tqdm.asyncio import tqdm
from pipeline.utils import save_record, save_urls_batch, human_scroll, log_error, save_progress, load_progress, load_urls
from pipeline.utils_getdetails import scraper


async def collect_url(page, filtered_url, filename, index=0, pg_num=1):
    urls_batch = []
    page_num = pg_num
    url_count = 0
    idx = index
    timeout_streak = 0
    saved_page = 0
    while True:
        ## Pagination handler
        print(f"[NAV] Go to page {page_num}")

        try:
            await page.goto(f"{filtered_url}&page={page_num}", wait_until='domcontentloaded', timeout=50000)
            await human_scroll(page)

            # await page.wait_for_selector("h6", timeout=10000)
            if await page.get_by_role("heading", level=6).count()==0:
                print("[FINISH] No items could be found. URL collecting is done...")
                break
            headings = page.get_by_role("heading", level=6)
            count_ = await headings.count()

            # Looping too get each drama's link
            for i in range(count_):
                title = headings.nth(i).locator("a").first
                link = await title.get_attribute("href")
                if link:
                    urls_batch.append(link)
                else:
                    title_ = await title.inner_text()
                    with open(f"failed_url.txt", "a") as f:
                        f.write(f"{title_}\n")
                    count_ -= 1    
                    print(f"[ERROR] Failed to scrape {title_}")

        except Exception as e:
            if isinstance(e,PlaywrightTimeoutError):
                print(f"[WARN] Timeout accessing: {page_num}")
                timeout_streak += 1
                if timeout_streak >= 3:
                    await log_error(page, "page", "failed_page", page_num, e, idx)
                    print(
                        f"[TERMINATED] Hit 3 timeouts in a row. Stopping to protect IP")
                    print(f"Last page: {page_num}")
                    break
            else:
                await log_error(page, "page", "failed_page", page_num, e)
            ## Add up page num 
                page_num+=1
            continue

        url_count += count_
        print(f"[INFO] Total scraping url: {url_count}")
        # Safety measure
        if page_num % 3==0:
            save_urls_batch(urls_batch,idx,filename)
            saved_page = page_num
            idx += len(urls_batch)
            urls_batch.clear()
            print(f"\n[SAVE] URLs saved up to page {page_num} & Index {idx}\n")

        page_num += 1
        
        await asyncio.sleep(random.uniform(2.4, 5.3))

        # Testing purpose
        # if page_num == 5:
        #     break
    if urls_batch:
        print(f"\n[SAVE] Save remaining {len(urls_batch)} urls...")
        save_urls_batch(urls_batch, idx, filename)
        idx += len(urls_batch)
        print(f"[SAVE] Save completed. Total index: {idx}")
    

async def controller(page, base_url):
    # records = []
    # record_cast = []
    # rec_platform = []
    # rating_re = [] ##temp
    poster_record = []  ##temp

    print("[INFO] Starting metadata scrape")

    # Load url
    idx = load_progress()
    urls = load_urls("link/kmovies", start_from=idx)

    timeout_streak = 0
    for idx, url in tqdm(urls, desc="Scraping Metadata"):
        await asyncio.sleep(random.uniform(1.2, 2.3))
        try:
            await page.goto(
                f"{base_url}{url}", 
                wait_until="domcontentloaded", 
                timeout = 60000)
            
            await page.wait_for_selector("h1.film-title")
            
            # Reset timeout streak
            timeout_streak = 0

        except PlaywrightTimeoutError or Exception as t:
            await log_error(page, "metadata", "failed_drama", url, t)
            # Increment streak on failure
            timeout_streak += 1
            if timeout_streak >= 3:
                print(f"[TERMINATED] Hit 3 timeouts in a row. Stopping to protect IP")
                break
            continue  # Skip to next URL

        # Scrape drama metadata
        try:
            # metadata, cast, platform = await scraper(page)
            poster = await scraper(page) ##temp
            await human_scroll(page)
        except Exception as e:
            await log_error(page, "metadata", "failed_drama", url, e, idx=idx)
            continue # Skip to next URL

        # Append data to list
        # records.append(metadata)
        # record_cast.extend(cast)
        # rec_platform.extend(platform)
        poster_record.extend(poster) #temp
        
        
        # Data losses safety measure
        if idx % 20 == 0:
            print(f"\n[INFO] Reach batch limit. Saving up to {idx}...")
            # await save_record(records, "metadata_variety")
            # await save_record(record_cast, "cast_variety")
            # await save_record(rec_platform, "platform_variety")
            await save_record(poster_record, "poster_movies")


            # Empty out the list
            # records.clear()
            # record_cast.clear()
            # rec_platform.clear()
            poster_record.clear() ##temp
            save_progress(idx)

    # Final save for remaining items
    if poster:
        print(f"\n[INFO] Saving remaining data... ")
        # await save_record(records, "metadata_variety")
        # await save_record(record_cast, "cast_variety")
        # await save_record(rec_platform, "platform_variety")
        await save_record(poster_record, "poster_movies")
        print("\n")
    return "Scrape Complete"

async def main():
    base_url = "https://mydramalist.com"
    filtered_url = "https://mydramalist.com/search?adv=titles&ty=86&fm=6,7,14,20,24,26,30,34&co=3&th=-428,-1045,-24729&re=2015,2031&rt=5,10&st=3&so=newest&or=asc"

    # browswer agent set up
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale= "id-ID",
            timezone_id= "Asia/Jakarta"
        )

        page = await context.new_page()
        ## Collect drama url
        # await collect_url(page, filtered_url,"ktvshows.txt")

        ## Scrape drama metadata
        await controller(page, base_url)
        
        await context.close()
        await browser.close()
        # print(result)
        print(f"Closing the program...")


if __name__ == "__main__":
    asyncio.run(main())
    # testing()
