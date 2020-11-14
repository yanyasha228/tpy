import options
import graphs


def print_2d_matrix(matrix):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in matrix]))


if __name__ == '__main__':
    options = options.OptionsService.get_options("options.txt")
    matrix_graph = graphs.GraphUtils.build_cell_graph_by_options(options)
    cell_start = matrix_graph.index_edge_map.get((options.first_row_index, options.first_col_index))
    cell_end = matrix_graph.index_edge_map.get((options.second_row_index, options.second_col_index))
    graphs.GraphUtils.change_edges_values_like_lines_game(matrix_graph)
    fPath = None
    try:
        fPath = graphs.GraphUtils.find_path(matrix_graph, cell_start, cell_end)
        graphs.GraphUtils.change_graph_path_cell_edges_values(cell_start, cell_end, fPath)
        print(f"({cell_start.row_index + 1} , {cell_start.column_index + 1})"
              f" -> ({cell_end.row_index + 1} , {cell_end.column_index + 1}) | Path between cells | ")
    except graphs.NoGraphPassException:
        print(f"({cell_start.row_index + 1} , {cell_start.column_index + 1})"
              f" -> ({cell_end.row_index + 1} , {cell_end.column_index + 1}) | There is no path between cells")

    print_2d_matrix(graphs.GraphUtils.graph_to_matrix(matrix_graph, options.matrix_row_len, options.matrix_column_len))
