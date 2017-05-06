#include <iostream>
#include <cstdio>
#include <cstdlib>

using namespace std;

int main(){
	system("CreateDate");
	system("Test");
	for(int i = 0; i < 36; ++i){
		if(system("fc data_output.txt data_res.txt"))
			break;
		system("CreateDate");
		system("Test");
	}
	return 0;
}
