from playwright.sync_api import sync_playwright
from get_laptop import laptops
from save_to_db import save_to_postgres, save_to_csv


def getFlipkartData():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.flipkart.com/")

        page.wait_for_timeout(2500)
        #page.screenshot(path="flipkart1.png")
        
        # Handle login popup safely
        close_btn = page.query_selector('span[role="button"].b3wTlE')
        if close_btn:
            close_btn.click()
            
        page.wait_for_timeout(2500)
        #page.screenshot(path="flipkart2.png")
        page.query_selector('div.olwU0Z.CXZSEo input.nw1UBF.v1zwn25').fill("laptop")
        page.wait_for_timeout(2500)
        #page.screenshot(path="flipkart3.png")
        page.query_selector('div.olwU0Z.CXZSEo button.XFwMiH').click()
        page.wait_for_load_state("networkidle")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_load_state("load")
        #page.screenshot(path="laptop_results.png")
        page.wait_for_timeout(5000)
        
        all_laptops = []
        page_num = 1
        while True:
            print(f"Scraping page {page_num}...")
            current_page_laptops = laptops(page)
            print(f"Scraped {len(current_page_laptops)} items from page {page_num}")
            
            if len(current_page_laptops) == 0:
                print("No items found on this page. Scraping finished.")
                break
                
            all_laptops.extend(current_page_laptops)
            
            page_num += 1
            # Maximum limit safeguard (2735 results / 24 per page ~= 114 pages)
            if page_num > 120:
                break
                
            # Navigate to next page directly using the page query parameter
            next_url = f"https://www.flipkart.com/search?q=laptop&page={page_num}"
            page.goto(next_url)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)
                
        save_to_postgres(all_laptops)
        save_to_csv(all_laptops)
        browser.close()


if __name__ == "__main__":
    getFlipkartData()