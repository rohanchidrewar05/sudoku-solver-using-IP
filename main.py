import time
from image_processor import sudoku_extractor
from solver import sudoku_solver
from check import check_sudoku
from utils import get_path

if __name__ == "__main__":
    
    print("Please select Image to be processed")
    img_name = get_path()

    sudoku = sudoku_extractor(img_name)

    sudoku = check_sudoku(sudoku)

    tic = time.time()
    sudoku = sudoku_solver(sudoku)
    toc = time.time()
    print("Solved in : ",toc-tic)