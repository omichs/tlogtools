import os
from bs4 import BeautifulSoup

def rename_user_in_html(input_file, output_file, old_name, new_name):
    """
    Находит все вхождения old_name в блоках с именами пользователей
    в HTML-файле и заменяет их на new_name.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            print(f"Чтение файла: {input_file}...")
            soup = BeautifulSoup(f, 'lxml')
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден.")
        return

    # В логах Telegram имя отправителя находится в блоке <div class="from_name">
    # Это позволяет нам изменять только имена, не трогая текст сообщений.
    name_tags = soup.find_all('div', class_='from_name')

    if not name_tags:
        print("Предупреждение: не найдено ни одного блока с именем пользователя (div.from_name).")
        print("Проверьте, что это действительно файл логов Telegram.")
        return

    replacements_count = 0
    print(f"Поиск имени '{old_name}' для замены на '{new_name}'...")

    for tag in name_tags:
        # .strip() убирает лишние пробелы и переносы строк вокруг имени
        if tag.get_text(strip=True) == old_name:
            # Заменяем содержимое тега на новое имя
            tag.string = new_name
            replacements_count += 1
            
            # Мы не трогаем атрибут style, чтобы сохранить цвет пользователя
            # tag['style'] = "color: #НовыйЦвет;" # <- Раскомментируйте, если хотите менять и цвет

    if replacements_count > 0:
        print(f"Найдено и заменено вхождений: {replacements_count}")
        # Сохраняем измененный HTML в новый файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Успешно сохранено в новый файл: {output_file}")
    else:
        print(f"Имя '{old_name}' не найдено в файле. Никаких изменений не сделано.")


if __name__ == "__main__":
    print("--- Скрипт для замены имени в логах Telegram ---")
    
    # 1. Получаем имя файла
    input_file_path = input("Введите путь к HTML-файлу лога (например, merged_chat.html): ")

    # 2. Получаем старое имя
    old_user_name = input("Введите имя, которое нужно заменить (точное совпадение): ")

    # 3. Получаем новое имя
    new_user_name = input("Введите новое имя: ")

    if not input_file_path or not old_user_name or not new_user_name:
        print("Ошибка: Все поля должны быть заполнены. Выход.")
    elif old_user_name == new_user_name:
        print("Старое и новое имена совпадают. Замена не требуется. Выход.")
    else:
        # Формируем имя для выходного файла
        base, ext = os.path.splitext(input_file_path)
        output_file_path = f"{base}_renamed{ext}"

        # Запускаем основную функцию
        rename_user_in_html(input_file_path, output_file_path, old_user_name, new_user_name)

