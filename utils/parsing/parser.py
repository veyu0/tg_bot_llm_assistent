import logging
import requests
from bs4 import BeautifulSoup
from utils.db.database import Database

class CaseParser:
    def __init__(self, db_url: str):
        self.logger = logging.getLogger(__name__)
        self.db = Database(db_path=db_url)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    def parse_page(self, url: str) -> dict:
        """Fetch and parse a single case page."""
        try:
            self.logger.info(f"Fetching page: {url}")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            project_name = soup.find('h1').text.strip() if soup.find('h1') else 'Unknown'

            # client_section = soup.find('h3', string=lambda t: t and 'Заказчик' in t) \
            #     or soup.find('div', string=lambda t: t and 'Клиент' in t) \
            #     or soup.find('div', string=lambda t: t and 'Заказчик' in t)
            # for_whom = 'Unknown'
            # if client_section:
            #     target_div = client_section.find_next('div', lambda tag: tag and tag.find('span'))
            #     if target_div:
            #         span = target_div.find('span')
            #         if span:
            #             for_whom = span.text.strip()
            # else:
            #     self.logger.warning(f"No client section found on page: {url}")

            # problem_section = soup.find('h3', string=lambda t: t and 'Задача' in t) or soup.find('div', string=lambda t: t and 'Задача' in t)
            # problem_solved = 'Unknown'
            # if problem_section:
            #     target_div = problem_section.find_next('div')
            #     if target_div:
            #         problem_solved = target_div.text.strip()
            # else:
            #     self.logger.warning(f"No problem section found on page: {url}")

            self.logger.info(f"Parsed {url}: Name='{project_name}'")

            return {
                'url': url,
                'name': project_name,
                #'for_whom': for_whom,
                #'problem_solved': problem_solved
            }
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    def run(self, source_file: str = 'utils/parsing/parsing_source.txt'):
        """Read URLs from file and parse each."""
        with open(source_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]

        for url in urls:
            data = self.parse_page(url)
            if data:
                self.db.add_project(data['url'], data['name'])