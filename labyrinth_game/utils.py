#!/usr/bin/env python3
"""
Вспомогательные функции для игры
"""

import math

from labyrinth_game.constants import PUZZLE_ANSWERS, ROOMS


def pseudo_random(seed, modulo):
    """Генератор псевдослучайных чисел"""
    
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    return math.floor(fractional * modulo)


def trigger_trap(game_state):
    """Активировать ловушку"""
    
    print("Ловушка активирована! Пол стал дрожать...")
    
    inventory = game_state['player_inventory']
    
    if inventory:
        # Выбираем случайный предмет для удаления
        item_index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(item_index)
        print(f"Вы потеряли: {lost_item}!")
    else:
        # Игрок получает "урон"
        damage_chance = pseudo_random(game_state['steps_taken'], 10)
        if damage_chance < 3:
            print("Вы получили смертельную травму! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам удалось уцелеть, но это было близко!")


def random_event(game_state):
    """Случайное событие при перемещении"""
    
    # Проверяем, произойдет ли событие (10% вероятность)
    event_chance = pseudo_random(game_state['steps_taken'], 10)
    if event_chance != 0:
        return
    
    # Выбираем тип события
    event_type = pseudo_random(game_state['steps_taken'] + 1, 3)
    current_room = game_state['current_room']
    room_data = ROOMS.get(current_room, {})
    
    match event_type:
        case 0:
            # Находка
            print("Вы заметили что-то блестящее на полу...")
            if 'coin' not in room_data['items']:
                room_data['items'].append('coin')
                print("Вы нашли монетку!")
            else:
                print("Но это оказалась всего лишь пыль.")
                
        case 1:
            # Испуг
            print("Вы слышите странный шорох из темноты...")
            if 'sword' in game_state['player_inventory']:
                print("Вы достаете меч, и шорох мгновенно прекращается.")
            else:
                print("Шорох приближается... вам стало не по себе.")
                
        case 2:
            # Ловушка
            if current_room == 'trap_room' and 'torch' not in game_state['player_inventory']:
                print("Вы чувствуете, как пол под ногами начинает двигаться...")
                trigger_trap(game_state)
            else:
                print("Вам показалось, что что-то щелкнуло, но ничего не произошло.")


def describe_current_room(game_state):
    """Описать текущую комнату"""
    
    current_room = game_state['current_room']
    room_data = ROOMS.get(current_room, {})
    
    # Название комнаты
    print(f"\n=== {current_room.upper()} ===")
    
    # Описание комнаты
    print(room_data.get('description', 'Неизвестная комната.'))
    
    # Предметы
    items = room_data.get('items', [])
    if items:
        print("\nЗаметные предметы:")
        for item in items:
            print(f"  - {item}")
    
    # Выходы
    exits = room_data.get('exits', {})
    if exits:
        print(f"\nВыходы: {', '.join(exits.keys())}")
    
    # Загадка
    puzzle = room_data.get('puzzle')
    if puzzle:
        print("\nКажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    """Решить загадку в текущей комнате"""
    
    current_room = game_state['current_room']
    room_data = ROOMS.get(current_room, {})
    puzzle = room_data.get('puzzle')
    
    if not puzzle:
        print("Загадок здесь нет.")
        return
    
    print(f"\nЗагадка: {puzzle[0]}")
    answer = input("Ваш ответ: ").strip().lower()
    
    # Проверяем альтернативные варианты ответов
    correct_answers = PUZZLE_ANSWERS.get(puzzle[1], [puzzle[1]])
    
    if answer in correct_answers:
        print("Правильно! Загадка решена.")
        # Убираем загадку из комнаты
        room_data['puzzle'] = None
        
        # Награда в зависимости от комнаты
        if current_room == 'hall':
            game_state['player_inventory'].append('silver_key')
            print("Вы получаете: silver_key")
        elif current_room == 'trap_room':
            print("Ловушка деактивирована! Теперь вы можете безопасно перемещаться.")
        elif current_room == 'library':
            game_state['player_inventory'].append('ancient_scroll')
            print("Вы получаете: ancient_scroll")
            
    else:
        print("Неверно. Попробуйте снова.")
        # В trap_room неверный ответ активирует ловушку
        if current_room == 'trap_room':
            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    """Попытаться открыть сундук с сокровищами"""
    
    current_room = game_state['current_room']
    if current_room != 'treasure_room':
        print("Здесь нет сундука с сокровищами.")
        return
    
    room_data = ROOMS.get(current_room, {})
    
    # Проверка ключа
    if 'rusty_key' in game_state['player_inventory']:
        print("Вы применяете ржавый ключ, и замок щёлкает. Сундук открыт!")
        if 'treasure_chest' in room_data['items']:
            room_data['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return
    
    # Предложение ввести код
    print("Сундук заперт. У вас нет ключа. Ввести код? (да/нет)")
    choice = input("> ").lower().strip()
    
    if choice == 'да':
        code = input("Введите код: ")
        puzzle = room_data.get('puzzle')
        if puzzle and code.strip() in PUZZLE_ANSWERS.get(puzzle[1], [puzzle[1]]):
            print("Код верный! Сундук открыт!")
            if 'treasure_chest' in room_data['items']:
                room_data['items'].remove('treasure_chest')
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
        else:
            print("Неверный код.")
    else:
        print("Вы отступаете от сундука.")


def show_help():
    """Показать справку по командам"""
    
    from labyrinth_game.constants import COMMANDS
    print("\nДоступные команды:")
    for cmd, desc in COMMANDS.items():
        print(f"  {cmd:<16} - {desc}")
