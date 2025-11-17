#!/usr/bin/env python3

from labyrinth_game import utils
from labyrinth_game.player_actions import Player, show_help


def main():
    """Основной игровой цикл"""

    utils.clear_screen()
    utils.print_welcome_message()
    
    player = Player()
    game_running = True
    
    game_state = {
        'player_inventory': [],  # Инвентарь игрока
        'current_room': 'entrance',  # Текущая комната
        'game_over': False,      # Значение окончания игры
        'steps_taken': 0         # Количество шагов
    }
    
    # Синхронизируем начальное состояние с игроком
    game_state['current_room'] = player.current_room
    game_state['player_inventory'] = player.inventory
    
    # Показать описание начальной комнаты
    utils.print_room_title(player.current_room)
    print(player.look_around())
    
    while game_running and not game_state['game_over']:
        user_input = input("\n> ")
        command, argument = utils.format_command(user_input)
        
        # Увеличиваем счетчик шагов для большинства команд
        if command and command not in ['help', 'inventory', 'look']:
            game_state['steps_taken'] += 1
        
        if command == "quit":
            print("Спасибо за игру! До свидания!")
            print(f"Вы сделали {game_state['steps_taken']} шагов.")
            game_running = False
            
        elif command == "help":
            print(show_help())
            
        elif command == "look":
            utils.print_room_title(player.current_room)
            print(player.look_around())
            
        elif command == "go":
            if argument:
                result = player.move(argument)
                print(result)
                # Обновляем состояние после перемещения
                game_state['current_room'] = player.current_room
                # Показать новую комнату после перемещения
                if "go" in result.lower():
                    utils.print_room_title(player.current_room)
                    print(player.look_around())
            else:
                print("Укажите направление.")
                
        elif command == "take":
            if argument:
                result = player.take_item(argument)
                print(result)
                # Обновляем инвентарь в состоянии игры
                game_state['player_inventory'] = player.inventory
            else:
                print("Укажите предмет.")
                
        elif command == "inventory":
            print(player.show_inventory())
            print(f"Шагов сделано: {game_state['steps_taken']}")
                
        elif command == "slove":
            if argument:
                result = player.solve_puzzle(argument)
                print(result)
                # Проверяем условия победы после решения загадки
                if "Верно" in result:
                    check_win_condition(player, game_state)
            else:
                print("Укажите ответ.")
                
        elif command == "state":
            show_game_status(game_state, player)
                
        elif command == "":
            continue
            
        else:
            print(f"Неизвестная команда: '{command}'. Введите 'помощь' для списка команд.")


def show_game_status(game_state: dict, player: Player):
    """Показать текущее состояние игры"""

    print("\n=== СТАТУС ИГРЫ ===")
    print(f"Текущая комната: {game_state['current_room']}")
    print(f"Шагов сделано: {game_state['steps_taken']}")
    print(f"Предметов в инвентаре: {len(game_state['player_inventory'])}")
    
    if game_state['player_inventory']:
        print(f"Инвентарь: {', '.join(game_state['player_inventory'])}")
    else:
        print("Инвентарь: пуст")
    
    # Проверяем прогресс
    from labyrinth_game.constants import ROOMS
    total_rooms = len(ROOMS)
    visited_rooms = 1  # Начинаем с текущей комнаты
    solved_puzzles = len(player.solved_puzzles)
    
    print("\nПрогресс:")
    print(f"- Комнат исследовано: {visited_rooms}/{total_rooms}")
    print(f"- Загадок решено: {solved_puzzles}")


def check_win_condition(player: Player, game_state: dict):
    """Проверить условия победы в игре"""

    from labyrinth_game.constants import ROOMS
    
    # Условие победы: решены все загадки и найден сундук с сокровищами
    total_puzzles = sum(1 for room in ROOMS.values() if room.get('puzzle'))
    puzzles_solved = len(player.solved_puzzles)
    
    has_treasure = 'treasure_chest' in player.inventory
    
    if puzzles_solved >= total_puzzles and has_treasure:
        print("\n ПОЗДРАВЛЯЕМ! ")
        print("Вы решили все загадки и нашли сокровище!")
        print(f"Игра завершена за {game_state['steps_taken']} шагов.")
        game_state['game_over'] = True
        
    elif puzzles_solved >= total_puzzles:
        print("\n Вы решили все загадки! Теперь найдите сундук с сокровищами.")
        
    elif has_treasure and puzzles_solved < total_puzzles:
        print("\n У вас есть сокровище, но остались нерешенные загадки.")


if __name__ == "__main__":
    main()
