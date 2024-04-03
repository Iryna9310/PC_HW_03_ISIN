import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging

# Створення парсера для обробки аргументів командного рядка
parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

# Отримання аргументів командного рядка
args = vars(parser.parse_args())

# Встановлення шляху до директорії джерела та цільової директорії
source = Path(args.get("source"))
output = Path(args.get("output"))

# Список для збереження шляхів до папок для копіювання
folders = []

# Функція для рекурсивного збору шляхів до всіх піддиректорій джерела
def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)

# Функція для копіювання файлів з директорії джерела відповідно до їх розширень
def copy_file(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            # Визначення розширення файлу
            ext = el.suffix[1:]
            # Визначення цільової директорії для файлу за розширенням
            ext_folder = output / ext
            try:
                # Створення цільової директорії, якщо вона не існує
                ext_folder.mkdir(exist_ok=True, parents=True)
                # Копіювання файлу в цільову директорію
                copyfile(el, ext_folder / el.name)
            except OSError as err:
                logging.error(err)

if __name__ == "__main__":
    # Налаштування рівня журналізації
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

    # Додавання джерела до списку папок для копіювання
    folders.append(source)
    # Збір шляхів до папок для копіювання
    grabs_folder(source)

    # Створення та запуск потоків для копіювання файлів з кожної папки
    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    # Очікування завершення всіх потоків
    [th.join() for th in threads]
    # Вивід повідомлення про завершення операції копіювання
    print(f"Можна видалять {source}")