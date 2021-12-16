import time
import traceback
from typing import Callable


def exec_time(f):
    """
    Декоратор.
    Подсчёт времени выполнения декорируемой функции.
    """
    def func(*a):
        time_start = time.time()
        f(*a)
        print(f"{round((time.time() - time_start) * 1000)}ms")
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


def cache_lines(f):
    """
    Декоратор сохраняющий в cached_lines индексы валидных строк
    """
    cached_lines: list = [[], []]

    def wrap():
        nonlocal cached_lines
        if not cached_lines[0]:
            try:
                with open("books.txt", encoding="utf-8") as file:
                    value = [i for i, s in enumerate(file) if s[0] != "\n"]
            except OSError:
                traceback.print_exc()
            if not value:
                raise ValueError("Файл списка книг пуст")
            items = value.copy()
            cached_lines[0], cached_lines[1] = value, items
        else:
            items = cached_lines[1]
            if not items:
                items = cached_lines[0].copy()
                cached_lines[1] = items
        return f(items)
    return wrap
