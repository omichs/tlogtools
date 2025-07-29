import os
import re
from bs4 import BeautifulSoup

def extract_external_links_from_log(input_html, output_txt):
    """
    Находит все ВНЕШНИЕ ссылки в HTML-логе Telegram и сохраняет их в TXT-файл.
    Локальные ссылки на файлы (фото, стикеры) игнорируются.
    """
    try:
        with open(input_html, "r", encoding="utf-8") as f:
            print(f"Чтение файла: {input_html}...")
            soup = BeautifulSoup(f, "lxml")
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_html}' не найден.")
        return

    # Используем set для автоматического удаления дубликатов
    links_set = set()
    
    # --- Ключевые изменения здесь ---

    # 1. Поиск ссылок в тегах <a href="...">
    for a_tag in soup.find_all("a", href=True):
        url = a_tag["href"]
        # Проверяем, что ссылка является внешней (начинается с http, https, ftp или t.me)
        if url.startswith(('http://', 'https://', 'ftp://', 't.me')):
            links_set.add(url)

    # 2. Поиск ссылок, которые написаны просто текстом (без тега <a>)
    # Этот блок уже искал только внешние ссылки, так что он остается без изменений.
    messages = soup.find_all('div', class_='text')
    url_regex = re.compile(
        r'(https?://[^\s"<>\]]+|t\.me/[^\s"<>\]]+|ftp://[^\s"<>\]]+)', re.IGNORECASE)
    
    for div in messages:
        text = div.get_text(separator="\n", strip=True)
        for match in url_regex.findall(text):
            links_set.add(match)

    # --- Конец изменений ---

    # Сортируем найденные уникальные ссылки по алфавиту
    links = sorted(list(links_set))

    if not links:
        print("Внешние ссылки в файле не найдены.")
        return

    # Сохраняем результат в файл
    try:
        with open(output_txt, "w", encoding="utf-8") as f:
            for link in links:
                f.write(link.strip() + "\n")
        print(f"\nНайдено уникальных внешних ссылок: {len(links)}")
        print(f"Все ссылки успешно сохранены в файл: {output_txt}")
    except Exception as e:
        print(f"Произошла ошибка при сохранении файла: {e}")


if __name__ == "__main__":
    print("--- Скрипт для извлечения внешних ссылок из логов Telegram ---")
    
    input_file_path = input("Введите путь к HTML-файлу (например, messages.html): ").strip()

    if not os.path.isfile(input_file_path):
        print(f"Ошибка: файл '{input_file_path}' не найден.")
    else:
        # Формируем имя для выходного файла
        base, _ = os.path.splitext(input_file_path)
        output_txt_path = base + "_external_links.txt"
        
        # Запускаем функцию
        extract_external_links_from_log(input_file_path, output_txt_path)
