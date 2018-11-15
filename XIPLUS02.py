import math


''' file foramt
	x bytes: char list
	1 byte: length of code length (=y)
	char huffman code length (y bits)
		+ huffman code
		(number of chars times)
	encoded content
	1 byte: number of padding zero after content
	4 bytes: chars size (=x)
'''

def XIPLUS02_encode(infile, outfile, utf8):
	print("----- XIPLUS02_encode -----")
	print("\tutf8 =", utf8)

	with open(infile, "rb") as fin:
		data = fin.read()

	if utf8:
		try:
			data = data.decode()
		except UnicodeDecodeError as e:
			print("\tdecode fail. skip.\n")
			return False

	with open(outfile, "wb") as fout:
		dic = {}
		for c in data:
			if c not in dic:
				dic[c] = 1
			else:
				dic[c] += 1

		# if there are no char, add a placeholder
		print("\tthere are {} chars".format(len(dic)))
		if len(dic) == 0:
			dic[0] = 0

		lenofchars = 0
		for c in dic:
			if utf8:
				fout.write(c.encode())
				lenofchars += len(c.encode())
			else:
				fout.write(bytes([c]))
				lenofchars += 1

		print("\tlenofchars =", lenofchars)

		dicpool = []
		for c in dic:
			dicpool.append(Node(c, dic[c]))

		if len(dicpool) == 1:
			dicpool.append(Node(None, 0))

		while len(dicpool) > 1:
			dicpool.sort(key=lambda v:v.weight)
			a = dicpool.pop(0)
			b = dicpool.pop(0)
			c = Node(None, a.weight+b.weight)
			c.left = a
			c.right = b
			a.parent = c
			a.code = '0'
			b.parent = c
			b.code = '1'
			dicpool.append(c)

		newdicpool = []
		while len(dicpool) > 0:
			c = dicpool.pop(0)
			a = c.left
			b = c.right
			if a is not None:
				a.code = c.code + a.code
				if a.char is None:
					dicpool.append(a)
				else:
					newdicpool.append(a)
				
			if b is not None:
				b.code = c.code + b.code
				if b.char is None:
					dicpool.append(b)
				else:
					newdicpool.append(b)

		newdicpool.sort(key=lambda v:v.char)
		maxcodelen = 0
		for node in newdicpool:
			maxcodelen = max(maxcodelen, len(node.code))
			# print("\t{}\t{:8}\t{}".format(repr([node.char]), node.code, node.weight))

		print("\tmaxcodelen =", maxcodelen)
		lofcl = math.ceil(math.log2(maxcodelen+1))
		print("\tlofcl =", lofcl)
		fout.write(bytes([lofcl]))

		table = {}
		for node in newdicpool:
			table[node.char] = node.code

		temp = ""
		for c in dic:
			temp += bin(len(table[c]))[2:].zfill(lofcl)
			temp += table[c]

			while len(temp) >= 8:
				fout.write(bytes([int(temp[0:8], 2)]))
				temp = temp[8:]

		for char in data:
			temp += table[char]

			while len(temp) >= 8:
				fout.write(bytes([int(temp[0:8], 2)]))
				temp = temp[8:]

		paddingzerolen = (8-len(temp)%8)%8
		print("\tpaddingzerolen =", paddingzerolen)
		for i in range(paddingzerolen):
			temp += "0"

		while len(temp) >= 8:
			fout.write(bytes([int(temp[0:8], 2)]))
			temp = temp[8:]

		fout.write(bytes([paddingzerolen]))
		fout.write(lenofchars.to_bytes(4, 'big'))

	print("----- XIPLUS02_encode -----")
	return True

def XIPLUS02_decode(infile, outfile, utf8):
	print("----- XIPLUS02_decode -----")
	print("\tutf8 =", utf8)

	with open(infile, "rb") as fin:
		data = fin.read()

	paddingzerolen = data[-5]
	print("\tpaddingzerolen =", paddingzerolen)
	lenofchars = int.from_bytes(data[-4:], "big")
	print("\tlenofchars =", lenofchars)
	lofcl = data[lenofchars]
	print("\tlofcl =", lofcl)

	chars = data[0:lenofchars]

	if utf8:
		chars = list(chars.decode())

	numberofchars = len(chars)
	print("\tnumberofchars =", numberofchars)

	temp = ""
	offset = lenofchars+1
	dic = {}
	for x in range(numberofchars):
		char = chars[x]
		while len(temp) < lofcl:
			temp += bin(data[offset])[2:].zfill(8)
			offset += 1
		codelen = int(temp[0:0+lofcl], 2)
		temp = temp[lofcl:]

		while len(temp) < codelen:
			temp += bin(data[offset])[2:].zfill(8)
			offset += 1
		code = temp[0:0+codelen]
		temp = temp[codelen:]

		# print("\t{}\t{:8}".format(repr([char]), code))
		dic[code] = char

	allcodelen = (len(data) - offset  - 5) * 8 + len(temp) - paddingzerolen

	with open(outfile, "wb") as fout:
		nowcode = ""
		i = 0
		nowcodelen = 0
		while nowcodelen < allcodelen:
			i += 1
			nowcodelen += 1
			while len(temp) < i:
				temp += bin(data[offset])[2:].zfill(8)
				offset += 1
					
			if temp[0:i] in dic:
				if utf8:
					fout.write(dic[temp[0:i]].encode())
				else:
					fout.write(bytes([dic[temp[0:i]]]))
				temp = temp[i:]
				i = 0

	print("----- XIPLUS02_decode -----")
	return True

class Node():
	def __init__(self, char, weight):
		self.code = ''
		self.char = char
		self.weight = weight
		self.parent = None
		self.left = None
		self.right = None

	def __repr__(self):
		if self.parent is None:
			return "({}, '{}', {}, None)".format(self.code, self.char, self.weight)
		return "({}, '{}', {}, {})".format(self.code, self.char, self.weight, self.parent.char)
