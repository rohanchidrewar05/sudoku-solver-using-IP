import time

def inits(sudoku):
	count = 0
	for row_s in sudoku:
		for num in row_s:
			if num !=0:
				count = count+1
	return count

def print_matrix(board):
	for row in board:
		print(row)

def check_row(sudoku,x,num):
	for j in range(len(sudoku[x])):
		if sudoku[x][j] == num:
			return False
	return True

def check_colm(sudoku,y,num):
	for i in range(len(sudoku)):
		if sudoku[i][y] == num:
			return False
	return True

def check_subgrid(sudoku,x,y,num,div_x,div_y):
	x_coef = x//div_x
	x_coef = x_coef * div_x
	y_coef = y//div_y
	y_coef = y_coef * div_y
	
	for i in range(div_x):
		for j in range(div_y):
			if sudoku[x_coef+i][y_coef+j] == num:
				return False
	return True

def check(sudoku,i,j,num,div_x,div_y):
	return check_row(sudoku,i,num) and check_colm(sudoku,j,num) and check_subgrid(sudoku,i,j,num,div_x,div_y)


def solve(doBacktrack, sudoku, i, j, count,limit,div_x,div_y):
	if count == limit:
		print("Solved it : \n")
		print_matrix(sudoku)
		return False

	rows, cols = len(sudoku),len(sudoku[0])

	if (i >= rows) or (j >= cols) :
		return False
	
	m = 1
	if sudoku[i][j] == 0 :
		while ( doBacktrack and (m < rows+1) and (i < rows) and (j < cols)):
			if check(sudoku,i,j,m,div_x,div_y):
				sudoku[i][j] = m
				if i < rows-1 and j < cols :
					doBacktrack = solve(True,sudoku,i+1,j,count+1,limit,div_x,div_y)
				elif i >= rows-1 and j < cols-1:
					doBacktrack = solve(True,sudoku,0,j+1,count+1,limit,div_x,div_y)
				
				if doBacktrack and count+1 == limit:
					print("Solved it : \n")
					print_matrix(sudoku)
					return False
				if doBacktrack:
					sudoku[i][j] = 0	
			m = m + 1
		
		if (doBacktrack and (m == rows+1)):
			return True
	else:
		if (i<rows-1) and (j<cols):
			doBacktrack = solve(True,sudoku,i+1,j,count,limit,div_x,div_y)
		elif (i>=rows-1) and (j<cols-1):
			doBacktrack = solve(True,sudoku,0,j+1,count,limit,div_x,div_y)
			
		if doBacktrack and (count+1 == limit):
			print("Solved it : \n")
			print_matrix(sudoku)
			return False
		
		if doBacktrack:
			return True
	return False

	


def sudoku_solver(sudoku):
	rows, cols = len(sudoku),len(sudoku[0])
	div_y = cols//3
	div_x = rows//div_y
	count = inits(sudoku)
	limit = rows*cols
	print('rows : ',rows,' coloumns : ',cols, ' count : ',count)
	print("Initial matrix :\n")
	print_matrix(sudoku)
	print('\n')
	return solve(True,sudoku,0,0,count,limit,div_x,div_y)