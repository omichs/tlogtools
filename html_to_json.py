import os
import json
from bs4 import BeautifulSoup

def extract_message_data(message_div):
    """
    Извлекает данные из одного блока <div class="message">.
    Возвращает словарь с ключевой информацией.
    """
    msg_data = {}

    # ID сообщения (из атрибута 'id')
    msg_data['id'] = message_div.get('id', 'unknown')

    # Дата (из <div class="date">)
    date_div = message_div.find('div', class_='date')
    msg_data['date'] = date_div.get('title', 'unknown') if date_div else 'unknown'

    # Отправитель (из <div class="from_name">)
    from_name_div = message_div.find('div', class_='from_name')
    msg_data['sender'] = from_name_div.get_text(strip=True) if from_name_div else 'unknown'

    # Текст сообщения (из <div class="text">)
    text_div = message_div.find('div', class_='text')
    msg_data['text'] = text_div.get_text(strip=True) if text_div else ''

    # Медиа (если есть, например, <div class="media_wrap">)
    media = []
    media_wrap = message_div.find('div', class_='media_wrap')
    if media_wrap:
        # Извлекаем ссылки на изображения, видео и т.д.
        for link in media_wrap.find_all('a', href=True):
            media.append({
                'type': 'link',
                'url': link['href'],
                'description': link.get_text(strip=True)
            })
        # Или просто текст медиа, если нет ссылок
        if not media:
            media.append({
                'type': 'text',
                'content': media_wrap.get_text(strip=True)
            })
    msg_data['media'] = media

    # Дополнительные атрибуты (например, forwarded, edited)
    msg_data['is_forwarded'] = bool(message_div.find('div', class_='forwarded'))
    msg_data['is_edited'] = bool(message_div.find('div', class_='edited'))

    return msg_data


def convert_html_to_json(input_file, output_file):
    """
    Конвертирует HTML-файл в JSON.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            print(f"Чтение файла: {input_file}...")
            soup = BeautifulSoup(f, 'lxml')
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден.")
        return

    # Находим все сообщения
    messages = soup.find_all('div', class_='message')

    if not messages:
        print("Предупреждение: в файле не найдено сообщений (div.message).")
        return

    print(f"Найдено сообщений: {len(messages)}")

    # Извлекаем данные из каждого сообщения
    json_data = []
    for msg in messages:
        msg_data = extract_message_data(msg)
        json_data.append(msg_data)

    # Сохраняем в JSON-файл
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        print(f"Конвертация завершена. Результат сохранен в: {output_file}")
    except Exception as e:
        print(f"Ошибка при сохранении JSON: {e}")


if __name__ == "__main__":
    print("--- Скрипт для конвертации HTML-лога Telegram в JSON ---")
    
    input_file_path = input("Введите путь к HTML-файлу лога (например, messages.html): ").strip()

    if not os.path.isfile(input_file_path):
        print(f"Ошибка: файл '{input_file_path}' не найден.")
    else:
        # Формируем имя для выходного файла
        base, ext = os.path.splitext(input_file_path)
        output_file_path = f"{base}.json"

        # Запускаем конвертацию
        convert_html_to_json(input_file_path, output_file_path)
