import os
from bs4 import BeautifulSoup, Tag

def create_split_file(filename: str, head_template: Tag, messages_list: list):
    """
    Создает новый HTML-файл, вставляет в него шапку со стилями
    и добавляет указанный список сообщений.
    """
    # Создаем базовую структуру нового HTML-документа
    new_soup = BeautifulSoup('<!DOCTYPE html><html><body></body></html>', 'lxml')

    # Проверяем, существует ли шапка, прежде чем ее копировать
    if head_template:
        # Создаем глубокую копию тега <head>, чтобы не изменять оригинал.
        # Это надежный способ, который не повредит исходный объект.
        copied_head = BeautifulSoup(str(head_template), 'lxml').head
        if copied_head:
            new_soup.html.insert(0, copied_head)

    # Получаем доступ к телу <body> нового документа
    body_tag = new_soup.body

    # Добавляем все сообщения из списка в тело документа
    for message in messages_list:
        body_tag.append(message)

    # Сохраняем результат в файл
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # prettify() делает HTML более читаемым
            f.write(str(new_soup.prettify()))
        print(f"-> Успешно создан файл '{filename}' с {len(messages_list)} сообщениями.")
    except Exception as e:
        print(f"Ошибка при сохранении файла '{filename}': {e}")


def split_telegram_log(input_file: str):
    """
    Основная функция для разделения HTML-лога на две части.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            print(f"Чтение файла '{input_file}'...")
            soup = BeautifulSoup(f, 'lxml')
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден.")
        return

    # Находим <head> из исходного файла, чтобы сохранить все стили
    original_head = soup.head
    if not original_head:
        print("Предупреждение: Тег <head> не найден в исходном файле. Стили не будут скопированы.")

    # Находим все блоки сообщений в документе по их классу
    messages = soup.find_all('div', class_='message')

    total_messages = len(messages)
    if total_messages < 2:
        print("В файле найдено менее двух сообщений. Разделение невозможно.")
        return

    print(f"Всего найдено сообщений: {total_messages}")

    # Находим точку разделения (середину)
    split_point = total_messages // 2
    print(f"Файл будет разделен после {split_point}-го сообщения.")

    # Делим список сообщений на две части
    messages_part1 = messages[:split_point]
    messages_part2 = messages[split_point:]

    # Генерируем имена для новых файлов
    base_name, extension = os.path.splitext(input_file)
    output_file1 = f"{base_name}_part1{extension}"
    output_file2 = f"{base_name}_part2{extension}"
    
    # Создаем первый файл
    create_split_file(output_file1, original_head, messages_part1)
    
    # Создаем второй файл
    create_split_file(output_file2, original_head, messages_part2)
    
    print("\nГотово! Файл успешно разделен на две части.")


if __name__ == "__main__":
    print("--- Скрипт для разделения HTML-лога Telegram на две части ---")
    
    # Запрашиваем у пользователя имя файла
    input_file_path = input("Введите имя вашего большого HTML-файла (например, messages.html): ").strip()

    if not os.path.isfile(input_file_path):
        print(f"Ошибка: Не удалось найти файл по пути '{input_file_path}'.")
    else:
        # Запускаем процесс разделения
        split_telegram_log(input_file_path)
