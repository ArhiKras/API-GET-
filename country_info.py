import requests
from colorama import Fore, Back, Style, init

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


def format_languages(languages):
    """
    Форматирует информацию о языках.
    """
    if not languages:
        return "Не указано"
    return ", ".join(languages.values())


def format_list(items):
    """
    Форматирует список в строку.
    """
    if not items:
        return "Не указано"
    if isinstance(items, list):
        return ", ".join(str(item) for item in items)
    return str(items)


def display_country_info(country_data: dict, status_code: int = None):
    """
    Красиво выводит информацию о стране с цветами.
    
    Args:
        country_data: Словарь с данными о стране
        status_code: HTTP статус код ответа
    """
    if not country_data:
        print(f"{Fore.RED}Нет данных для отображения")
        return
    
    name = country_data.get('name', {})
    common_name = name.get('common', 'Неизвестно')
    official_name = name.get('official', 'Неизвестно')
    
    # Заголовок
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{common_name.upper():^70}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'='*70}\n")
    
    # Статус код
    if status_code is not None:
        status_color = Fore.GREEN if 200 <= status_code < 300 else Fore.RED
        print(f"{Fore.YELLOW}{Style.BRIGHT}HTTP Status Code:{Style.RESET_ALL} {status_color}{status_code}\n")
    
    # Основная информация
    print(f"{Fore.YELLOW}{Style.BRIGHT}Официальное название:{Style.RESET_ALL} {Fore.WHITE}{official_name}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}Регион:{Style.RESET_ALL} {Fore.WHITE}{country_data.get('region', 'Не указано')}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}Подрегион:{Style.RESET_ALL} {Fore.WHITE}{country_data.get('subregion', 'Не указано')}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}Континент:{Style.RESET_ALL} {Fore.WHITE}{format_list(country_data.get('continents', []))}")
    
    # Географическая информация
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Географическая информация:{Style.RESET_ALL}")
    latlng = country_data.get('latlng', [])
    if latlng and len(latlng) >= 2:
        print(f"  {Fore.YELLOW}Координаты:{Style.RESET_ALL} {Fore.WHITE}Широта: {latlng[0]}, Долгота: {latlng[1]}")
    print(f"  {Fore.YELLOW}Площадь:{Style.RESET_ALL} {Fore.WHITE}{country_data.get('area', 'Не указано'):,} км²" if country_data.get('area') else f"  {Fore.YELLOW}Площадь:{Style.RESET_ALL} {Fore.WHITE}Не указано")
    print(f"  {Fore.YELLOW}Граничит с:{Style.RESET_ALL} {Fore.WHITE}{format_list(country_data.get('borders', []))}")
    print(f"  {Fore.YELLOW}Выход к морю:{Style.RESET_ALL} {Fore.WHITE}{'Нет' if country_data.get('landlocked', False) else 'Да'}")
    
    # Демографическая информация
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Демографическая информация:{Style.RESET_ALL}")
    population = country_data.get('population', 0)
    if population:
        print(f"  {Fore.YELLOW}Население:{Style.RESET_ALL} {Fore.WHITE}{population:,} человек")
    else:
        print(f"  {Fore.YELLOW}Население:{Style.RESET_ALL} {Fore.WHITE}Не указано")
    
    gini = country_data.get('gini', {})
    if gini:
        year = list(gini.keys())[0] if gini else None
        value = list(gini.values())[0] if gini else None
        if year and value:
            print(f"  {Fore.YELLOW}Коэффициент Джини ({year}):{Style.RESET_ALL} {Fore.WHITE}{value}")
    
    # Политическая информация
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Политическая информация:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Столица:{Style.RESET_ALL} {Fore.WHITE}{format_list(country_data.get('capital', []))}")
    capital_info = country_data.get('capitalInfo', {})
    if capital_info.get('latlng'):
        cap_latlng = capital_info['latlng']
        print(f"  {Fore.YELLOW}Координаты столицы:{Style.RESET_ALL} {Fore.WHITE}Широта: {cap_latlng[0]}, Долгота: {cap_latlng[1]}")
    print(f"  {Fore.YELLOW}Независимость:{Style.RESET_ALL} {Fore.WHITE}{'Да' if country_data.get('independent', False) else 'Нет'}")
    print(f"  {Fore.YELLOW}Член ООН:{Style.RESET_ALL} {Fore.WHITE}{'Да' if country_data.get('unMember', False) else 'Нет'}")
    
    # Экономическая информация
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Экономическая информация:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Валюта:{Style.RESET_ALL} {Fore.WHITE}{format_currency(country_data.get('currencies', {}))}")
    
    # Культурная информация
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Культурная информация:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Языки:{Style.RESET_ALL} {Fore.WHITE}{format_languages(country_data.get('languages', {}))}")
    
    # Коды и идентификаторы
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Коды и идентификаторы:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}ISO 3166-1 alpha-2:{Style.RESET_ALL} {Fore.WHITE}{country_data.get('cca2', 'Не указано')}")
    print(f"  {Fore.YELLOW}ISO 3166-1 alpha-3:{Style.RESET_ALL} {Fore.WHITE}{country_data.get('cca3', 'Не указано')}")
    print(f"  {Fore.YELLOW}Телефонный код:{Style.RESET_ALL} {Fore.WHITE}{country_data.get('idd', {}).get('root', '')}{country_data.get('idd', {}).get('suffixes', [''])[0] if country_data.get('idd', {}).get('suffixes') else ''}")
    
    # Дополнительная информация
    if country_data.get('timezones'):
        print(f"  {Fore.YELLOW}Часовые пояса:{Style.RESET_ALL} {Fore.WHITE}{format_list(country_data.get('timezones', []))}")
    if country_data.get('startOfWeek'):
        print(f"  {Fore.YELLOW}Начало недели:{Style.RESET_ALL} {Fore.WHITE}{country_data.get('startOfWeek', 'Не указано').capitalize()}")
    
    # Ссылки
    maps = country_data.get('maps', {})
    if maps:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}Ссылки:{Style.RESET_ALL}")
        if maps.get('googleMaps'):
            print(f"  {Fore.YELLOW}Google Maps:{Style.RESET_ALL} {Fore.BLUE}{maps['googleMaps']}")
        if maps.get('openStreetMaps'):
            print(f"  {Fore.YELLOW}OpenStreetMap:{Style.RESET_ALL} {Fore.BLUE}{maps['openStreetMaps']}")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}\n")


def main():
    """
    Основная функция для ввода страны и вывода информации.
    """
    while True:
        print(f"{Fore.CYAN}{Style.BRIGHT}Информация о стране{Style.RESET_ALL}")
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
            display_country_info(country_data, status_code)
        else:
            print(f"{Fore.RED}Не удалось получить информацию о стране '{country}'\n")


if __name__ == "__main__":
    main()

