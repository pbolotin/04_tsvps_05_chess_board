import sys

class Vertex:
    #name
    #index
    def __init__(self, name, index):
        self.name = name
        self.index = index

class Edge:
    #vertex1
    #vertex2
    #weight
    def __init__(self, vertex1, vertex2, weight):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.weight = weight

class Graph:
    #set_of_vertex
    #set_of_edges
    
    def __init__(self):
        self.set_of_vertex = set()
        self.set_of_edges = set()

    def add_vertex(self, vertex):
        self.set_of_vertex.add(vertex)

    def add_edge(self, edge):
        if edge in self.set_of_edges:
            return False
        else:
            self.set_of_vertex.add(edge.vertex1)
            self.set_of_vertex.add(edge.vertex2)
            self.set_of_edges.add(edge)
        return True

    def union_with_graph(self, another_graph):
        self.set_of_vertex.union(another_graph.set_of_vertex)
        self.set_of_edges.union(another_graph.set_of_edges)
        
    def check_edge_for_cycle(self, edge):
        return edge.vertex1 in self.set_of_vertex and edge.vertex2 in self.set_of_vertex

    def has_this_vertex(self, vertex):
        return vertex in self.set_of_vertex
        
class Forest:
    #set_of_graphs
    
    def __init__(self):
        self.set_of_graphs = set()
        
    def add_graph(self, graph):
        self.set_of_graphs.add(graph)
        
    def check_edge_for_cycle(self, edge):
        for graph in self.set_of_graphs:
            if graph.check_edge_for_cycle(edge) == True:
                return True
        return False

    def try_update_by_edge_if_not_cycle(self, edge):
        g1 = None
        g2 = None
        for graph in self.set_of_graphs:
            if graph.has_this_vertex(edge.vertex1) == True:
                g1 = graph
            if graph.has_this_vertex(edge.vertex2) == True:
                g2 = graph
                if(g1 == g2):
                    return False
        
        if g1 != None and g2 != None:
            self.set_of_graphs.discard(g2)
            g1.union_with_graph(g2)
            g1.add_edge(edge)
        else:
            return False
        
        return True
        
    def how_many_components(self):
        return len(self.set_of_graphs)
        
        
def print_help():
    print("""Для неориентированного взвешенного графа
эта программа может найти минимальное остовное дерево.

Использование программы в командной строке:

[1]              [2]
min_span_tree.py [filename]

[1] - вызов самой программы
[2] - аргумент программы - имя файла с входными данными [filename]

Пример вызова:
min_span_tree.py adjacency_matrix.csv

Формат [filename] формат соответствует стандартному csv-файлу.

В [filename] должны быть следующие данные
(пример для графа из 5 вершин, и 7 рёбер), :

5;A;B;C;D;E
A;0;2;0;8;4
B;2;0;3;0;0
C;0;3;0;5;1
D;8;0;5;0;7
E;4;0;1;7;0

В левом верхнем углу указывается количество вершин в графе (в примере 5).

Разделитель данных - ; - точка с запятой

Далее, по первой горизонтали и вертикали, указываются имена вершин.
Остальные места заполнены матрицей смежности для взвешенного
неориентированного графа.

Вывод программы:
Список рёбер минимального остовного дерева графа. Его вес.
""")

def check_and_prepare_data(data):
    try:
        data[0][0] = int(data[0][0])
    except ValueError:
        print("""ОШИБКА!

Значение n в матрице, не получается конвертировать в число

Ниже показан пример правильной матрицы где n в левом верхнем углу равно 5.

5;A;B;C;D;E
A;0;2;0;8;4
B;2;0;3;0;0
C;0;3;0;5;1
D;8;0;5;0;7
E;4;0;1;7;0

Проверьте это место в ваших данных!""")
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
        if data[i][0] != data[0][i]:
            print("""ОШИБКА!

Названия вершин по вертикали и горизонтали должны быть последовательны!\n\n""", " Название: ", data[i][0], " не соответствует названию: ", data[0][i], "\n")
            exit()
            
    for i in range(1, data[0][0] + 1):
        for j in range(1, data[0][0] + 1):
            try:
                data[i][j] = int(data[i][j])
                if i == j and data[i][j] != 0:
                    print("""ПРЕДУПРЕЖДЕНИЕ!

В ячейке с индексами:""", i, i, 
"""ненулевое значение!
Это соответствует петле в графе, для минимального остова эти данные игнорируются!\n\n""")
            except ValueError:
                print("""ОШИБКА!

В ячейке матрицы данные которые не получается конвертировать в число!\n\nИндексы:""", i, j, "\nДанные:", data[i][j], "\n")
                exit()
                
    for i in range(1, data[0][0] + 1):
        for j in range(1, data[0][0] + 1):
            if data[i][j] != data[j][i]:
                print("""ОШИБКА!

Матрица смежности неориентированного взвешенного графа должна быть
симметричной относительно диагонали!
""")
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

def min_span_tree_Kruskal(data):
    size = data[0][0]
    
    #Создаём лес из графов инициализированных вершинами
    #Создаём список вершин
    f = Forest()
    list_of_vertex = []
    for i in range(1, size+1):
        v = Vertex(data[0][i], i)
        list_of_vertex.append(v)
        g = Graph()
        g.add_vertex(v)
        f.add_graph(g)
    #Создаём список рёбер с весом больше 0
    list_of_edges = []
    for i in range(1, size):
        for j in range(i+1, size+1):
            if data[i][j] != 0:
                list_of_edges.append(Edge(list_of_vertex[i-1], list_of_vertex[j-1], data[i][j]))
    
    #Сортируем
    list_of_edges.sort(key = lambda x: x.weight)
    #Создаём список рёбер остова
    mst_edges = []
    #Проходим по списку
    for edge in list_of_edges:
        if f.try_update_by_edge_if_not_cycle(edge) != False:
            mst_edges.append(edge)

    #Проверка на завершённость процесса (все ли компоненты объединены)
    if(f.how_many_components() > 1):
        return None

    return mst_edges

def give_answer(mst_edges):
    print("Минимальное остовное дерево графа представлено рёбрами (возможно 0 рёбер, если граф состоит из одной вершины):\n")
    sum_weight = 0
    for edge in mst_edges:
        print(("Ребро:", (edge.vertex1.name + str(edge.vertex1.index) + "-" + edge.vertex2.name + str(edge.vertex2.index))), ("Вес ребра:", edge.weight))
        sum_weight += edge.weight
        
    print("\nВес минимального остовного дерева:", sum_weight)
    
if __name__ == "__main__":
    if(check_number_of_arguments() == False):
        print_help()
        exit()
    data = load_matrix_from_file()
    mst_edges = min_span_tree_Kruskal(data)
    if(mst_edges == None):
        print("Данные матрицы графа не позволяют построить минимальное остовное дерево.\nВозможно в графе более одного компонента связности")
    else:
        give_answer(mst_edges)