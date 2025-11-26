import requests


def get(url, params=None, timeout=10, headers=None):
    """
    Выполняет GET запрос к указанному URL с базовой проверкой статуса.
    
    Args:
        url: URL для запроса
        params: словарь параметров запроса (опционально)
        timeout: таймаут запроса в секундах (по умолчанию 10)
        headers: словарь заголовков (опционально)
        
    Returns:
        requests.Response: Объект ответа, если запрос успешен
        None: В случае ошибки или неуспешного статуса
        
    Raises:
        requests.exceptions.RequestException: При ошибках сети или таймауте
    """
    try:
        response = requests.get(url, params=params, timeout=timeout, headers=headers)
        
        # Базовая проверка статуса
        if response.status_code >= 200 and response.status_code < 300:
            return response
        else:
            print(f"Ошибка: HTTP статус {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"Ошибка: Превышено время ожидания ({timeout} секунд)")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

