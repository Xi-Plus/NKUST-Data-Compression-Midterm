import math


''' file foramt
	char list
	content
	4 bytes: header size
'''

def XIPLUS01_encode(infile, outfile, utf8):
	print("----- XIPLUS01_encode -----")
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
		chars = list(set(list(data)))
		print("\tfind {} different chars".format(len(chars)))

		headersize = 0
		if utf8:
			fout.write(("".join(chars)).encode())
			headersize = len(("".join(chars)).encode())
		else:
			for char in chars:
				fout.write(bytes([char]))
				headersize += len(bytes([char]))

		print("\theadersize =", headersize)

		dic = {}
		for t in range(len(chars)):
			dic[chars[t]] = t

		cbit = math.ceil(math.log2(len(chars)))
		print("\tcbit =", cbit)

		temp = ""
		for char in data:
			temp += bin(dic[char])[2:].zfill(cbit)
			while len(temp) >= 8:
				fout.write(bytes([int(temp[0:8], 2)]))
				temp = temp[8:]

		for i in range((8-len(temp)%8)%8):
			temp += "0"

		while len(temp) >= 8:
			fout.write(bytes([int(temp[0:8], 2)]))
			temp = temp[8:]
		fout.write(headersize.to_bytes(4, 'big'))

	print("----- XIPLUS01_encode -----")
	return True

def XIPLUS01_decode(infile, outfile, utf8):
	print("----- XIPLUS01_decode -----")
	print("\tutf8 =", utf8)

	with open(infile, "rb") as fin:
		data = fin.read()

	with open(outfile, "wb") as fout:
		headersize = int.from_bytes(data[-4:], "big")
		print("\theadersize =", headersize)

		chars = data[0:headersize]

		if utf8:
			chars = list(chars.decode())

		cbit = math.ceil(math.log2(len(chars)))
		print("\tcbit=", cbit)

		temp = ""
		for offset in range(headersize, len(data)-4):
			temp += bin(data[offset])[2:].zfill(8)
			while len(temp) >= cbit:
				if utf8:
					fout.write(chars[int(temp[0:cbit], 2)].encode())
				else:
					fout.write(bytes([chars[int(temp[0:cbit], 2)]]))
				temp = temp[cbit:]

	print("----- XIPLUS01_decode -----")
	return True
