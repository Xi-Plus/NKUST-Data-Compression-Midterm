import sys
import os
import math
from LZ78 import *
from XIPLUS01 import *
from huffman import *
import time

algolist = {
	"auto": [],
	"lz78": [LZ78_encode, LZ78_decode, []],
	"xp01": [XIPLUS01_encode, XIPLUS01_decode, [True]],
	"xp01b": [XIPLUS01_encode, XIPLUS01_decode, [False]],
	"huffman": [huffman_encode, huffman_decode, []],
}

ctype = sys.argv[1]
algo = sys.argv[2].lower()
finname = sys.argv[3]
foutname = sys.argv[4]

if ctype == "encode":
	if algo not in algolist:
		exit("alog not found")
	print("encode by {}".format(algo))
	# with open(finname, "rb") as fin:
	# 	data = fin.read()
	# print("old size: {}".format(len(data)))
	oldsize = os.path.getsize(finname)
	print("old size: {}".format(oldsize))
	start = time.time()
	if algo == "auto":
		minsize = 2**100
		minalgo = ""
		for algo2 in list(algolist.keys())[1:]:
			fouttmp = "tmp_{}.bin".format(algo2)
			result = algolist[algo2][0](finname, fouttmp, *algolist[algo2][2])
			if result == False:
				print("{} skip".format(algo2))
				continue
			newsize = os.path.getsize(fouttmp)
			print("{} {}".format(algo2, newsize))
			if newsize < minsize:
				minalgo = algo2
				minsize = newsize

		print("real encode by {}".format(minalgo))
		for algo2 in list(algolist.keys())[1:]:
			fouttmp = "tmp_{}.bin".format(algo2)
			if algo2 == minalgo:
				os.replace(fouttmp, foutname)
			else:
				if os.path.exists(fouttmp):
				   os.remove(fouttmp)
		with open(foutname, "ab") as fout:
			fout.write(bytes([list(algolist.keys()).index(minalgo)]))
	else:
		algolist[algo][0](finname, foutname, *algolist[algo][2])
	print("spend {} s".format(time.time()-start))
	# result = algolist[algo][0](data)
	# print("new size: {}".format(len(result)))
	newsize = os.path.getsize(foutname)
	print("new size: {}".format(newsize))
	print("compression ratio: {}".format(oldsize/newsize))
	# with open(foutname, "wb") as fout:
	# 	fout.write(result)

elif ctype == "decode":
	if algo not in algolist:
		exit("alog not found")
	print("decode by {}".format(algo))
	# with open(finname, "rb") as fin:
	# 	data = fin.read()
	# print("old size: {}".format(len(data)))
	start = time.time()
	if algo == "auto":
		with open(finname, 'rb') as fin:
			data = fin.read()
		fintmp = "tmp_auto.bin"
		with open(fintmp, 'wb') as fin:
			fin.write(data[:-1])
		algo2 = list(algolist.keys())[data[-1]]
		print("real decode by {}".format(algo2))
		algolist[algo2][1](fintmp, foutname, *algolist[algo2][2])
		os.remove(fintmp)
	else:
		algolist[algo][1](finname, foutname, *algolist[algo][2])
	print("spend {} s".format(time.time()-start))
	# result = algolist[algo][1](data)
	# print("new size: {}".format(len(result)))
	# print("compression ratio: {}".format(len(data)/len(result)))
	# with open(foutname, "wb") as fout:
	# 	fout.write(result)
else:
	print("nothing to do")
