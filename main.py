from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.patches import Polygon


# Функция вывода в консоль или в файл
def output_(file, output):
    if file:
        file.write(output + '\n')   # Записываем в файл
    else:
        print(output)               # Выводим в консоль


# Создаем классы фигур
# У каждого класса есть свои атрибуты и метод для отображения информации о себе
@dataclass
class Point:
    x: float
    y: float

    def display(self, file=None):       # По-умолчанию выводим в консоль (file=None)
        output = f"Точка: координаты ({self.x}, {self.y})"
        output_(file, output)


@dataclass
class Line:
    start: Point  # используем экземпляры класса Point для создания отрезка
    end: Point

    def display(self, file=None):
        output = f"Отрезок: координаты начала ({self.start.x}, {self.start.y}), координаты окончания ({self.end.x}, {self.end.y})"
        output_(file, output)

@dataclass
class Circle:
    center: Point
    radius: float

    def display(self, file=None):
        output = f"Круг: координаты центра ({self.center.x}, {self.center.y}), радиус {self.radius}"
        output_(file, output)

@dataclass
class Square:
    top_left: Point
    side_length: float

    def display(self, file=None):
        output = f"Квадрат: координаты верхнего левого угла ({self.top_left.x}, {self.top_left.y}), длина стороны {self.side_length}"
        output_(file, output)

@dataclass
class Rectangle:
    top_left: Point
    a_side_length: float
    b_side_length: float

    def display(self, file=None):
        output = (f"Прямоугольник: координаты верхнего левого угла ({self.top_left.x}, {self.top_left.y}), "
                  f"длина первой стороны {self.a_side_length}, длина второй стороны {self.b_side_length}")
        output_(file, output)

@dataclass
class Oval:
    center: Point
    width: float
    height: float

    def display(self, file=None):
        output = f"Овал: координаты центра ({self.center.x}, {self.center.y}), ширина {self.width}, высота {self.height}"
        output_(file, output)

@dataclass
class Triangle:
    top1: Point
    top2: Point
    top3: Point

    def display(self, file=None):
        output = (f"Треугольник: координаты 1-ой вершины ({self.top1.x}, {self.top1.y}), "
            f"координаты 2-ой вершины ({self.top2.x}, {self.top2.y}), "
            f"координаты 3-ей вершины ({self.top3.x}, {self.top3.y})")
        output_(file, output)


