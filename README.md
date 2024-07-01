
# Upwork Scraper

This Python script scrapes freelancer profiles from Upwork based on specified search criteria and saves the results to a CSV file.

## Requirements

- Python 3.6+
- The following Python packages:
  - `typer`
  - `beautifulsoup4`
  - `selenium`
  - `webdriver-manager`

You can install the required packages using `pip`:

```bash
pip install typer beautifulsoup4 selenium webdriver-manager
```

## Usage

To run the script, use the following command:

```bash
python script.py [OPTIONS]
```

### Options

- `--q TEXT`: The search query (required).
- `--rate TEXT`: The minimum hourly rate (default: 30).
- `--hrs TEXT`: The minimum number of hours worked (default: 1000).
- `--nss TEXT`: The minimum Job Success Score (default: 90).
- `--revenue TEXT`: The minimum total earnings (default: 10000).
- `--page-start INTEGER`: The starting page number for pagination (default: 1).
- `--page-end INTEGER`: The ending page number for pagination (default: 10).
- `--output-file TEXT`: The output CSV file name (default: `freelancers.csv`).

### Example

```bash
python script.py --q "Python developer" --rate "40" --hrs "500" --nss "95" --revenue "20000" --page-start 1 --page-end 5 --output-file "python_developers.csv"
```

## How It Works

1. **Initialization**: The `UpworkScraper` class is initialized with the base URL, search parameters, and the range of pages to scrape.

2. **URL Creation**: The `create_url` method generates the URL for each page based on the search parameters and page number.

3. **Fetching Page Content**: The `fetch_page_content` method uses Selenium to load the page and retrieve its HTML content.

4. **Parsing the Page**: The `parse_main_page` method uses BeautifulSoup to parse the HTML content and extract freelancer information.

5. **Saving to CSV**: The `save_to_csv` method saves the extracted freelancer information to a CSV file.

6. **Scraping**: The `scrape` method iterates over the specified page range, fetches, parses, and accumulates the freelancer data, and then saves it to a CSV file.

## Note

- Ensure that ChromeDriver is installed and properly configured on your system as the script uses Selenium with Chrome.
- The script includes a delay (`time.sleep(2)`) to ensure that the page loads completely before parsing.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

---

This script was created to facilitate the scraping of freelancer profiles from Upwork based on specific criteria. It demonstrates the use of web scraping techniques and the handling of dynamic web content using Selenium and BeautifulSoup.
