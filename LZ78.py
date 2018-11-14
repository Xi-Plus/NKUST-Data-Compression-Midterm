def LZ78_encode(infile, outfile):
	print("----- LZ78_encode -----")
	with open(infile, "rb") as fin:
		data = fin.read()

	with open(outfile, "wb") as fout:
		# result = b""
		tree = {"index": 0}
		node = tree
		offset = 0
		idx = 0
		dlen = len(data)
		while offset < dlen:
			# if offset % 10000 < 5:
			# 	print(offset)
			# print("read {}".format(data[offset]))
			# print(node)
			if data[offset] not in node:
				# result += bytes([int(idx/256), idx%256])
				# print("output {} {}".format(node["index"], data[offset]))
				fout.write(bytes([node["index"]]))
				fout.write(bytes([data[offset]]))
				# result += bytes([node["index"]])
				# result += bytes([data[offset]])
				# result += data[offset].encode()
				idx += 1
				node[data[offset]] = {"index": idx}
				offset += 1
				node = tree
				if idx >= 256:
					tree = {"index": 0}
					node = tree
					idx = 0
					# input()
			else:
				node = node[data[offset]]
				offset += 1
			# input()
		# result += bytes([node["index"]])
		# result += bytes([0])
		fout.write(bytes([node["index"]]))
		fout.write(bytes([0]))
	print("----- LZ78_encode -----")
	return True

def LZ78_decode(infile, outfile):
	print("----- LZ78_decode -----")
	with open(infile, "rb") as fin:
		data = fin.read()

	with open(outfile, "wb") as fout:
		# result = b""
		tree = [b""]
		offset = 0
		while offset < len(data):
			# print(data[offset], tree[data[offset]], chr(data[offset+1]))
			# result += tree[data[offset]]
			fout.write(tree[data[offset]])
			if data[offset+1] != 0:
				# result += bytes([data[offset+1]])
				fout.write(bytes([data[offset+1]]))
			tree.append(tree[data[offset]] + bytes([data[offset+1]]))
			offset += 2
			if len(tree) >= 257:
				tree = [b""]
				# print("clear tree")
				# input()
		# print(tree)
	# return result
	print("----- LZ78_decode -----")
	return True
