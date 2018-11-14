import math

def XIPLUS01_encode(infile, outfile):
	with open(infile, "rb") as fin:
		data = fin.read()

	data = data.decode()
	with open(outfile, "wb") as fout:
		# result = b""

		chars = list(set(list(data)))
		print("\tfind {} different chars".format(len(chars)))
		dic = {}
		for t in range(len(chars)):
			dic[chars[t]] = t+1
		# print(chars)
		# result += ("".join(chars)).encode()
		# result += bytes([0])
		fout.write(("".join(chars)).encode())
		fout.write(bytes([0]))

		cbit = math.ceil(math.log2(len(chars)))
		# print("cbit=", cbit)
		temp = ""
		for char in data:
			# temp += bin(chars.index(char) + 1)[2:].zfill(cbit)
			temp += bin(dic[char])[2:].zfill(cbit)
			while len(temp) >= 8:
				fout.write(bytes([int(temp[0:8], 2)]))
				temp = temp[8:]

		for i in range((8-len(temp)%8)%8):
			temp += "0"

		while len(temp) >= 8:
			fout.write(bytes([int(temp[0:8], 2)]))
			temp = temp[8:]
		# for i in range(0, len(temp), 8):
		# 	result += bytes([int(temp[i:i+8], 2)])

	# return result

def XIPLUS01_decode(infile, outfile):
	with open(infile, "rb") as fin:
		data = fin.read()

	with open(outfile, "wb") as fout:
		i = 0
		while data[i] != 0:
			i += 1
		chars = data[:i]
		# print(chars.decode())
		chars = list(chars.decode())

		# print(chars)
		cbit = math.ceil(math.log2(len(chars)))
		# print("cbit=", cbit)

		temp = ""
		for b in data[i+1:]:
			temp += bin(b)[2:].zfill(8)

		# result = b""
		for i in range(cbit, len(temp), cbit):
			fout.write(chars[int(temp[i-cbit:i], 2)-1].encode())
			# result += chars[int(temp[i-cbit:i], 2)-1].encode()

	# return result
