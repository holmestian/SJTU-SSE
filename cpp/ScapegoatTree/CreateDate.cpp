#include <iostream>
#include <ctime>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <algorithm>

using namespace std;

// n + m, ContentSize
// 0: insert, id, content
// 1: remove, id  if id == 0 mean do noting
// 2: find, key

const int cCONTENT_SIZE = 325;

int n = 1000, m = 5000, Count = 1000;

struct node{
	int id;
	bool content[cCONTENT_SIZE];
}SEQ[30001];

bool exist[30001];

int res[30001], top;

int main(){
	srand(time(NULL));
	ofstream fout_input("data_input.txt");
	ofstream fout_res("data_res.txt");
	fout_input << n + m << " " << cCONTENT_SIZE << endl;
	for(int i = 1; i <= n; ++i){
		SEQ[i].id = i;
		for(int j = 0; j < cCONTENT_SIZE; ++j)
			SEQ[i].content[j] = rand() % 2;
		exist[i] = 1;
		fout_input << "0 " << i << " ";
		for(int j = 0; j < cCONTENT_SIZE; ++j)
			fout_input << SEQ[i].content[j] << " ";
		fout_input << endl;
	}
	for(int i = 1; i <= m; ++i){
		int type = rand() % 3;
		if(type == 0){
			SEQ[++n].id = n;
			++Count;
			for(int j = 0; j < cCONTENT_SIZE; ++j)
			SEQ[n].content[j] = rand() % 2;
			exist[n] = 1;
			fout_input << "0 " << n << " ";
			for(int j = 0; j < cCONTENT_SIZE; ++j)
				fout_input << SEQ[n].content[j] << " ";
			fout_input << endl;
		}
		else if(type == 1){
			if(!Count){
				fout_input << "1 0" << endl;
			}
			else{
				int id = 0;
				int pos = rand() % n + 1;
				--Count;
				for(int j = pos; j <= n; ++j){
					if(exist[j]){
						id = SEQ[j].id;
						exist[j] = 0;
						break;
					}
				}
				if(id > 0){
					fout_input << "1 " << id << endl;
					continue;
				}
				for(int j = pos - 1; j > 0; --j){
					if(exist[j]){
						id = SEQ[j].id;
						exist[j] = 0;
						break;
					}
				}
				fout_input << "1 " << id << endl;
			}
		}
		else{
			int key = rand() % cCONTENT_SIZE;
			fout_input << "2 " << key << endl;

			top = 0;
			for(int j = 1; j <= n; ++j){
				if(!exist[j]) continue;
				if(SEQ[j].content[key]){
					res[++top] = SEQ[j].id;
				}
			}
			if(top > 0)
				sort(res + 1, res + 1 + top);
			for(int j = 1; j < top; ++j)
				fout_res << res[j] << " ";
			if(top > 0){
				fout_res << res[top] << endl;
			}
			else fout_res << endl;
		}	
	}
	return 0;
}
