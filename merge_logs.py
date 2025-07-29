import os
import glob
import re
from bs4 import BeautifulSoup

# --- Настройки ---
# Папка, в которой лежат ваши HTML-файлы от Telegram
input_directory = '.' 
# Название для итогового объединенного файла
output_filename = 'merged_chat.html'
# Шаблон для поиска файлов (стандартный для экспорта Telegram)
file_pattern = 'messages*.html'
# --- Конец настроек ---

def get_file_number(filename):
    """
    Извлекает номер из имени файла для корректной хронологической сортировки.
    Пример:
    'messages.html' -> 1
    'messages2.html' -> 2
    'messages10.html' -> 10
    """
    # Извлекаем только имя файла из полного пути
    base_name = os.path.basename(filename)
    
    # Ищем число в имени файла, например, '2' в 'messages2.html'
    match = re.search(r'messages(\d+)\.html', base_name)
    if match:
        # Если нашли число, возвращаем его как целое число
        return int(match.group(1))
    
    # Файл 'messages.html' без номера по умолчанию является первым
    if base_name == 'messages.html':
        return 1
    
    # Для любых других файлов, которые не подходят под шаблон, 
    # возвращаем очень большое число, чтобы они оказались в конце.
    return float('inf')

print("Поиск файлов для объединения...")

# Составляем полный путь для поиска файлов
search_path = os.path.join(input_directory, file_pattern)

# Находим все файлы, подходящие под шаблон
file_list_unsorted = glob.glob(search_path)

# *** Ключевое изменение: сортируем файлы с помощью нашей функции ***
file_list = sorted(file_list_unsorted, key=get_file_number)

if not file_list:
    print(f"Файлы по шаблону '{file_pattern}' не найдены в папке '{input_directory}'.")
    exit()

print(f"Найдено файлов: {len(file_list)}")
print("Файлы будут объединены в следующем порядке:")
for f in file_list:
    print(f"- {f}")

# Берем за основу первый файл для извлечения <head> со стилями
print("\nИзвлечение стилей из первого файла...")
with open(file_list[0], 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')
    head_content = soup.head

# Создаем новый HTML-файл для записи
with open(output_filename, 'w', encoding='utf-8') as outfile:
    # Записываем начало HTML-документа и секцию <head>
    outfile.write('<!DOCTYPE html>\n')
    outfile.write('<html>\n')
    outfile.write(str(head_content))
    outfile.write('\n<body>\n')

    # Проходим по каждому файлу в отсортированном порядке и добавляем его содержимое
    for filename in file_list:
        print(f"Обработка файла: {filename}...")
        with open(filename, 'r', encoding='utf-8') as infile:
            soup = BeautifulSoup(infile, 'lxml')
            
            # В логах Telegram основное содержимое находится внутри <div class="page_body">
            body_content = soup.find('div', class_='page_body')
            
            if body_content:
                # Извлекаем все сообщения из этого блока
                messages = body_content.find_all('div', class_='message')
                for message in messages:
                    outfile.write(str(message))
            else:
                print(f"  - Предупреждение: не найден блок <div class=\"page_body\"> в файле {filename}")

    # Завершаем HTML-документ
    outfile.write('\n</body>\n')
    outfile.write('</html>\n')

print(f"\nГотово! Все файлы успешно объединены в один: {output_filename}")
