#!/usr/bin/env python3

from labyrinth_game import utils
from labyrinth_game.player_actions import Player, show_help


def main():
    """Основной цикл игры"""

    utils.clear_screen()
    utils.print_welcome_message()

    player = Player()
    game_running = True

    utils.print_room_title(player.current_room)
    print(player.look_around())

    while game_running:
        user_input = input("\n> ")
        command, argument = utils.format_command(user_input)

        if command == "quit":
            print("Спасибо за игру! До свидания!")
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

                if "move" in result.lower():
                    utils.print_room_title(player.current_room)
                    print(player.look_around())
            else:
                print("Укажите направление")

        elif command == "take":
            if argument:
                print(player.take_item(argument))
            else:
                print("Укажите предмет.")

        elif command == "inventory":
            print(player.show_inventory())

        elif command == "solve":
            if argument:
                print(player.solve_puzzle(argument))
            else:
                print("Укажите ответ.")

        elif command == "":
            continue

        else:
            print(f"Неизвестная команда: '{command}'. Введите 'help' для списка команд.")


if __name__ == "__main__":
    main()
