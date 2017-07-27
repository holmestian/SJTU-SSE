#include <iostream>
#include <cstdio> 
#include <cstdlib>
#include <algorithm>
#include <fstream>

using namespace std;

const double cSIZE_THRESHOLD = 0.7;

class ScapegoatTreeNode{
public:
	ScapegoatTreeNode *ls, *rs, *father;
	int ContentSize, id, TreeSize;
	bool* content;
	bool IsRealNode;
	int SubTreeMinId, SubTreeMaxId;
	
	ScapegoatTreeNode(ScapegoatTreeNode *_ls = NULL, ScapegoatTreeNode *_rs = NULL, 
						ScapegoatTreeNode *_father = NULL, int _id = 0, 
		 				int _ContentSize = 0, bool* _content = NULL, bool _IsRealNode = false) : 
		ls(_ls), rs(_rs), father(_father), id(_id), ContentSize(_ContentSize), IsRealNode(_IsRealNode) {
		TreeSize = 1;
		SubTreeMinId = SubTreeMaxId = id;
		content = new bool[ContentSize];
		if(_content != NULL){
			for(int i = 0; i < ContentSize; ++i)
				content[i] = _content[i];
		}
	}

	void update(){
		int lsize, rsize;
		lsize = (ls == NULL) ? 0 : ls -> TreeSize;
		rsize = (rs == NULL) ? 0 : rs -> TreeSize;
		TreeSize = lsize + rsize + 1;
		bool lscontent, rscontent;
		for(int i = 0; i < ContentSize; ++i){
			lscontent = (ls == NULL) ? 0 : ls -> content[i];
			rscontent = (rs == NULL) ? 0 : rs -> content[i];
			content[i] = (lscontent | rscontent);
		}
		if(TreeSize > 1){
			SubTreeMinId = (ls != NULL) ? ls -> SubTreeMinId : rs -> SubTreeMinId;
			SubTreeMaxId = (rs != NULL) ? rs -> SubTreeMaxId : ls -> SubTreeMaxId;
			id = (rs != NULL) ? rs -> SubTreeMinId : ls -> SubTreeMaxId + 1;
		} 
	}

	~ScapegoatTreeNode(){
		delete [] content;
	}

};

class ScapegoatTree{
private:
	ScapegoatTreeNode* root;
	int ContentSize;
	ScapegoatTreeNode* NeedReBuild;

	int Max(const int &a, const int &b){
		return a > b ? a : b;
	}

	int Find_Get_Size(ScapegoatTreeNode* t, const int &key){
		if(t == NULL) return 0;
		if(t -> content[key] == false) return 0;
		if(t -> IsRealNode){
			if(t -> content[key]) return 1;
			else return 0;
		}
		return Find_Get_Size(t -> ls, key) + Find_Get_Size(t -> rs, key);
	}

	void Find_GetId(ScapegoatTreeNode* t, const int &key, int &top, int* Result){
		if(t -> content[key] == false) return;
		if(t -> IsRealNode){
			if(t -> content[key]){
				Result[top++] = t -> id;
			}
			return;
		}
		if(t -> ls != NULL) 
			Find_GetId(t -> ls, key, top, Result);
		if(t -> rs != NULL)
			Find_GetId(t -> rs, key, top, Result);
	}

	void Inner_Insert(ScapegoatTreeNode* &t, const int &id, bool* content){
		if(t == NULL){
			t = new ScapegoatTreeNode(NULL, NULL, t, id, ContentSize, content, true);
			return;
		}
		if(t -> IsRealNode){ // leaf key point
			if(t -> ls != NULL || t -> rs != NULL){ // check error
				printf("Node %d has at least one son while inserting new node!\n", t -> id);
				throw(-1);
			}
			ScapegoatTreeNode *p = new ScapegoatTreeNode(NULL, NULL, t, t -> id, ContentSize, t -> content, true);
			ScapegoatTreeNode *q = new ScapegoatTreeNode(NULL, NULL, t, id, ContentSize, content, true);
			if(id < t -> id){
				t -> ls = q;
				t -> rs = p;
			}
			else{
				t -> ls = p;
				t -> rs = q;
			}
			t -> update();
			t -> IsRealNode = false;
			return;
		}
		if(id < t -> id)
			Inner_Insert(t -> ls, id, content);
		else
			Inner_Insert(t -> rs, id, content);
		t -> update();
		int lsize = (t -> ls == NULL) ? 0 : t -> ls -> TreeSize;
		int rsize = (t -> rs == NULL) ? 0 : t -> rs -> TreeSize;
		if(Max(lsize, rsize) > (t -> TreeSize) * cSIZE_THRESHOLD){
			NeedReBuild = t;
		}
	}

