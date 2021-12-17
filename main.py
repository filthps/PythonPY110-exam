import json
from typing import Generator
from random import randint, choice, uniform

from faker import Faker

from decorators import *

from conf import MODEL, TITTLE_STRING_LENGTH, CURRENT_YEAR


fake = Faker()  # faker generator


@lock_books_file
@exec_time
def main(pk: int = 1) -> None:
    """
    Главная функция

    :param pk: порядковый номер книги
    """
    gen = book_gen(pk)
    books = (next(gen) for _ in range(100))
    with open("books_new.txt", "w", encoding="utf-8") as file:
        file.write(json.dumps(list(books), ensure_ascii=False, indent=4))


def book_gen(primary_key: int) -> Generator:
    """
    :param primary_key: порядковый номер книги
    :return: выражение генератор, возвращающий список словарей
    """
    while True:
        yield {
            "model": MODEL,
            "pk": primary_key,
            "fields": {
                "tittle": get_tittle(),
                "year": get_year(),
                "pages": count_pages(),
                "isbn13": get_isbn(),
                "rating": get_rating(),
                "author": get_authors(),
                "price": get_price(),
            }
        }
        primary_key += 1


def get_year(start_year: int = 1950, end_year: int = CURRENT_YEAR) -> int:
    """
    Сгенерировать при помощи randint число - дату публикации книги

    :param start_year: год начала публикации клиг
    :param end_year: текущий год
    :return: произвольный год
    """
    return randint(start_year, end_year)


@cache_lines
@books_filter(TITTLE_STRING_LENGTH)
def get_tittle(available_lines: list[int]):
    """
    Прочитать файл books.txt и вернуть случайную строку

    :param available_lines: Список с индексами валидных строк из файла books.txt
    :return: случайная строка, отобранная из списка валидных
    """
    ch = choice(available_lines)
    with open("books.txt", encoding="utf-8") as file:
        output = list((s.strip() for i, s in enumerate(file) if i == ch))[0]
    available_lines.remove(ch)
    return output


def count_pages(lowest_book_size=100, highest_book_size=500) -> int:
    """
    Сгенерировать при помощи randint число - количество страниц в книге

    :return: целое случайное число в диапазоне от 100 до 500
    """
    return randint(lowest_book_size, highest_book_size)


def get_isbn() -> str:
    """
    Сгенерировать при помощи модуля Faker номер isbn

    :return: строка isbn
    """
    return fake.isbn13()


def get_rating(lowest_rating: float = 0.0, highest_rating: float = 5.0) -> float:
    """
    Сгенерировать при помощи uniform рейтинг книги

    :return: случайное число float в диапазоне от 0.0 до 5.0
    """
    return uniform(lowest_rating, highest_rating)


def get_price(start: float = 1.0, end: float = 100.0) -> float:
    """
    Сгенерировать при помощи uniform цену книги

    :return: число float от 1.0 до 100.0
    """
    return uniform(start, end)


def get_authors() -> list[str]:
    """
    Сгенерировать при помощи модуля Faker имена авторов книг

    :return: список строк с именами авторов, авторов в списке от 1 до 3
    """
    return [fake.name() for _ in range(randint(1, 3))]


if __name__ == "__main__":
    main()
