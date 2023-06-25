import request
from typing import List


class HeadHunterAPI:
    def __init__(self):
        self.base_url = "https://api.hh.ru"

    def get_vacancies(self, search_query: str) -> List[dict]:
        vacancies_url = f"{self.base_url}/vacancies"
        params = {'text': search_query}
        response = requests.get(vacancies_url, params=params)
        response.raise_for_status()
        return response.json()['items']