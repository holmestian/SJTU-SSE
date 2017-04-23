from commands import *

def main():
	url = "http://www.wangjksjtu.com.cn:2117/"
	h = Http_ClientServer(url)
	h.getAll()
	h.add('1111001001', "0b2952b0d93576dd24b49dcb66a9c7d8")
	h.update(17, '1111001001', "0b2952b0d93576dd24b49dcb66dfc7d8")
	h.search('1111001001')
	h.delete(17)


if __name__ == '__main__':
	main()