	void Inner_Remove(ScapegoatTreeNode* &t, const int &id){
		if(t -> IsRealNode && t -> id == id){
			if(t -> ls != NULL || t -> rs != NULL){ // check error
				printf("Node %d has at least one son while removing it!\n", id);
				throw(-1);
			}
			delete t;
			t = NULL;
			return;
		}
		if(id < t -> id)
			Inner_Remove(t -> ls, id);
		else
			Inner_Remove(t -> rs, id);
		t -> update();
		if(t -> IsRealNode == false && t -> TreeSize == 1){ // delete redundant Node
			delete t;
			t = NULL;
			return;
		}
		int lsize = (t -> ls == NULL) ? 0 : t -> ls -> TreeSize;
		int rsize = (t -> rs == NULL) ? 0 : t -> rs -> TreeSize;
		if(Max(lsize, rsize) > (t -> TreeSize) * cSIZE_THRESHOLD){
			NeedReBuild = t;
		}
	}

	void Dfs_GetId(ScapegoatTreeNode *t, int &top, ScapegoatTreeNode **IdSeq){
		if(t -> IsRealNode){
			if(t -> ls != NULL || t -> rs != NULL){ // check error
				printf("Node %d has at least one son while accessing it!\n", t -> id);
				throw(-1);
			}
			IdSeq[++top] = t;
			return;
		}
		if(t -> ls != NULL)
			Dfs_GetId(t -> ls, top, IdSeq);
		if(t -> rs != NULL)
			Dfs_GetId(t -> rs, top, IdSeq);
		delete t;

	}

	ScapegoatTreeNode* Build(int l, int r, ScapegoatTreeNode** IdSeq, ScapegoatTreeNode *father){
		if(l == r){
			IdSeq[l] -> father = father;
			return IdSeq[l];
		}
		ScapegoatTreeNode *node = new ScapegoatTreeNode(NULL, NULL, father, 0, ContentSize, NULL, false);
		ScapegoatTreeNode *ls, *rs;
		int mid = (l + r) >> 1;
		ls = Build(l, mid, IdSeq, node);
		rs = Build(mid + 1, r, IdSeq, node);
		node -> ls = ls;
		node -> rs = rs;
		node -> update();
		return node;
	}

	void ReBuild_SubTree(){
		ScapegoatTreeNode *father = NeedReBuild -> father;
		ScapegoatTreeNode **IdSeq = new ScapegoatTreeNode*[NeedReBuild -> TreeSize + 1];
		int top = 0;
		Dfs_GetId(NeedReBuild, top, IdSeq);
		ScapegoatTreeNode *NewNode = Build(1, top, IdSeq, father);
		delete [] IdSeq;
		if(father == NULL){
			root = NewNode;
			return;
		}
		if(father -> ls == NeedReBuild)
			father -> ls = NewNode;
		else 
			father -> rs = NewNode;
		while(father != NULL){
			father -> update();
			father = father -> father;
		}
	}

	void Clear_Tree(ScapegoatTreeNode *t){
		if(t == NULL) return;
		Clear_Tree(t -> ls);
		Clear_Tree(t -> rs);
		delete t;
	}

	void Output_Tree(ScapegoatTreeNode *t, int depth){
		for(int i = 0; i < depth; ++i)
			printf("\t");
		printf("%d %d\n", t -> id, t -> IsRealNode);
		if(t -> ls != NULL)
			Output_Tree(t -> ls, depth + 1);
		if(t -> rs != NULL)
			Output_Tree(t -> rs, depth + 1);
	}

public:

	ScapegoatTree(int _ContentSize = 0) : ContentSize(_ContentSize){
		root = NULL;
		NeedReBuild = NULL;
	}
	
	void Insert(const int &id, bool *content){
		NeedReBuild = NULL;
		Inner_Insert(root, id, content);
		if(NeedReBuild != NULL){
			ReBuild_SubTree();
		}
	}

	void Remove(const int &id){
		NeedReBuild = NULL;
		Inner_Remove(root, id);
		if(NeedReBuild != NULL){
			ReBuild_SubTree();
		}
	}

	int Query(const int &key, int* &uResult, int &uSize){
		int LocalSize = Find_Get_Size(root, key);
		int* Result = new int[LocalSize + 1];
		int top = 0;
		Find_GetId(root, key, top, Result);
		uSize = LocalSize;
		uResult = Result;
		return LocalSize;
	}

	~ScapegoatTree(){
		Clear_Tree(root);
	}
};

extern "C" {
	int ContentSize = 100;
	ScapegoatTree obj(ContentSize);

	void Insert(int id, char* s) {
		bool* content = new bool[ContentSize];
		for (int i = 0; i < ContentSize; ++i) {
			content[i] = int(s[i]) - 48;
		}
		obj.Insert(id, content);
	}

	void Remove(int id) {
		obj.Remove(id);
	}

	void Query(int key, int* res, int size) {
		ofstream fout("tmp");
		obj.Query(key, res, size);
		if (size > 0) {
			sort(res, res + size);
			for (int j = 0; j < size - 1; ++j) {
				cout << res[j] << " ";
				fout << res[j] << " ";
			}
			cout << res[size - 1] << endl;
			fout << res[size - 1] << endl;
			delete [] res;
		}
		else {
			cout << "No result for this key word" << endl;
			fout << endl;
		}
	}
}
