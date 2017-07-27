import ctypes

#so = ctypes.cdll.LoadLibrary
#lib = so('./treeLib.so')

class Tree():
	def __init__(self):
		self.so = ctypes.cdll.LoadLibrary
		self.lib = self.so('./treeLib.so')

	def insert(self, id, key):
		key = ctypes.c_char_p(key)
		self.lib.Insert(id, key)

	def remove(self, id):
		self.lib.Remove(id)

	def query(self, key):
		self.lib.Query.restype = ctypes.c_int
		self.lib.Query.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
		data = ctypes.c_int()
		self.lib.Query(key, ctypes.byref(data), 0)
		return self.getIdList()

	def getIdList(self):
		idlist = []
		infile = open("tmp", "r")
		line = infile.readline().strip().split(" ")
		return line
