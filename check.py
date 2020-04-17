import os
from solver import print_matrix
from utils import accepted
from solver import check

def valid_sudoku(sudoku):
    rows, cols = len(sudoku),len(sudoku[0])
    div_y = cols//3
    div_x = rows//div_y
    for i in range(rows):
        for j in range(cols):
            if sudoku[i][j] == 0:
                continue
            else:
                temp = sudoku[i][j]
                sudoku[i][j] = 0
                if not check(sudoku,i,j,temp,div_x,div_y):
                    #print(i,j,sudoku[i][j],(not check(sudoku,i,j,temp,div_x,div_y)))
                    sudoku[i][j] = temp    
                    return False
                sudoku[i][j] = temp
    return True

def read_matrix(file):
    f = open(file,'r')
    sudoku = []
    for line in f:
        line = line[1:len(line)-2]
        fields = line.split(', ')
        row = []
        row = [int(x) for x in fields]
        sudoku.append(row)
    f.close()
    return sudoku


def check_sudoku(sudoku):
    is_valid = valid_sudoku(sudoku)
    
    if is_valid:
        print("Is the following detect matrix correct ?\n(Yes/No)")
        print_matrix(sudoku)

    if (not is_valid) or (not accepted()):

        if not is_valid:
            print("Sudoku detected seems invalid.")
        print("Please edit the matrix in the opened .txt file and then save")

        while (True):
            f = open("temp.txt","w")
            for line in sudoku:
                f.write(str(line))
                f.write('\n')
            f.close()
            os.system("gedit temp.txt")
            print("Entered matrix is : ")
            sudoku = read_matrix("temp.txt")
            print_matrix(sudoku)
            print("Do you wish to edit above matrix ? \n(Yes/No)")
            if not accepted() and valid_sudoku(sudoku):
                break
            elif not valid_sudoku(sudoku):
                print("Detected sudoku seems invalid.\nPlease edit the matrix in the opened .txt file and then save")
        os.system("rm temp.txt")
    return sudoku