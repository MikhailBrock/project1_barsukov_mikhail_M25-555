#!/usr/bin/env python3
"""
Вспомогательные функции.
"""

def clear_screen():
    """Очистить экран терминала"""

    print("\033[H\033[J", end="")


def print_welcome_message():
    """Приветственное сообщение"""
    print("=== ЛАБИРИНТ ===")
    print("Найди путь через лабиринт комнат.")
    print("Решай загадки, собирай предметы и найдите сокровище!")
    print("Введите 'help' для списка команд.\n")


def format_command(input_string: str) -> tuple[str, str]:
    """Ввод пользователя"""

    parts = input_string.strip().lower().split()
    if not parts:
        return "", ""

    command = parts[0]
    argument = " ".join(parts[1:]) if len(parts) > 1 else ""

    return command, argument


def print_room_title(room_name: str):
    """Вывести название комнаты"""

    print(f"\n=== {room_name.upper()} ===")
