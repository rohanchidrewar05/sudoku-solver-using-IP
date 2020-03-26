#include<iostream>
#include<vector>
using namespace std;
int sides = 9;
int limit = sides*sides;

 //sudoku(9,vector<int>(9));

/*
vector<vector<int> > sudoku={
	{6,4,0,2,0,0},
	{0,5,1,0,0,0},
	{3,6,4,0,0,2},
	{5,0,0,4,3,6},
	{0,0,0,6,4,0},
	{0,0,6,0,2,5}
};
*/
int div_x = 3, div_y = 3;

void print_matrix(vector<vector<int> > board)
{
	for(int i=0; i<board.size();i++ )
	{
		for(int j=0;j<board[i].size();j++)
			cout<<board[i][j]<<" ";
		cout<<endl;
	}
}

void init(vector<vector<int> >sudoku, int& counts)
{
	for(int i=0;i<sides;i++)
	{
		for(int j=0;j<sides;j++)
			{
				if(sudoku[i][j] != 0)
					counts++;
			}
	}
}

bool check_row(vector<vector<int> >&sudoku,int x,int num)
{
	for(int i=0; i<sides; i++)
	{
		if(sudoku[x][i] == num)
			return false;
	}
	return true;
}

bool check_column(vector<vector<int> >&sudoku,int y,int num)
{
	for(int i=0;i<sides;i++)
	{
		if(sudoku[i][y]==num)
			return false;
	}
	return true;
}

bool check_subgrid(vector<vector<int> >&sudoku,int x,int y,int num)
{
	int x_coef = x/div_x;
	x_coef = x_coef * div_x;
	int y_coef = y/div_y;
	y_coef = y_coef * div_y;

	for(int i=0; i<div_x;i++)
	{
		for(int j=0;j<div_y;j++)
		{
			if(sudoku[x_coef+i][y_coef+j] == num)
				return false;
		}
	}
	return true;
}

bool check(vector<vector<int> >&sudoku,int i, int j,int num)
{
	return check_row(sudoku,i,num)&&check_column(sudoku,j,num)&&check_subgrid(sudoku,i,j,num);
}
/*
bool diffcheck(int i, int j,int num)
{
	return check_row(i,num)&&check_column(j,num)&&check_subgrid(i,j,num);
}
*/
bool solve(bool doBacktrack,vector<vector<int> >sudoku,int i,int j,int counts)
{
	if(counts == limit){
//		cout<<"Limit anna:"<<endl;
		print_matrix(sudoku);
		return false;
	}

	if(i>=sides || j >= sides)
	{
//		cout<<"sides anna:"<<endl;
	//	print_matrix(sudoku);
		return false;
	}
	int m = 1;
	//cout<<"i: "<<i<<" j: "<<j<<endl;
	if((sudoku[i][j] == 0))
	{
		while(doBacktrack && m<sides+1 && i< sides && j<sides)
		{
			if(check(sudoku,i,j,m))
			{
		//	cout<<"m :"<<m<<" ";
			sudoku[i][j] = m;
		//	cout<<"i: "<<i<<" j: "<<j<<"m :"<<m<<" ";
			if( i < sides-1 && j < sides )
				doBacktrack = solve(true,sudoku,i+1,j,counts+1);
			else if(i >= sides-1 && j < sides-1 )
				doBacktrack = solve(true,sudoku,0,j+1,counts+1);
			
			if(doBacktrack && counts+1 == limit)
				{
				//	cout<<"i: "<<i<<" j: "<<j<<" m: "<<m<<endl;
					cout<<"Solved it : "<<endl;
					print_matrix(sudoku);
					return false;
				}
			}
			m++;	
		}
		if(doBacktrack && m == sides+1)
		{
			//cout<<"go back bitch"<<endl;
			return true;
		}
	}
	else
	{
		if( i < sides-1 && j < sides )
			doBacktrack = solve(true,sudoku,i+1,j,counts);
		else if(i >= sides-1 && j < sides-1 )
			doBacktrack = solve(true,sudoku,0,j+1,counts);
		if(doBacktrack && counts+1 == limit)
			{
				cout<<"Solved it : "<<endl;
				print_matrix(sudoku);
				return false;
			}
		if(doBacktrack)
		{
//			cout<<"go back bitch"<<endl;
			return true;
		}
	}
//	cout<<"WTF"<<endl;
	return false;
}

int main()
{
	int counts = 0;
	vector<vector<int> >	sudoku = {
			{0,0,0,0,0,4,0,0,0},
			{0,0,0,0,0,0,6,0,8},
			{0,0,8,0,1,0,0,0,0},
			{0,0,5,0,3,0,8,0,2},
			{0,7,0,2,0,0,0,0,1},
			{0,6,0,0,0,0,0,0,0},
			{0,0,0,4,0,7,0,9,0},
			{0,9,0,0,0,0,4,7,0},
			{0,3,0,5,2,0,0,0,0}
	};
	init(sudoku,counts);
//	cout<<"count :"<<counts<<endl;
	cout<<"Initial matrix :"<<endl;
	print_matrix(sudoku);
	cout<<endl;
	solve(true,sudoku,0,0,counts);
	return 0;
}
