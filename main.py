import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load environment variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
LOGIN_USER = os.getenv("LOGIN_USER")
LOGIN_PASS = os.getenv("LOGIN_PASS")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        page.goto(BASE_URL)

        page.fill("#username", LOGIN_USER)
        page.fill("#password", LOGIN_PASS)
        page.click("#login-button")

        page.wait_for_selector(".framework-header-selector-button")
        page.click(".framework-header-selector-button")

        page.wait_for_selector(".component-selector-model-input")
        division_list = ['Toyota', 'Honda', 'Chevy Cars', 'Chevy Utility Vehicles']
        for each_division in division_list:
            page.select_option('.component-selector-make-input', label=each_division)
            division = page.eval_on_selector('select.component-selector-make-input','select => select.options[select.selectedIndex].textContent')
            time.sleep(1)
            page.wait_for_selector(".component-selector-model-input")
            models = page.eval_on_selector_all(".component-selector-model-input option", "options => options.slice(1).map(option=> option.textContent)")
            for model in models:
                data = []
                page.select_option('.component-selector-model-input', label=model)
                time.sleep(1)
                table = page.query_selector("table.style-cellTableWidget tbody")
                rows = table.query_selector_all("tr")

                for row in rows:
                    cells = row.query_selector_all("td")
                    row_data = [cell.inner_text().strip() for cell in cells]
                    data.append(row_data)
            
                time.sleep(1)
                print(data)
            print(f"Division: {division} \nModels: {models}")
        page.pause()

        #browser.close()


if __name__ == "__main__":
    run()