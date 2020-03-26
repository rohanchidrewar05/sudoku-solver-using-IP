import os
from solver import print_matrix

def accepted():
    ans = input()
    if( ans == 'yes' or ans == 'y' or ans == 'Y' or ans == 'Yes'):
        return True
    return False

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
    print("Is the following detect matrix correct ?\n(Yes/No)")
    print_matrix(sudoku)
    if not accepted():
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
            print("Do you wish to edit above matrix ? \n (Yes/No)")
            if not accepted():
                break
    os.system("rm temp.txt")
    return sudoku