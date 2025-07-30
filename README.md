# tlogtools

Инструменты для работы с логами Telegram

![GitHub stars](https://img.shields.io/github/stars/ВАШ_ЮЗЕРНЕЙМ/tlogtools.svg)
![GitHub forks](https://img.shields.io/github/forks/ВАШ_ЮЗЕРНЕЙМ/tlogtools.svg)
![GitHub issues](https://img.shields.io/github/issues/ВАШ_ЮЗЕРНЕЙМ/tlogtools.svg)
![MIT License](https://img.shields.io/badge/license-MIT-green.svg)

## 📖 Описание

**tlogtools** — это набор лёгких скриптов Python для обработки и анализа логов переписки Telegram (HTML-экспорт). Позволяют разбивать, объединять, конвертировать и фильтровать логи, а также работать со ссылками и именами пользователей.

---

## 🚀 Быстрый старт

1. Клонируйте репозиторий:
    ```
    git clone https://github.com/ВАШ_ЮЗЕРНЕЙМ/tlogtools.git
    cd tlogtools
    ```
2. Установите зависимости:
    ```
    pip install beautifulsoup4 lxml
    ```
3. Запустите нужный скрипт:
    ```
    python имя_скрипта.py
    ```

---

## 🛠️ Скрипты и их назначение

| Скрипт                | Описание                                                                           |
|-----------------------|------------------------------------------------------------------------------------|
| `split_log.py`        | Разделяет HTML-файл чата на части                                                  |
| `merge_logs.py`       | Объединяет несколько HTML-файлов в один                                            |
| `html_to_txt.py`      | Конвертирует лог из HTML в TXT                                                     |
| `html_to_json.py`     | Конвертирует лог из HTML в JSON                                                    |
| `extract_links_tel.py`| Находит все **внешние** ссылки в логе и сохраняет их в TXT                         |
| `rename_user.py`      | Заменяет все вхождения `old_name` на `new_name` в блоках имён в HTML-файле         |

---

## 📋 Пример использования

