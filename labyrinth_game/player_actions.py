#!/usr/bin/env python3
"""
Действия игрока для игры
"""

from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room


def get_input(prompt="> "):
    """Получить ввод от пользователя"""
    
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    """Переместить игрока в указанном направлении"""
    
    current_room = game_state['current_room']
    room_data = ROOMS.get(current_room, {})
    exits = room_data.get('exits', {})
    
    if direction in exits:
        # Обновляем текущую комнату
        game_state['current_room'] = exits[direction]
        # Увеличиваем счетчик шагов
        game_state['steps_taken'] += 1
        # Выводим описание новой комнаты
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    """Взять предмет из комнаты"""
    
    current_room = game_state['current_room']
    room_data = ROOMS.get(current_room, {})
    items = room_data.get('items', [])
    
    # Проверка на сундук с сокровищами
    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return
    
    if item_name in items:
        # Добавляем в инвентарь
        game_state['player_inventory'].append(item_name)
        # Удаляем из комнаты
        items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def show_inventory(game_state):
    """Показать инвентарь игрока"""
    
    inventory = game_state['player_inventory']
    if not inventory:
        print("Ваш инвентарь пуст.")
    else:
        print("Ваш инвентарь:")
        for item in inventory:
            print(f"  - {item}")


def use_item(game_state, item_name):
    """Использовать предмет из инвентаря"""
    
    inventory = game_state['player_inventory']
    
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return
    
    # Уникальные действия для предметов
    if item_name == 'torch':
        print("Вы зажигаете факел. Стало светлее.")
    elif item_name == 'sword':
        print("Вы чувствуете себя увереннее с мечом в руках.")
    elif item_name == 'bronze_box':
        print("Вы открываете бронзовую шкатулку.")
        if 'rusty_key' not in inventory:
            inventory.append('rusty_key')
            print("Внутри вы находите ржавый ключ!")
        else:
            print("Шкатулка пуста.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
