from shutil import copyfile


def nocompress_encode(infile, outfile):
	print("----- nocompress_encode -----")
	copyfile(infile, outfile)
	print("----- nocompress_encode -----")
	return True

def nocompress_decode(infile, outfile):
	print("----- nocompress_decode -----")
	copyfile(infile, outfile)
	print("----- nocompress_decode -----")
	return True
