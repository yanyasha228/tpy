import collections
import options


class Edge:

    def __init__(self, is_passable: bool):
        self.__is_passable = is_passable

    @property
    def is_passable(self):
        return self.__is_passable


class CellEdge(Edge):

    def __init__(self, row_index: int, column_index: int, value, is_passable: bool):
        super().__init__(is_passable)
        self.__row_index = row_index
        self.__column_index = column_index
        self.__value = value

    @property
    def row_index(self):
        return self.__row_index

    @property
    def column_index(self):
        return self.__column_index

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Queue:

    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()


class Graph:

    def __init__(self):
        self.__edges = {}

    @property
    def edges(self):
        return self.__edges

    @edges.setter
    def edges(self, edges: {Edge: [Edge]}):
        self.__edges = edges

    def neighbors(self, edge: Edge):
        return self.__edges[edge]


class CellGraph(Graph):

    def __init__(self):
        super().__init__()
        self.__index_edge_map = {}

    @property
    def index_edge_map(self):
        return self.__index_edge_map

    @index_edge_map.setter
    def index_edge_map(self, index_edge_map: {(int, int): Edge}):
        self.__index_edge_map = index_edge_map


class GraphUtils:

    @staticmethod
    def change_graph_path_cell_edges_values(edge_start: CellEdge, edge_end: CellEdge, path: [CellEdge]):
        for idx, edge in enumerate(path):

            if idx == len(path) - 1:
                edge.value = 'F'
                break

            if idx == 0:
                continue

            diff_row_indexes = edge.row_index - path[idx - 1].row_index
            diff_column_indexes = edge.column_index - path[idx - 1].column_index
            if diff_row_indexes > 0:
                edge.value = 'D'
            if diff_row_indexes < 0:
                edge.value = 'U'
            if diff_column_indexes > 0:
                edge.value = 'R'
            if diff_column_indexes < 0:
                edge.value = 'L'

    @staticmethod
    def change_edges_values_like_lines_game(graph: CellGraph):
        i_map = graph.index_edge_map
        for ed in i_map:
            edge_to_update = i_map.get(ed)
            if edge_to_update.value == 0:
                edge_to_update.value = '+'
            else:
                edge_to_update.value = 'O'

        return graph

    @staticmethod
    def build_cell_graph_by_options(opt: options.Options):
        graph = CellGraph()
        matx = opt.matrix
        edges_map = {}
        ind_edg_map = {}
        for i in range(opt.matrix_row_len):
            for j in range(opt.matrix_column_len):
                ind_edg_map[(i, j)] = CellEdge(i, j, matx[i][j], matx[i][j] == 0)

        for ind in ind_edg_map:
            row_index = ind[0]
            column_index = ind[1]

            n_edges = [ind_edg_map.get((row_index - 1, column_index)), ind_edg_map.get((row_index + 1, column_index)),
                       ind_edg_map.get((row_index, column_index - 1)), ind_edg_map.get((row_index, column_index + 1))]

            edges_map[ind_edg_map[ind]] = list(filter(lambda a: a is not None, n_edges))

        graph.index_edge_map = ind_edg_map
        graph.edges = edges_map

        return graph

    @staticmethod
    def graph_to_matrix(graph: CellGraph, matrix_row_num: int, matrix_column_num: int):
        matrix_to_ret = [[0] * matrix_row_num for i in range(matrix_column_num)]
        r_map = graph.index_edge_map
        for mat in r_map:
            matrix_to_ret[mat[0]][mat[1]] = r_map[mat].value

        return matrix_to_ret

    @staticmethod
    def find_path(graph: Graph, start: Edge, end: Edge):
        frontier = Queue()
        frontier.put(start)
        came_from = {start: None}

        while not frontier.empty():
            current = frontier.get()

            if current == end:
                break

            for next_ed in graph.neighbors(current):
                if next_ed not in came_from and next_ed.is_passable:
                    frontier.put(next_ed)
                    came_from[next_ed] = current

        if came_from.get(end) is None:
            raise NoGraphPassException()

        current = end
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)
        # path.append(start)
        path.reverse()
        return path


class NoGraphPassException(Exception):
    def __init__(self,
                 message="No pass between cells"):
        super().__init__(message)
        self.__message = message


class NoCellGraphPassException(NoGraphPassException):
    def __init__(self,
                 cell_edge_start: CellEdge,
                 cell_edge_end: CellEdge,
                 message="No pass between cells"):
        super().__init__(message)
        self.__start_edge = cell_edge_start
        self.__end_edge = cell_edge_end
        self.__message = message

    def __str__(self):
        return f"({self.__start_edge.row_index + 1} , {self.__start_edge.column_index + 1}) " \
               f"-> ({self.__end_edge.row_index + 1} , {self.__end_edge.column_index + 1}) | {self.__message}"
