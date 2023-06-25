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

    @staticmethod
    def print_vacancies(cls, vacancies: List[dict]):
        for vacancy in vacancies:
            print(f"{vacancy['name']}\n{vacancy['employer']['name']}\n{vacancy['alternate_url']}\n{'-' * 30}\n")

    def user_interaction(self):
        from JSONSaver import JSONSaver

        hh_api = HeadHunterAPI()
        app_key = "v3.r.137636772.89b8dc4297218a5dcf9c8e6f468e738f0182aae0.5d001ac5ff302dddcf98f5f8de641b4d947f0c4e"
        sj_api = SuperJobAPI(app_key)

        search_query = input("Введите поисковый запрос: ")
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        filter_words = input("Введите ключевые слова для фильтрации вакансий: ").lower().split()

        hh_vacancies = hh_api.get_vacancies(search_query)
        sj_vacancies = []

        filtered_vacancies = SuperJobAPI.filter_vacancies(hh_vacancies, sj_vacancies, filter_words)
        if not filtered_vacancies:
            print("Нет вакансий, соответствующих заданным критериям.")
        sorted_vacancies = SuperJobAPI.sort_vacancies(filtered_vacancies)
        top_vacancies = SuperJobAPI.get_top_vacancies(sorted_vacancies, top_n)

        SuperJobAPI.print_vacancies(sj_api, top_vacancies)

        save_to_file = input("Сохранить вакансии в файл? (y/n): ")
        if save_to_file.lower() == "y":
            json_saver = JSONSaver()
            for vacancy in filtered_vacancies:
                json_saver.add_vacancy(vacancy)
            json_saver.save_data("vacancies.json")
            print("Вакансии сохранены в файл.")

