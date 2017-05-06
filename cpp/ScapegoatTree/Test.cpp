#include <iostream>
#include <ctime>
#include <cstdio>
#include <fstream> 
#include <cstdlib>
#include <cstring>
#include <algorithm>

#include "ScapegoatTree.hpp"

using namespace std;

int n, ContentSize;

int main(){
	ifstream fin("data_input.txt");
	ofstream fout("data_output.txt");
	int ty, id, key;
	fin >> n >> ContentSize;
	
	sjtu::ScapegoatTree Tree(ContentSize);
	bool *content = new bool[ContentSize];	
	for(int i = 1; i <= n; ++i){
		fin >> ty;
		if(ty == 0){ // insert
			fin >> id;
			for(int j = 0; j < ContentSize; ++j)
				fin >> content[j];
			Tree.Insert(id, content);
		}
		else if(ty == 1){ // remove
			fin >> id;
			if(!id) continue;
			Tree.Remove(id);
		}
		else{		
			int *res = NULL;
			int size = 0;
			fin >> key;
			Tree.Query(key, res, size);
			if(size > 0){
				sort(res, res + size);
				for(int j = 0; j < size - 1; ++j)
					fout << res[j] << " ";
				fout << res[size - 1] << endl;
				delete [] res;
			}
			else fout << endl;
		}
	}
	return 0;
}
