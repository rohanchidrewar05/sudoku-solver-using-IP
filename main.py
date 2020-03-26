import time
from image_processor import sudoku_extractor
from solver import sudoku_solver
from check import check_sudoku

if __name__ == "__main__":
    
    print("Enter name of Image to be processed")
    img_name = input()

    sudoku = sudoku_extractor(img_name)

    sudoku = check_sudoku(sudoku)

    tic = time.time()
    sudoku = sudoku_solver(sudoku)
    toc = time.time()
    print("Solved in : ",toc-tic)