main: binfile = $(basename ${f})_${a}.bin
main: outfile = $(basename ${f})_out$(suffix ${f})
main:
	py compress.py encode ${a} ${f} ${binfile}
	py compress.py decode ${a} ${binfile} ${outfile}
	fc ${f} ${outfile}
	del ${binfile}
	del ${outfile}
