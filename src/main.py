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


class SuperJobAPI:
    def __init__(self, app_key: str):
        self.base_url = "https://api.superjob.ru/2.33.0"
        self.headers = {'X-Api-App-Id': app_key}

    @staticmethod
    def filter_vacancies(hh_vacancies: List[dict], sj_vacancies: List[dict], filter_words: List[str]) -> List[dict]:
        filtered_vacancies = []
        for vacancy in hh_vacancies + sj_vacancies:
            if not filter_words:
                filtered_vacancies.append(vacancy)
            else:
                for word in filter_words:
                    if word in vacancy['name'].lower():
                        filtered_vacancies.append(vacancy)
                        break
        return filtered_vacancies

    @staticmethod
    def sort_vacancies(vacancies: List[dict]) -> List[dict]:
        return sorted(vacancies, key=lambda x: x['salary']['from'] if x['salary'] and x['salary']['from'] else 0,
                      reverse=True)

    @staticmethod
    def get_top_vacancies(vacancies: List[dict], top_n: int) -> List[dict]:
        return vacancies[:top_n]


