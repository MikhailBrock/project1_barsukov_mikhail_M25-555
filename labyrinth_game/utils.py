#!/usr/bin/env python3
"""
Вспомогательные функции для игры
"""

from labyrinth_game.constants import ROOMS


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
    answer = input("Ваш ответ: ")
    
    if answer.strip().lower() == puzzle[1].lower():
        print("Правильно! Загадка решена.")
        # Убираем загадку из комнаты
        room_data['puzzle'] = None
        # Добавляем награду
        if 'reward' in room_data:
            game_state['player_inventory'].append(room_data['reward'])
            print(f"Вы получаете: {room_data['reward']}")
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
    """Попытаться открыть сундук с сокровищами"""
    
    current_room = game_state['current_room']
    if current_room != 'treasure_room':
        print("Здесь нет сундука с сокровищами.")
        return
    
    room_data = ROOMS.get(current_room, {})
    
    # Проверка ключа
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
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
        if puzzle and code.strip() == puzzle[1]:
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
    """Показать справку по командам."""
    
    from labyrinth_game.constants import COMMANDS
    print("\nДоступные команды:")
    for cmd, desc in COMMANDS.items():
        print(f"  {cmd}: {desc}")
