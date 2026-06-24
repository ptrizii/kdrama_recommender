from playwright.async_api import async_playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
import asyncio
from pipeline.utils import log_error


async def scrape_synopsis(page):
    syp_box = page.locator("div.show-synopsis p")
    if await syp_box.count() == 0:
        return None
    synopsis = await syp_box.inner_text()
    syps = " ".join(synopsis.split()) if synopsis else None
    return syps


async def scrape_id(page):
    drama_id = await page.locator('meta[property="mdl:rid"]').get_attribute("content")
    return drama_id


async def scrape_metadata(page, content, label, alt=None):
    content_box = page.locator(f"div.{content}")
    locator = content_box.locator(
        f"li:has(b:text-is('{label}'))"
    )
    if await locator.count() == 0 and alt:
        locator = content_box.locator(f"li:has(b:has-text('{alt}'))").first

    if await locator.count() == 0:
        return None

    text = await locator.inner_text()
    text = text.split(":", 1)[-1].strip()
    return text


async def scrape_cast(page, drama_id):
    cast = []

    cast_box = page.locator(
        "div.box:has(h3:text-is('Cast & Credits'))"
    )
    # Safety check
    if await cast_box.count() == 0:
        print(f"[ERROR] Cast section not found")
        title_ = await page.locator("h1.film-title", timeout=6000).inner_text()
        with open(f"failed_url.txt", "a") as f:
            f.write(f"{title_}\n")
        return cast

    cast_items = cast_box.locator(
        "ul.credits li.list-item"
    )
    count_ = await cast_items.count()
    # print(f"[INFO] Found {count_} cast members")

    # Start scraping
    for i in range(count_):
        actor_name = await cast_items.nth(i).locator("b[itempropx='name']").inner_text()
        role = await cast_items.nth(i).locator("small.text-muted").inner_text()
        cast.append({
            "drama_id": drama_id,
            "actor": actor_name.strip(),
            "role": role.strip()            
            })

    return cast

async def scrape_platform(page, drama_id):
    platform = []
    container = page.locator("div.box:has(h3:has-text('Where to Watch'))")

    if await container.count() == 0:
        # print(f"[ERROR] No watching platform found for {drama_id}")
        return platform
    
    items = container.locator("div.row.no-gutter")
    count_ = await items.count()
    for i in range(count_):
        box_name = await items.nth(i).locator("div.p-l a b").inner_text()
        platform.append(
            {"drama_id": drama_id, 
            "name": box_name}
        )
    return platform

async def scrape_rating(page):
    container = page.locator("div.box:has(h3:has-text('Statistics'))")
    if await container.count()==0:
        return None

    locator = container.locator("li:has(b:has-text('Score'))")
    rating = await locator.inner_text()

    return rating

async def get_poster(page, drama_id):  ##need to remove the drama id

    container = page.locator("div.film-cover img")
    if await container.count()==0:
        return None
    
    url = await container.first.get_attribute('src')

    return url



async def scraper(page):

    # Scrape general metadata
    drama_id = await scrape_id(page)
    metadata = {
        "id": drama_id,
        "title": await scrape_metadata(page, "content-side", "Title:"),
        "native-title": await scrape_metadata(page, "show-detailsxss", "Native Title:"),
        "genre": await scrape_metadata(page, "show-detailsxss", "Genres:"),
        "director": await scrape_metadata(page, "show-detailsxss", "Director:"),
        "format": await scrape_metadata(page, "content-side", "Format:"),
        "type": await scrape_metadata(page, "content-side", "Type:"),
        "country": await scrape_metadata(page, "content-side", "Country:"),
        "release_date": await scrape_metadata(page, "content-side", "Release Date:", "Air"),
        "duration": await scrape_metadata(page, "content-side", "Duration:"),
        "episodes": await scrape_metadata(page, "content-side", "Episodes:"),
        "ct_rate": await scrape_metadata(page, "content-side", "Content Rating:"),
        "tag": await scrape_metadata(page, "show-detailsxss", "Tags:"),
        "synopsis": await scrape_synopsis(page),
        "rating": await scrape_rating(page),
        "poster": await get_poster(page)
    }

    # Scrape cast member, platform
    cast = await scrape_cast(page, drama_id)
    platform = await scrape_platform(page, drama_id)

    return metadata, cast, platform
