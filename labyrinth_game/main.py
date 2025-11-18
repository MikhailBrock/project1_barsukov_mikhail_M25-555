#!/usr/bin/env python3
"""
Главный модуль игры
"""

from labyrinth_game.constants import DIRECTIONS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command_line):
    """Обработать команду пользователя"""
    
    parts = command_line.strip().lower().split()
    if not parts:
        return
    
    command = parts[0]
    argument = " ".join(parts[1:]) if len(parts) > 1 else ""
    
    # Обработка односложных команд движения
    if command in DIRECTIONS:
        move_player(game_state, command)
        return
    
    match command:
        case "look":
            describe_current_room(game_state)
            
        case "go":
            if argument:
                move_player(game_state, argument)
            else:
                print("Куда идти? Укажите направление.")
                
        case "take":
            if argument:
                take_item(game_state, argument)
            else:
                print("Что взять? Укажите предмет.")
                
        case "inventory":
            show_inventory(game_state)
            
        case "use":
            if argument:
                use_item(game_state, argument)
            else:
                print("Что использовать? Укажите предмет.")
                
        case "solve":
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
                
        case "help":
            show_help()
            
        case "quit" | "exit":
            print("Спасибо за игру! До свидания!")
            game_state['game_over'] = True
            
        case _:
            message = f"Неизвестная команда: '{command}'. "
            message += "Введите 'help' для списка команд."
            print(message)


def main():
    """Основной игровой цикл"""
    
    # Инициализация состояния игры
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0
    }
    
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)
    
    # Основной игровой цикл
    while not game_state['game_over']:
        command = get_input("\n> ")
        if command == "quit":
            game_state['game_over'] = True
            break
        process_command(game_state, command)


if __name__ == "__main__":
    main()
