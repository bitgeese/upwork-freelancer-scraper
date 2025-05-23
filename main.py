import csv
import time
from typing import List, Optional
from urllib.parse import urlencode

import typer
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = typer.Typer()


class UpworkScraper:
    def __init__(self, base_url: str, search_params: dict, page_range: range):
        self.base_url = base_url
        self.search_params = search_params
        self.page_range = page_range

    def create_url(self, page_number: int) -> str:
        params = self.search_params.copy()
        params["page"] = page_number
        return f"{self.base_url}?{urlencode(params)}"

    def fetch_page_content(self, url: str) -> Optional[str]:
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        try:
            browser.get(url)
            time.sleep(2)  # Adding a delay to ensure the page loads completely
            return browser.page_source
        except Exception as e:
            print(f"Error fetching page content: {e}")
            return None
        finally:
            browser.quit()

    def parse_main_page(self, content: str) -> List[dict]:
        soup = BeautifulSoup(content, "html.parser")
        articles = soup.find_all("article")
        freelancers = []
        for art in articles:
            title = art.find("h4").text.strip()
            description = art.find("div", {"class": "description"}).text.strip()
            link = art.find("a", {"class": "profile-link"})["href"]
            skills = art.find("div", {"data-test": "FreelancerTileSkills"})
            skills = [x.text.strip() for x in skills.find_all("span")][:-1]
            skills = ", ".join(skills)
            rate = art.find("span", {"data-test": "rate-per-hour"}).text.strip()
            if float(rate.strip("$")) < 30:
                continue
            try:
                total_earnings = art.find(
                    "div", {"data-test": "freelancer-tile-earnings"}
                ).text.strip()
            except AttributeError:
                continue
            freelancers.append(
                {
                    "headline": title,
                    "skills": skills,
                    "hourly rate": rate,
                    "total_earnings": total_earnings,
                    "description": description,
                    "url": link,
                }
            )
        return freelancers

    def save_to_csv(self, freelancers: List[dict], filename: str) -> None:
        keys = freelancers[0].keys() if freelancers else []
        with open(filename, "w", newline="", encoding="utf-8") as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(freelancers)

    def scrape(self, output_file: str) -> None:
        freelancers = []
        for page in self.page_range:
            main_page_url = self.create_url(page)
            main_page_content = self.fetch_page_content(main_page_url)
            if main_page_content:
                freelancers += self.parse_main_page(main_page_content)
        self.save_to_csv(freelancers, output_file)


@app.command()
def main(
    q: str,
    rate: str = "30",
    hrs: str = "1000",
    nss: str = "90",
    revenue: str = "10000",
    page_start: int = 1,
    page_end: int = 10,
    output_file: str = "freelancers.csv",
) -> None:
    base_url = "https://www.upwork.com/nx/search/talent"
    search_params = {
        "rate": rate,
        "hrs": hrs,
        "nss": nss,
        "q": q,
        "revenue": revenue,
    }
    page_range = range(page_start, page_end + 1)

    scraper = UpworkScraper(base_url, search_params, page_range)
    scraper.scrape(output_file)


if __name__ == "__main__":
    app()
