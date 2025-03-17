from dataclasses import dataclass
import matplotlib.pyplot as plt


# Создаем классы фигур
# У каждого класса есть свои атрибуты и метод для отображения информации о себе
@dataclass
class Point:
    x: float
    y: float

    def display(self):
        print(f"Точка: координаты ({self.x}, {self.y})")


@dataclass
class Line:
    start: Point  # используем экземпляры класса Point для создания отрезка
    end: Point

    def display(self):
        print(
            f"Отрезок: координаты начала ({self.start.x}, {self.start.y}), координаты окончания ({self.end.x}, {self.end.y})")


@dataclass
class Circle:
    center: Point
    radius: float

    def display(self):
        print(f"Круг: координаты центра ({self.center.x}, {self.center.y}), радиус {self.radius}")


@dataclass
class Square:
    top_left: Point
    side_length: float

    def display(self):
        print(
            f"Квадрат: координаты верхнего левого угла ({self.top_left.x}, {self.top_left.y}), длина стороны {self.side_length}")


# Функция для отрисовки фигур с помощью matplotlib
def plot_shape(shape, ax):
    if isinstance(shape, Point):
        ax.plot(shape.x, shape.y, 'ro')  # Точка (красный круг)
    elif isinstance(shape, Line):
        ax.plot([shape.start.x, shape.end.x], [shape.start.y, shape.end.y], 'b-')  # Линия (синяя линия)
    elif isinstance(shape, Circle):
        circle = plt.Circle((shape.center.x, shape.center.y), shape.radius, color='g', fill=False)  # Круг (зеленый круг)
        ax.add_patch(circle)
    elif isinstance(shape, Square):
        rect = plt.Rectangle((shape.top_left.x, shape.top_left.y), shape.side_length, shape.side_length, color='orange', fill=False)  # Квадрат (оранжевый квадрат)
        ax.add_patch(rect)


# Интерфейс командной строки - редактор
class Editor:
    def __init__(self):
        self.shapes = []  # Инициализация списка для хранения фигур

    # Функция создания фигуры
    def create_shape(self, shape_type, *args):
        try:
            if shape_type == "p":
                x, y = map(float, args)            # преобразование аргументов в числа и распаковка в переменные
                self.shapes.append(Point(x, y))    # добавление объекта Point в список shapes
                print(f"Точка создана ({args})")
                self.plot_all_shapes()             # выводим график с фигурами
            elif shape_type == "l":
                x1, y1, x2, y2 = map(float, args)
                self.shapes.append(Line(Point(x1, y1), Point(x2, y2)))
                print(f"Отрезок создан ({args})")
                self.plot_all_shapes()
            elif shape_type == "cir":
                x, y, radius = map(float, args)
                if radius < 0:
                    print("Ошибка: радиус должен быть неотрицательным числом.")
                    return
                self.shapes.append(Circle(Point(x, y), radius))
                print(f"Круг создан ({args})")
                self.plot_all_shapes()
            elif shape_type == "sq":
                x, y, side_length = map(float, args)
                if side_length < 0:
                    print("Ошибка: сторона квадрата должна быть неотрицательным числом.")
                    return
                self.shapes.append(Square(Point(x, y), side_length))
                print(f"Квадрат создан ({args})")
                self.plot_all_shapes()
            else:
                print("Неизвестный тип фигуры")

        except ValueError:
            print("Ошибка: не все аргументы являются числами или введено больше аргументов, чем требуется.")

    # Функция удаления фигуры
    def delete_shape(self, index):
        if 0 <= index < len(self.shapes):
            print("Удалена фигура:", self.shapes[index])
            self.shapes.pop(index)
        else:
            print("Неверный индекс")
            
    # Функция вывод списка фигур и графики
    def list_shapes(self):
        for i, shape in enumerate(self.shapes):
            print(f"{i}: ", end="")
            shape.display()

    # Функция создания графики с фигурами
    def plot_all_shapes(self):
        if not self.shapes:
            print("Нет фигур для отображения.")
            return

        fig, ax = plt.subplots()
        ax.set_title("Все фигуры")
        ax.set_aspect('equal')

        for shape in self.shapes:
            plot_shape(shape, ax)

        # Установка пределов графика для корректного отображения фигур
        x_min = min([shape.x if isinstance(shape, Point) else min(shape.start.x, shape.end.x)
                             if isinstance(shape, Line) else shape.center.x - shape.radius
                             if isinstance(shape, Circle) else shape.top_left.x for shape in self.shapes])

        x_max = max([shape.x if isinstance(shape, Point) else max(shape.start.x, shape.end.x)
                             if isinstance(shape, Line) else shape.center.x + shape.radius
                             if isinstance(shape, Circle) else shape.top_left.x + shape.side_length for shape in self.shapes])

        y_min = min([shape.y if isinstance(shape, Point) else min(shape.start.y, shape.end.y)
                             if isinstance(shape, Line) else shape.center.y - shape.radius
                             if isinstance(shape, Circle) else shape.top_left.y - shape.side_length for shape in self.shapes])

        y_max = max([shape.y if isinstance(shape, Point) else max(shape.start.y, shape.end.y)
                             if isinstance(shape, Line) else shape.center.y + shape.radius
                             if isinstance(shape, Circle) else shape.top_left.y for shape in self.shapes])

        ax.set_xlim(x_min - 1, x_max + 1)
        ax.set_ylim(y_min - 1, y_max + 1)

        plt.grid(False)
        plt.show()

    # Функция ввода/приема команд
    def run(self):
        while True:
            command = input(
                "Введите команду (help - помощь): ").strip().split()    # обрезаем пробелы по краям и разбиваем строку на слова
            if not command:
                continue

            if command[0] == "add":
                if len(command) < 2:                         # проверка на заполнение аргументов
                    print("Недостаточно аргументов")
                    continue
                self.create_shape(command[1], *command[2:])  # создание фигуры

            elif command[0] == "del":
                if len(self.shapes) == 0:
                    print("Не добавлено ни одной фигуры.")
                    continue
                if len(command) < 2:
                    print("Недостаточно аргументов")
                    continue
                self.delete_shape(int(command[1]))

            elif command[0] == "list":
                if len(self.shapes) == 0:
                    print("Не добавлено ни одной фигуры.")
                else:
                    self.list_shapes()                       # вывод списка фигур
                    self.plot_all_shapes()                   # вывод графики

            elif command[0] == "help":
                print("add <p|l|cir|sq> <x> <y> - создание фигуры")
                print("---")
                print("Cоздание точки: add p <x> <y>  (x, y - координаты точки)")
                print("Cоздание отрезка: add l <x1> <y1> <x2> <y2> (x1, y1 и x2, y2 - координаты начала и конца отрезка)")
                print("Cоздание круга: add cir <x> <y> <radius> (x, y - координаты центра, radius - радиус круга")
                print("Cоздание квадрата: add sq <x> <y> <side_length> (x, y - координаты верхнего левого угла, side_length - длина стороны квадрата")
                print("===")
                print("del <номер> - удаление фигуры")
                print("list - список фигур")
                print("exit - выход из программы")
                print("======")

            elif command[0] == "exit":
                break
            else:
                print("Неизвестная команда")


if __name__ == "__main__":
    editor = Editor()
    editor.run()
