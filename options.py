class OptionsService:

    @staticmethod
    def get_options(file_path: str):
        str_num_matrix_row_len = 0
        str_num_matrix_column_len = 1
        str_num_start_indexes = 2
        str_num_end_indexes = 3
        str_num_last_param_string = 4

        with open(file_path, "r") as opt_file:
            lines = opt_file.readlines()
            index_start_str = lines[str_num_start_indexes].replace("(", "").replace(")", "").replace("\n", "").split(
                ",")
            index_end_str = lines[str_num_end_indexes].replace("(", "").replace(")", "").replace("\n", "").split(",")
            matrix_row_len = lines[str_num_matrix_row_len].strip(" \n")
            matrix_column_len = lines[str_num_matrix_column_len].strip(" \n")
            matrix = []

            for num in range(str_num_last_param_string + 1, len(lines)):
                ln_to_add = list(filter(lambda a: a.isnumeric(), lines[num].replace("\n", "").split(" ")))
                if len(ln_to_add) > 0:
                    matrix.append(list(map(lambda a: eval(a), ln_to_add)))

        return Options(matrix,
                       eval(matrix_row_len),
                       eval(matrix_column_len),
                       eval(index_start_str[0]) - 1,
                       eval(index_start_str[1]) - 1,
                       eval(index_end_str[0]) - 1,
                       eval(index_end_str[1]) - 1)


class Options:

    def __init__(self,
                 matrix,
                 matrix_row_len: int,
                 matrix_column_len: int,
                 first_row_index: int,
                 first_col_index: int,
                 second_row_index: int,
                 second_col_index: int):
        self.__matrix = matrix
        self.__matrix_row_len = matrix_row_len
        self.__matrix_column_len = matrix_column_len
        self.__first_row_index = first_row_index
        self.__first_col_index = first_col_index
        self.__second_row_index = second_row_index
        self.__second_col_index = second_col_index

    @property
    def matrix_row_len(self):
        return self.__matrix_row_len

    @property
    def matrix_column_len(self):
        return self.__matrix_column_len

    @property
    def matrix(self):
        return self.__matrix

    @property
    def first_row_index(self):
        return self.__first_row_index

    @property
    def first_col_index(self):
        return self.__first_col_index

    @property
    def second_row_index(self):
        return self.__second_row_index

    @property
    def second_col_index(self):
        return self.__second_col_index
