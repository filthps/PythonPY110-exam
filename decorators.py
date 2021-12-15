import time
from typing import Callable


lines = []


def exec_time(f):
    """
    Декоратор.
    Подсчёт времени выполнения декорируемой функции.
    """
    def func(*a):
        time_start = time.time()
        f(*a)
        print(time.time() - time_start)
    return func


def books_filter(length: int) -> Callable:
    """
    Возбудить ValueError, если длина названия книги больше,
    чем задано параметром

    :param length: Допустимая длина названия книги
    :return: Декоратор
    """
    def decorator(f):
        def func(*args):
            book_name = f(*args)
            if len(book_name) > length:
                raise ValueError()
            return book_name
        return func
    return decorator


def count_lines(func):
    """
    Декоратор.
    Кэшировать на 1 запуск функции main
    список lines, содержащий индексы
    "правильных", не пустых строк.
    Возбудить ValueError, если файл пуст.
    """
    def wrap(*a):
        global lines
        if not lines:
            try:
                with open("books.txt", encoding="utf-8") as file:
                    lines = [i for i, s in enumerate(file) if s[0] != "\n"]
                    if not lines:
                        raise ValueError("Файл с книгами пуст")
            except OSError:
                raise OSError("Файл с книгами недоступен")
        tittle = func(lines)
        return tittle
    return wrap
