import sys
import random

def check_number_of_arguments():
    if len(sys.argv) != 2:
        return False

def print_help():
    print("""
Формат запуска программы:
имя программы:
    05_chess_board_generator.py
параметр число от 1 до 100:
    [1-100]
Пример вызова:
    05_chess_board_generator.py 10
Будет сгенерирован файл generated_matrix.csv
В который можно дать на вход программе 05_chess_board.py
В нём будет сгенерирована информация о матрице (шахматной доске),
со случаынйми числами в ячейках
""")
    
def generate_matrix(matrix_size):
    random.seed()
    matrix = [[0] * (matrix_size+1) for _ in range(matrix_size+1)]
    matrix[0][0] = matrix_size
    for i in range(1, matrix_size + 1):
        for j in range(1, matrix_size + 1):
            matrix[i][j] = random.randint(1,9)
            
    return matrix

def output_matrix(matrix):
    file = open("generated_matrix.csv", "w")
    for i in range(matrix[0][0] + 1):
        for j in range(matrix[0][0] + 1):
            if i == 0 and j == 0:
                print(matrix[0][0], file=file, end="")
            elif i == 0 or j == 0:
                print(";", file=file, end="")
                if j == matrix[0][0]:
                    print(file=file)
            elif j != matrix[0][0]:
                print(str(matrix[i][j]) + ";", file=file, end="")
            else:
                print(matrix[i][j], file=file)

if __name__ == "__main__":
    if(check_number_of_arguments() == False):
        print_help()
        exit()
    try:
        matrix_size = int(sys.argv[1])
    except:
        print_help()
        exit()
        
    print("Размер генерируемой матрицы:", matrix_size)
    if matrix_size < 1 or matrix_size > 100:
        print_help()
        exit()
        
    matrix = generate_matrix(matrix_size)
    try:
        output_matrix(matrix)
    except:
        print("Не удаётся открыть файл: generated_matrix.csv на запись")
        print("Проверьте, не открыт ли этот файл какой-либо программой")
        exit()