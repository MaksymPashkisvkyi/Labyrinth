# Ccылка на игровую Карту 👇🏻 https://1.bp.blogspot.com/-IXplOdXWc70/VNcARys7KpI/AAAAAAAAZjI/H3Xb4GDPJHs/s1600
# /Labirint.png
#
# Помогаем Шарику найти косточку.
# Вам нужно написать код, который будет проверять правильно ли Шарик идет по лабиринту.
#
# То есть, вам нужно придумать реализацию системы управления и проверки решений. Управление: Вверх, вниз, влево,
# вправо через инпут или при нажатии клавиши, как хотите.
#
# УСЛОВИЯ :
#
# 1.	Если игрок выбрал оптимальное направление - выводим в консоль, что Шарик нашел правильный пути и даем
# следующий ход.
# 2.	Если Шарик пошел в сторону стены - пишем, что шарик ударился о стену, игра закончена.
# 3.	Если Шарик вернулся туда откуда пришел на предыдущем ходу - выводим шарик струсил и убежал, игра закончена.
# 4.	Если Шарик выбрал не оптимальный проход - выводим шарик заблудился, тоже заканчиваем игру.
# 5.	Если Шарик прошел через все оптимальные ходы - поздравляем с победой, завершаем игру.
#
# ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ :
#
# Реализовать систему сохранений в JSON. При проигрыше предлагаем сохраниться, прогресс шарика сохраняется на той
# позиции с которой он сделал неправильный ход. При запуске новой игры происходит проверка на наличие сохранения.
# Если есть сохранение - предлагаем игроку загрузить его. При отказе удаляем сохранение и начинаем новую игру с нуля.
import json


class Dog:

    def __init__(self, user_answer=None):
        self.user_answer = user_answer

    def move(self):
        print('\nШарик, в какую сторону пойдёшь?')
        self.user_answer = input('Введи одну из команд: "down", "up", "left", "right"\n')

        if self.user_answer == "down":
            return 'down'
        elif self.user_answer == 'up':
            return 'up'
        elif self.user_answer == 'left':
            return 'left'
        elif self.user_answer == 'right':
            return 'right'
        else:
            return self.move()


class Labyrinth:

    def __init__(self, move_step):
        self.move_step = move_step
        with open("labyrinth.json", "r") as read_file:
            labyrinth_from_json = json.load(read_file)
        self.labyrinth = labyrinth_from_json['labyrinth']

    def start(self):
        if self.move_step == 0:
            print('----------')
            print('Start game')
            print('----------')

    def next(self):
        self.move_step += 1
        if self.is_win():
            return self.win()
        else:
            print("---------")
            print("Next step")
            print("---------")

    @staticmethod
    def game_over():
        print("---------")
        print("Game over")
        print("---------")

    @staticmethod
    def win():
        print("---------")
        print("You win!")
        print("---------")

    def is_right_side(self, side):
        if self._is_wall(side) | self._is_prev(side) | self._is_wrong(side):
            return False
        else:
            return True

    def move_to_side(self, side):
        if self._is_next(side):
            return self.next()
        elif self._is_wall(side) | self._is_prev(side) | self._is_wrong(side):
            return self.game_over()

    def _is_next(self, side):
        if self.labyrinth[self.move_step][side] == 'next':
            print("Шарик на правильном пути")
            return True
        else:
            return False

    def _is_wall(self, side):
        if self.labyrinth[self.move_step][side] == 'wall':
            print("Шарик ударился о стену, игра закончена")
            return True
        else:
            return False

    def _is_prev(self, side):
        if self.labyrinth[self.move_step][side] == 'prev':
            print("Шарик струсил и убежал, игра закончена")
            return True
        else:
            return False

    def _is_wrong(self, side):
        if self.labyrinth[self.move_step][side] == 'wrong':
            print("Шарик заблудился, игра закончена")
            return True
        else:
            return False

    def is_win(self):
        if self.move_step == len(labyrinth.labyrinth):
            return True
        else:
            return False


class Save:

    def __init__(self):
        self.saved_state = None

    def get_save(self):
        try:
            with open("save.json", "r") as read_file:
                self.saved_state = json.load(read_file)
        except json.decoder.JSONDecodeError:
            self.saved_state = None
        return self.saved_state

    @staticmethod
    def set_save(saved_state):
        with open("save.json", "w") as write_file:
            return json.dump(saved_state, write_file)


if __name__ == '__main__':
    sharick = Dog()
    labyrinth = Labyrinth(move_step=0)
    start_game = True
    save = Save()

    if save.get_save() is not None:
        while True:
            user_ans = input('Хотите загрузить предыдущую игру? Y/N\n')
            if user_ans == 'Y':
                labyrinth.move_step = save.get_save()
                break
            elif user_ans == 'N':
                labyrinth.move_step = 0
                break

    while start_game:

        labyrinth.start()

        print(f"Num of step: {labyrinth.move_step + 1}")
        chosen_side = sharick.move()

        if not labyrinth.is_right_side(chosen_side):
            break

        labyrinth.move_to_side(chosen_side)

        if labyrinth.is_win():
            break

    while True:
        user_ans = input('Хотите сохранить прогресс? Y/N\n')
        if user_ans == 'Y':
            save.set_save(labyrinth.move_step)
            break
        elif user_ans == 'N':
            save.set_save(None)
            break

    # combination for win: 1: right, 2: down, 3: left, 4: down, 5: right, 6: right, 7: right, 8: right, 9: down,
    # 10: down, 11: right, 12: right, 13: right, 14: right, 15: down, 16: left, 17: down, 18: down, 19: left,
    # 20: down, 21: right, 22: down, 23: right, 24: right
