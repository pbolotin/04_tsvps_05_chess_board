import sys

def print_help():
    print("""
Использование программы в командной строке:

[1]              [2]
05_chess_board.py [filename]

[1] - вызов самой программы
[2] - аргумент программы - имя файла с входными данными [filename]

Пример вызова:
05_chess_board.py matrix.csv

Формат [filename] формат соответствует стандартному csv-файлу.

В [filename] должны быть следующие данные

В левом верхнем углу указывается количество вершин в графе (напримере 5).

Разделитель данных - ; - точка с запятой

Вывод программы:
Максимальная сумма собираемая по пути из левого верхнего угла матрицы в
правый нижний, допустимы единичные шаги вниз и вправо
""")

def check_and_prepare_data(data):
    try:
        data[0][0] = int(data[0][0])
    except ValueError:
        print("""ОШИБКА!

Значение n в матрице, не получается конвертировать в число
""")
        exit()
    
    if data[0][0] < 1:
        print("""ОШИБКА!

Проверьте значение n - оно не должно быть меньше 1.""")
        exit()

    if len(data) != data[0][0] + 1:
        print("""ОШИБКА!

Проверьте количество строк входных данных!
Оно должно быть равно """, data[0][0] + 1, " для вашего n.")
        exit()
        
    for i in range(data[0][0] + 1):
        if len(data[i]) != data[0][0] + 1:
            print("""ОШИБКА!

Проверьте строки данных в них должно быть """, data[0][0]+1, "ячеек\n")
            exit()
            
    for i in range(1, data[0][0] + 1):
        for j in range(1, data[0][0] + 1):
            try:
                data[i][j] = int(data[i][j])
            except ValueError:
                print("""ОШИБКА!

В ячейке матрицы данные которые не получается конвертировать в число!\n\nИндексы:""", i, j, "\nДанные:", data[i][j], "\n")
                exit()

def check_number_of_arguments():
    if 2 != len(sys.argv): return False

def load_matrix_from_file():
    data_file = open(sys.argv[1])
    data = [] 
    for i in data_file:
        data.append(i.strip().split(";"))
        
    data_file.close()
    check_and_prepare_data(data)
    return data
    
if __name__ == "__main__":
    if(check_number_of_arguments() == False):
        print_help()
        exit()
    data = load_matrix_from_file()
    print(data)