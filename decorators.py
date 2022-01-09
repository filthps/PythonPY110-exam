import time
import sys
from typing import Callable


def exec_time(f: Callable) -> Callable:
    """
    Подсчёт времени выполнения декорируемой функции

    :param f: декорируемая функция
    :return: функция - обёртка
    """
    def func(*a):
        time_start = time.time()
        val = f(*a)
        print(f"{round((time.time() - time_start) * 1000)}ms")
        return val
    return func


def books_filter(length: int) -> Callable:
    """
    Фабрика декораторов

    Возбудить ValueError, если длина названия книги больше,
    чем задано параметром

    :param length: допустимая длина символов в названии книги
    :return: функция - декоратор
    """
    def decorator(f):
        def func(*args):
            book_name = f(*args)
            if len(book_name) > length:
                raise ValueError()
            return book_name
        return func
    return decorator


def cache_lines(f: Callable) -> Callable:
    """
    Хранить в cached_lines индексы валидных строк

    :param f: декорируемая функция
    :return: функция - обёртка
    """
    cached_lines: list[list[int], list[int]] = [[], []]

    def wrap():
        nonlocal cached_lines
        if not cached_lines[0]:
            with open("books.txt", encoding="utf-8") as file:
                value = [i for i, s in enumerate(file) if s[0] != "\n"]
            if not value:
                raise ValueError("Файл списка книг пуст")
            items = value.copy()
            cached_lines[0], cached_lines[1] = value, items
            print(f"Ссылки на валидные строки в файле: {sys.getsizeof(value) // 1000}кб")
        else:
            items = cached_lines[1]
            if not items:
                items = cached_lines[0].copy()
                cached_lines[1] = items
        return f(items)
    return wrap


def lock_books_file(func: Callable) -> Callable:
    """
    Блокировка файла books.txt на время работы главной функции
    :param func: декорируемая функция
    :return: функция - обёртка
    """

    def wrapper(*args):
        file = open("books.txt", "a")
        result = func(*args)
        file.close()
        return result
    return wrapper