# Функция для отрисовки фигур с помощью matplotlib
def plot_shape(shape, ax):
    if isinstance(shape, Point):
        ax.plot(shape.x, shape.y, 'ro')  # Точка (красный круг)
    elif isinstance(shape, Line):
        ax.plot([shape.start.x, shape.end.x], [shape.start.y, shape.end.y], 'blue')  # Линия (синяя линия)
    elif isinstance(shape, Circle):
        circle = plt.Circle((shape.center.x, shape.center.y), shape.radius, color='green', fill=False)  # Круг (зеленый круг)
        ax.add_patch(circle)
    elif isinstance(shape, Square):
        rect = plt.Rectangle((shape.top_left.x, shape.top_left.y - shape.side_length), shape.side_length, shape.side_length, color='orange', fill=False)  # Квадрат (оранжевый квадрат)
        ax.add_patch(rect)
    elif isinstance(shape, Rectangle):
        rect2 = plt.Rectangle((shape.top_left.x, shape.top_left.y - shape.b_side_length), shape.a_side_length, shape.b_side_length, color='violet', fill=False)  # Прямоугольник (фиолетовый)
        ax.add_patch(rect2)
    elif isinstance(shape, Oval):
        oval = Ellipse(xy=(shape.center.x, shape.center.y),  # Центр овала
                       width=shape.width,                    # Ширина
                       height=shape.height,                  # Высота
                       color='black',                        # Цвет
                       fill=False)                           # Без заливки  Овал (черный)
        ax.add_patch(oval)
    elif isinstance(shape, Triangle):
        triangle = Polygon(
            [(shape.top1.x, shape.top1.y), (shape.top2.x, shape.top2.y), (shape.top3.x, shape.top3.y)],  # Список координат вершин
            color='red',  # красный
            fill=False)
        ax.add_patch(triangle)


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
            elif shape_type == "rec":
                x, y, a_side_length, b_side_length = map(float, args)
                if a_side_length < 0 or b_side_length < 0:
                    print("Ошибка: стороны прямоугольника должны быть неотрицательными числами.")
                    return
                self.shapes.append(Rectangle(Point(x, y), a_side_length, b_side_length))
                print(f"Прямоугольник создан ({args})")
                self.plot_all_shapes()
            elif shape_type == "oval":
                x, y, width, height = map(float, args)
                if width < 0 or height < 0:
                    print("Ошибка: ширина и высота овала должны быть неотрицательными числами.")
                    return
                self.shapes.append(Oval(Point(x, y), width, height))
                print(f"Овал создан ({args})")
                self.plot_all_shapes()
            elif shape_type == "tr":
                x1, y1, x2, y2, x3, y3 = map(float, args)
                self.shapes.append(Triangle(Point(x1, y1), Point(x2, y2), Point(x3, y3)))
                print(f"Треугольник создан ({args})")
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
            # Вычисляем минимальное и максимальное значение координат X и Y

        x_min = min([
            shape.x if isinstance(shape, Point)                               # Для точки
            else min(shape.start.x, shape.end.x) if isinstance(shape, Line)   # Для отрезка
            else min(shape.top1.x, shape.top2.x, shape.top3.x) if isinstance(shape, Triangle)  # Для треугольника
            else shape.center.x - shape.radius if isinstance(shape, Circle)   # Для круга
            else shape.center.x - max(shape.width, shape.height) if isinstance(shape, Oval)  # Для овала
            else shape.top_left.x                                             # Для квадрата (левая граница)
            for shape in self.shapes
        ])

        x_max = max([
            shape.x if isinstance(shape, Point)                              # Для точки
            else max(shape.start.x, shape.end.x) if isinstance(shape, Line)  # Для линии
            else max(shape.top1.x, shape.top2.x, shape.top3.x) if isinstance(shape, Triangle)  # Для треугольника
            else shape.center.x + shape.radius if isinstance(shape, Circle)  # Для круга
            else shape.center.x + max(shape.width, shape.height) if isinstance(shape, Oval)  # Для овала
            else shape.top_left.x + max(shape.a_side_length, shape.b_side_length) if isinstance(shape, Rectangle)  # Для прямоугольника (правая граница)
            else shape.top_left.x + shape.side_length                        # Для квадрата  (правая граница)
            for shape in self.shapes
        ])

        y_min = min([
            shape.y if isinstance(shape, Point)                              # Для точки
            else min(shape.start.y, shape.end.y) if isinstance(shape, Line)  # Для линии
            else min(shape.top1.y, shape.top2.y, shape.top3.y) if isinstance(shape, Triangle)  # Для треугольника
            else shape.center.y - shape.radius if isinstance(shape, Circle)  # Для круга
            else shape.center.y - max(shape.width, shape.height) if isinstance(shape, Oval)  # Для овала
            else shape.top_left.y - max(shape.a_side_length, shape.b_side_length) if isinstance(shape, Rectangle) # Для прямоугольника (нижняя граница)
            else shape.top_left.y - shape.side_length                        # Для квадрата (нижняя граница)
            for shape in self.shapes
        ])

        y_max = max([
            shape.y if isinstance(shape, Point)                              # Для точки
            else max(shape.start.y, shape.end.y) if isinstance(shape, Line)  # Для линии
            else max(shape.top1.y, shape.top2.y, shape.top3.y) if isinstance(shape, Triangle)  # Для треугольника
            else shape.center.y + shape.radius if isinstance(shape, Circle)  # Для круга
            else shape.center.y + max(shape.width, shape.height) if isinstance(shape, Oval)  # Для овала
            else shape.top_left.y                                            # Для квадрата и прямоугольника (верхняя граница)
            for shape in self.shapes
        ])

            # к пределам добавляем отступ -1 и +1, чтобы фигуры не прилипали к краям графика
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

            elif command[0] == "save":
                with open("shapes_list.txt", 'w', encoding='utf-8') as file:  # Открываем файл для записи
                    for i, shape in enumerate(self.shapes):
                        file.write(f"{i}: ")  # Записываем индекс фигуры
                        shape.display(file)  # Записываем информацию о фигуре
                print("Файл shapes_list.txt сохранен в текущей директории.")

            elif command[0] == "help":
                print("****************************************************************************************")
                print("Команда создания фигуры:")
                print("   add <p|l|cir|sq|rec|oval|tr> <x> <y> ... \n")
                print("   Cоздание точки: add p <x> <y>  (x, y - координаты точки)")
                print("   Cоздание отрезка: add l <x1> <y1> <x2> <y2> \n"
                      "      (x1, y1 и x2, y2 - координаты начала и конца отрезка)")
                print("   Cоздание круга: add cir <x> <y> <radius> \n"
                      "      (x, y - координаты центра, radius - радиус круга")
                print("   Cоздание квадрата: add sq <x> <y> <side_length> \n"
                      "      (x, y - координаты верхнего левого угла, side_length - длина стороны квадрата")
                print("   Cоздание прямоугольника: add rec <x> <y> <a_side_length> <b_side_length> \n"
                      "      (x, y - координаты верхнего левого угла, a_side_length - длина 1-ой стороны, \n"
                      "       b_side_length - длина второй стороны прямоугольника)")
                print("   Cоздание овала: add oval <x> <y> <a_side_length> <b_side_length> \n"
                      "      (x, y - координаты центра овала, width - ширина овала, height - высота овала)")
                print("   Cоздание треугольника: add tr <x1> <y1> <x2> <y2> <x3> <y3> \n"
                      "      (x1, y1 и x2, y2 и x3, y3 - координаты вершин треугольника)\n")
                print("Другие команды:")
                print("   del <номер> - удаление фигуры")
                print("   list - вывести список фигур")
                print("   save - сохранить список фигур в файл")
                print("   exit - выход из программы")
                print("****************************************************************************************\n")

            elif command[0] == "exit":
                break
            else:
                print("Неизвестная команда")


if __name__ == "__main__":
    editor = Editor()
    editor.run()