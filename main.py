import requests
from http_client import get

try:
    from country_info import get_country_info as get_full_country_info, display_country_info
    from short_country_info import get_country_info as get_short_country_info, display_short_country_info
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError as e:
    print(f"Ошибка импорта модулей: {e}")
    get_full_country_info = None
    display_country_info = None
    get_short_country_info = None
    display_short_country_info = None
    Fore = None
    Style = None


def get_request(url, params=None, headers=None):
    """
    Выполняет GET запрос к указанному URL.
    
    Args:
        url: URL для запроса
        params: словарь параметров запроса (опционально)
        headers: словарь заголовков (опционально)
    """
    response = get(url, params=params, headers=headers)
    if response:
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Body:\n{response.text}")
    return response


def post_request(url, data=None, json=None, headers=None):
    """
    Выполняет POST запрос к указанному URL.
    
    Args:
        url: URL для запроса
        data: данные для отправки (form-data, опционально)
        json: JSON данные для отправки (опционально)
        headers: словарь заголовков (опционально)
    """
    try:
        response = requests.post(url, data=data, json=json, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Body:\n{response.text}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# GET запрос для страны
def make_get_country_request(country: str):
    url = f"https://restcountries.com/v3.1/name/{country}"
    get_request(url)


def get_random_dog():
    """
    Получает случайное изображение собаки и выводит ссылку.
    """
    url = "https://dog.ceo/api/breeds/image/random"
    response = get(url)
    if response:
        status_code = response.status_code
        data = response.json()
        if data.get('status') == 'success':
            image_url = data.get('message', '')
            print(f"\n=== Случайная собака ===")
            # Вывод статус кода
            if Fore and Style:
                status_color = Fore.GREEN if 200 <= status_code < 300 else Fore.RED
                print(f"{Fore.YELLOW}{Style.BRIGHT}HTTP Status Code:{Style.RESET_ALL} {status_color}{status_code}\n")
            else:
                print(f"HTTP Status Code: {status_code}\n")
            print(f"Ссылка на изображение: {image_url}")
            return image_url
        else:
            print("Ошибка: API вернул статус 'error'")
            return None
    return None


def main():
    """
    Основная функция для выбора типа запроса.
    """
    import json
    
    while True:
        print("\n" + "="*50)
        print("Выберите тип запроса:")
        print("1 - GET запрос")
        print("2 - POST запрос")
        print("3 - GET запрос для страны")
        print("4 - Случайная собака")
        print("5 - Выход")
        
        choice = input("\nВведите номер (1-5): ").strip()
        
        if choice == "1":
            print("\n=== GET запрос ===")
            url = input("Введите URL: ").strip()
            if not url:
                print("URL не может быть пустым")
                continue
            
            params_input = input("Параметры запроса (JSON формат, или Enter для пропуска): ").strip()
            headers_input = input("Заголовки (JSON формат, или Enter для пропуска): ").strip()
            
            params = None
            headers = None
            
            if params_input:
                try:
                    params = json.loads(params_input)
                except json.JSONDecodeError:
                    print("Ошибка: неверный формат JSON для параметров")
                    continue
            
            if headers_input:
                try:
                    headers = json.loads(headers_input)
                except json.JSONDecodeError:
                    print("Ошибка: неверный формат JSON для заголовков")
                    continue
            
            get_request(url, params=params, headers=headers)
        
        elif choice == "2":
            print("\n=== POST запрос ===")
            url = input("Введите URL: ").strip()
            if not url:
                print("URL не может быть пустым")
                continue
            
            data_type = input("Тип данных (1 - form-data, 2 - JSON): ").strip()
            headers_input = input("Заголовки (JSON формат, или Enter для пропуска): ").strip()
            
            headers = None
            if headers_input:
                try:
                    headers = json.loads(headers_input)
                except json.JSONDecodeError:
                    print("Ошибка: неверный формат JSON для заголовков")
                    continue
            
            if data_type == "1":
                data_input = input("Данные (JSON формат): ").strip()
                if data_input:
                    try:
                        data = json.loads(data_input)
                        post_request(url, data=data, headers=headers)
                    except json.JSONDecodeError:
                        print("Ошибка: неверный формат JSON для данных")
                else:
                    post_request(url, data=None, headers=headers)
            elif data_type == "2":
                json_input = input("JSON данные (JSON формат): ").strip()
                if json_input:
                    try:
                        json_data = json.loads(json_input)
                        post_request(url, json=json_data, headers=headers)
                    except json.JSONDecodeError:
                        print("Ошибка: неверный формат JSON")
                else:
                    post_request(url, json=None, headers=headers)
            else:
                print("Неверный выбор типа данных")
        
        elif choice == "3":
            if not get_full_country_info or not display_country_info:
                print("Ошибка: модули для работы со странами не загружены")
                continue
            
            while True:
                print("\n=== Информация о стране ===")
                print("Выберите тип информации:")
                print("1 - Полная информация по стране")
                print("2 - Краткая информация по стране")
                print("3 - Назад в главное меню")
                
                sub_choice = input("\nВведите номер (1-3): ").strip()
                
                if sub_choice == "1":
                    country = input("Введите название страны: ").strip()
                    if not country:
                        print("Название страны не может быть пустым")
                        continue
                    print(f"\nЗагрузка полной информации о {country}...")
                    status_code, country_data = get_full_country_info(country)
                    if country_data:
                        display_country_info(country_data, status_code)
                    else:
                        print("Не удалось получить информацию о стране")
                
                elif sub_choice == "2":
                    country = input("Введите название страны: ").strip()
                    if not country:
                        print("Название страны не может быть пустым")
                        continue
                    print(f"\nЗагрузка краткой информации о {country}...")
                    status_code, country_data = get_short_country_info(country)
                    if country_data:
                        display_short_country_info(country_data, status_code)
                    else:
                        print("Не удалось получить информацию о стране")
                
                elif sub_choice == "3":
                    break
                
                else:
                    print("Неверный выбор. Используйте 1, 2 или 3.")
        
        elif choice == "4":
            print("\n=== Случайная собака ===")
            get_random_dog()
        
        elif choice == "5":
            print("Выход из программы.")
            break
        
        else:
            print("Неверный выбор. Используйте 1, 2, 3, 4 или 5.")


if __name__ == "__main__":
    main()
