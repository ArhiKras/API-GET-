import requests
from colorama import Fore, Style, init

# Инициализация colorama для Windows
init(autoreset=True)


def get_country_info(country: str):
    """
    Получает информацию о стране через API.
    
    Args:
        country: Название страны
        
    Returns:
        tuple: (status_code, data) - статус код и данные о стране, или (None, None) в случае ошибки
    """
    url = f"https://restcountries.com/v3.1/name/{country}"
    try:
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 200:
            data = response.json()
            # API возвращает список, берем первый элемент
            if isinstance(data, list) and len(data) > 0:
                return (status_code, data[0])
            return (status_code, data)
        else:
            print(f"{Fore.RED}Ошибка: Статус код {status_code}")
            return (status_code, None)
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Ошибка при запросе: {e}")
        return (None, None)


def format_currency(currencies):
    """
    Форматирует информацию о валютах.
    """
    if not currencies:
        return "Не указано"
    result = []
    for code, info in currencies.items():
        result.append(f"{code} - {info.get('name', '')} ({info.get('symbol', '')})")
    return ", ".join(result)


def display_short_country_info(country_data: dict, status_code: int = None):
    """
    Выводит краткую информацию о стране (ключевые поля) с цветами.
    
    Args:
        country_data: Словарь с данными о стране
        status_code: HTTP статус код ответа
    """
    if not country_data:
        print(f"{Fore.RED}Нет данных для отображения")
        return
    
    name = country_data.get('name', {})
    common_name = name.get('common', 'Неизвестно')
    
    # Столица
    capital = country_data.get('capital', [])
    capital_str = capital[0] if capital and len(capital) > 0 else 'Не указано'
    
    # Население
    population = country_data.get('population', 0)
    population_str = f"{population:,} человек" if population else 'Не указано'
    
    # Валюта
    currencies = country_data.get('currencies', {})
    currency_str = format_currency(currencies)
    
    # Заголовок
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*50}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{common_name.upper():^50}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'='*50}\n")
    
    # Статус код
    if status_code is not None:
        status_color = Fore.GREEN if 200 <= status_code < 300 else Fore.RED
        print(f"{Fore.YELLOW}{Style.BRIGHT}HTTP Status Code:{Style.RESET_ALL} {status_color}{status_code}\n")
    
    # Ключевые поля
    print(f"{Fore.YELLOW}{Style.BRIGHT}Столица:{Style.RESET_ALL} {Fore.WHITE}{capital_str}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}Население:{Style.RESET_ALL} {Fore.WHITE}{population_str}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}Валюта:{Style.RESET_ALL} {Fore.WHITE}{currency_str}")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*50}\n")


def main():
    """
    Основная функция для ввода страны и вывода краткой информации.
    """
    while True:
        print(f"{Fore.CYAN}{Style.BRIGHT}Краткая информация о стране{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Введите название страны (или 'exit' для выхода):{Style.RESET_ALL}", end=" ")
        country = input().strip()
        
        if not country:
            print(f"{Fore.RED}Название страны не может быть пустым\n")
            continue
        
        if country.lower() == 'exit':
            print(f"{Fore.CYAN}Выход из программы.")
            break
        
        print(f"\n{Fore.YELLOW}Загрузка информации о {country}...{Style.RESET_ALL}")
        status_code, country_data = get_country_info(country)
        
        if country_data:
            display_short_country_info(country_data, status_code)
        else:
            print(f"{Fore.RED}Не удалось получить информацию о стране '{country}'\n")


if __name__ == "__main__":
    main()

