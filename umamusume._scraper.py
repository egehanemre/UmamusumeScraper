import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://gametora.com"

def get_all_character_urls(driver):
    driver.get(f"{BASE_URL}/umamusume/characters")
    time.sleep(2)

    try:
        driver.find_element(By.CLASS_NAME, "legal_cookie_banner_button__Oy_Qr").click()
        time.sleep(0.2)
    except:
        pass

    links = driver.find_elements(By.XPATH, "//a[contains(@href, '/umamusume/characters/') and not(contains(@href, '#'))]")
    hrefs = list(set([BASE_URL + a.get_attribute("href") for a in links]))
    # Remove duplicates and fix if there's double "https://gametora.com"
    hrefs = [h.replace("https://gametora.comhttps://gametora.com", "https://gametora.com") for h in hrefs]
    return hrefs

def scrape_character_events(driver, url):
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    time.sleep(0.5)

    try:
        driver.find_element(By.CLASS_NAME, "legal_cookie_banner_button__Oy_Qr").click()
        time.sleep(0.2)
    except:
        pass

    character_events = {}
    try:
        categories = driver.find_elements(By.CSS_SELECTOR, "div.eventhelper_elist__A0Bud")
    except:
        return {}

    for category in categories:
        try:
            cat_title = category.find_element(By.CSS_SELECTOR, "div.sc-913225d8-0.bWLkfL").text.strip()
        except:
            continue

        events = category.find_elements(By.CSS_SELECTOR, "div.compatibility_viewer_item__SWULM")
        event_dict = {}

        for event in events:
            event_name = event.text.strip()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", event)
            time.sleep(0.2)

            try:
                event.click()
            except:
                driver.execute_script("arguments[0].click();", event)
            time.sleep(0.5)

            try:
                tooltip = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.tippy-box[role='tooltip']")))
                tooltip_content = tooltip.find_element(By.CSS_SELECTOR, "div.tippy-content")
            except:
                continue

            try:
                event_title = tooltip_content.find_element(By.CSS_SELECTOR, "div.tooltips_ttable_heading__jlJcE").text.strip()
            except:
                continue

            options_list = []
            rows = tooltip_content.find_elements(By.CSS_SELECTOR, "tr.tooltips_ttable_row__T8N69")
            for row in rows:
                tds = row.find_elements(By.CSS_SELECTOR, "td.tooltips_ttable_cell___3NMF")
                if len(tds) == 2:
                    option_text = tds[0].text.strip()
                    effects = [e.text.strip() for e in tds[1].find_elements(By.CSS_SELECTOR, "div") if e.text.strip()]
                    options_list.append({"text": option_text, "effects": effects})

            if not options_list:
                effect_divs = tooltip_content.find_elements(By.CSS_SELECTOR, "div.tooltips_ttable_cell___3NMF > div")
                effects = [e.text.strip() for e in effect_divs if e.text.strip()]
                if effects:
                    options_list.append({"text": "Reward", "effects": effects})

            event_dict[event_title] = {"options": options_list}

            driver.execute_script("document.body.click();")
            time.sleep(0.2)

        character_events[cat_title] = event_dict

    return character_events

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    print("Collecting character URLs...")
    character_urls = get_all_character_urls(driver)
    print(f"Found {len(character_urls)} characters.")

    all_data = {}
    for idx, url in enumerate(character_urls):
        char_id = url.split("/")[-1]
        print(f"[{idx+1}/{len(character_urls)}] Scraping: {char_id}")
        try:
            events = scrape_character_events(driver, url)
            all_data[char_id] = events
        except Exception as e:
            print(f"  Error on {char_id}: {e}")
            continue

    driver.quit()

    with open("all_umamusume_events.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

    print("✅ Scraping complete! Saved to all_umamusume_events.json")

if __name__ == "__main__":
    main()
