#!/usr/bin/env python3

from labyrinth_game.constants import DIRECTIONS, ROOMS


class Player:
    """Класс игрока для отслеживания"""

    def __init__(self):
        self.current_room = 'entrance'
        self.inventory = []
        self.solved_puzzles = set()

    def move(self, direction: str) -> str:
        """Переместить игрока в указанном направлении"""

        if direction not in DIRECTIONS:
            return f"Неверное направление: {direction}. Доступные направления: {', '.join(DIRECTIONS)}"

        current_room_data = ROOMS.get(self.current_room, {})
        exits = current_room_data.get('exits', {})

        if direction in exits:
            next_room = exits[direction]
            self.current_room = next_room
            return f"Вы идете {direction} в {next_room}."
        else:
            return f"Вы не можете пойти {direction} отсюда."

    def look_around(self) -> str:
        """Описание комнаты"""

        room_data = ROOMS.get(self.current_room, {})
        description = room_data.get('description', 'Неизвестная комната.')

        exits = room_data.get('exits', {})
        if exits:
            exit_dirs = ', '.join(exits.keys())
            description += f"\nВыходы: {exit_dirs}"

        items = room_data.get('items', [])
        if items:
            items_list = ', '.join(items)
            description += f"\nПредметы здесь: {items_list}"

        puzzle = room_data.get('puzzle')
        if puzzle and self.current_room not in self.solved_puzzles:
            description += f"\n\nЗагадка: {puzzle[0]}"

        return description

    def take_item(self, item_name: str) -> str:
        """Взять предмет из текущей комнаты"""

        room_data = ROOMS.get(self.current_room, {})
        items = room_data.get('items', [])

        if item_name in items:
            self.inventory.append(item_name)
            items.remove(item_name)
            return f"Вы берете {item_name}."
        else:
            return f"Здесь нет {item_name}."

    def show_inventory(self) -> str:
        """Показать инвентарь"""

        if not self.inventory:
            return "Ваш инвентарь пуст"
        else:
            return f"Инвентарь: {', '.join(self.inventory)}"

    def solve_puzzle(self, answer: str) -> str:
        """Попытаться решить загадку"""

        if self.current_room in self.solved_puzzles:
            return "Эта загадка уже решена."

        room_data = ROOMS.get(self.current_room, {})
        puzzle = room_data.get('puzzle')

        if not puzzle:
            return "В этой комнате нет загадки."

        if answer.lower().strip() == puzzle[1].lower():
            self.solved_puzzles.add(self.current_room)
            return "Верно! Загадка решена."
        else:
            return "Неправильный ответ. Попробуйте снова."


def show_help() -> str:
    """Показать доступные команды и их описание"""

    help_text = "Доступные команды:\n"
    from labyrinth_game.constants import COMMANDS
    for cmd, desc in COMMANDS.items():
        help_text += f"  {cmd}: {desc}\n"
    return help_text
