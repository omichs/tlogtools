import os
from bs4 import BeautifulSoup

def convert_html_to_txt(input_file, output_file):
    """
    Конвертирует HTML-файл лога Telegram в текстовый (.txt) формат.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            print(f"Чтение файла: {input_file}...")
            soup = BeautifulSoup(f, 'lxml')
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден.")
        return

    # Находим все блоки сообщений
    messages = soup.find_all('div', class_='message')

    if not messages:
        print("Предупреждение: в файле не найдено сообщений (div.message).")
        return

    print(f"Найдено сообщений для конвертации: {len(messages)}")

    # Создаем список для хранения отформатированных строк
    conversation_lines = []

    for msg_div in messages:
        # Извлекаем дату из атрибута 'title' тега <div class="date">
        date_div = msg_div.find('div', class_='date')
        date_str = date_div['title'] if date_div and 'title' in date_div.attrs else "Неизвестная дата"

        # Извлекаем имя отправителя из <div class="from_name">
        from_name_div = msg_div.find('div', class_='from_name')
        sender_name = from_name_div.get_text(strip=True) if from_name_div else "Неизвестный отправитель"
        
        # Извлекаем текст сообщения из <div class="text">
        text_div = msg_div.find('div', class_='text')
        message_text = ''
        if text_div:
            # get_text с разделителем '\n' сохраняет переносы строк внутри сообщения
            message_text = text_div.get_text('\n', strip=True)
        else:
            # Если блока с текстом нет, это может быть медиафайл или стикер
            message_text = "[Медиафайл или сервисное сообщение]"

        # Форматируем строку для записи в файл
        formatted_line = f"[{date_str}] {sender_name}: {message_text}"
        conversation_lines.append(formatted_line)

    # Сохраняем все строки в один текстовый файл
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # Объединяем все строки, разделяя их двойным переносом для лучшей читаемости
            f.write('\n\n'.join(conversation_lines))
        print(f"Конвертация завершена. Результат сохранен в файл: {output_file}")
    except Exception as e:
        print(f"Произошла ошибка при сохранении файла: {e}")


if __name__ == "__main__":
    print("--- Скрипт для конвертации HTML-лога Telegram в TXT ---")
    
    input_file_path = input("Введите путь к вашему HTML-файлу лога (например, messages.html): ").strip()

    if not os.path.isfile(input_file_path):
        print(f"Ошибка: файл по пути '{input_file_path}' не найден.")
    else:
        # Формируем имя для выходного файла (меняем расширение на .txt)
        base, ext = os.path.splitext(input_file_path)
        output_file_path = f"{base}.txt"

        # Запускаем основную функцию
        convert_html_to_txt(input_file_path, output_file_path)
