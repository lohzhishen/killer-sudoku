from Editor import editor


board = [["3", "", "", "9", "", "6", "1", "", "8"],
         ["", "", "", "", "5", "", "9", "4", "3"],
         ["", "9", "", "", "7", "3", "", "5", ""],
         ["", "1", "3", "", "", "", "", "2", ""],
         ["6", "", "", "", "", "", "", "", ""],
         ["", "", "4", "", "9", "", "", "8", ""],
         ["", "", "8", "2", "", "", "", "", ""],
         ["1", "", "2", "7", "", "4", "", "9", "5"],
         ["", "", "9", "", "", "5", "", "", "1"]]


sums = [[9, 9, 5, 11, 11, 14, 14, 14, 17],
        [15, 9, 16, 13, 13, 21, 20, 17, 17],
        [15, 16, 16, 21, 21, 21, 20, 20, 17],
        [17, 18, 8, 8, 21, 17, 17, 6, 6],
        [17, 18, 10, 10, 4, 17, 6, 6, 9],
        [17, 18, 18, 3, 16, 16, 11, 11, 6],
        [16, 13, 13, 3, 4, 26, 14, 18, 18],
        [16, 16, 13, 13, 4, 26, 14, 13, 18],
        [16, 16, 16, 13, 26, 26, 14, 13, 13]]


top_border = [[True, True, True, True, True, True, True, True, True],
              [True, False, True, True, True, True, True, True, False],
              [False, True, False, True, True, False, False, True, False],
              [True, True, True, True, False, True, True, True, True],
              [False, False, True, True, True, False, True, True, True],
              [False, False, True, True, True, True, True, True, True],
              [True, True, True, False, True, True, True, True, True],
              [False, True, False, True, False, False, False, True, False],
              [False, True, True, False, True, False, False, False, True]]


bottom_border = [[True, False, True, True, True, True, True, True, False],
                 [False, True, False, True, True, False, False, True, False],
                 [True, True, True, True, False, True, True, True, True],
                 [False, False, True, True, True, False, True, True, True],
                 [False, False, True, True, True, True, True, True, True],
                 [True, True, True, False, True, True, True, True, True],
                 [False, True, False, True, False, False, False, True, False],
                 [False, True, True, False, True, False, False, False, True],
                 [True, True, True, True, True, True, True, True, True]]


left_border = [[True, False, True, True, False, True, False, False, True],
               [True, True, True, True, False, True, True, True, False],
               [True, True, False, True, False, False, True, False, True],
               [True, True, True, False, True, True, False, True, False],
               [True, True, True, False, True, True, True, False, True],
               [True, True, False, True, True, False, True, False, True],
               [True, True, False, True, True, True, True, True, False],
               [True, False, True, True, True, True, True, True, True],
               [True, True, False, True, True, False, True, True, False]]


right_border = [[False, True, True, False, True, False, False, True, True],
                [True, True, True, False, True, True, True, False, True],
                [True, False, True, False, False, True, False, True, True],
                [True, True, False, True, True, False, True, False, True],
                [True, True, False, True, True, True, False, True, True],
                [True, False, True, True, False, True, False, True, True],
                [True, False, True, True, True, True, True, False, True],
                [False, True, True, True, True, True, True, True, True],
                [True, False, True, True, False, True, True, False, True]]


if __name__ == '__main__':
    app = editor.KillerSudokuEditor(board, sums, top_border, bottom_border, left_border, right_border)
    data = app.start()  
    