from tree import Tree

def main():
	tree = Tree()
	#tree.query(3) Segmentation fault(core dumpted)
	tree.insert(1, "0010010011")
	tree.insert(2, "1100101110")
	tree.insert(3, "0001110001")
	tree.insert(4, "0011111100")
	print tree.query(0)
	print tree.query(5)
	print tree.query(4)
	tree2 = Tree()
	tree2.remove(4)
	print tree.query(4)
	print tree.query(12)
	#tree2.remove(20) Segmentation fault(core dumped)

if __name__ == "__main__":
	main()
