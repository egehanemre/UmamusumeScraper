# Uma Musume Event Scraper

This Python script uses **Selenium** to scrape character event data from [Gametora](https://gametora.com/umamusume/characters).  
It collects all Uma Musume character event choices and effects, then saves the results into a JSON file.

---

## Features
- Automatically collects all **character URLs** from Gametora.  
- Scrapes **event options and their effects** for each character.  
- Saves everything into a structured JSON file (`all_umamusume_events.json`).  
- Handles tooltips, dynamic loading, and duplicate links automatically.  

---

## Requirements

Make sure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [Google Chrome](https://www.google.com/chrome/)
- [ChromeDriver](https://chromedriver.chromium.org/) (installed automatically by `webdriver_manager`)

Install dependencies via pip:

```bash
pip install selenium webdriver-manager
