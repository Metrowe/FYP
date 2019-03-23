import sys

def getX(argv, argCount, instructions):
	args = argv[1:]
	if len(args) == argCount:
		return tuple(args)
	else:
		if isinstance(instructions, str):
			print(argv[0] + ' ' + instructions)
		sys.exit('exit: expected ' + str(argCount) + ' arguments, received ' + str(len(args)))



def testmain():
	# print(type(sys.argv))
	# print(len(sys.argv))

	# for i in sys.argv:
	# 	print(str(i) + ' is type: ' + str(type(i)))

	op1, op2 = getX(sys.argv, 2, '<val 1> <val2>')
	print('op1 = ' + op1)
	print('op2 = ' + op2)
	# getOptions(sys.argv, 2, 'test.py -i <inputfile> -o <outputfile>')

# testmain()


#!/usr/bin/python

# import sys, getopt

# def main(argv):
#    inputfile = ''
#    outputfile = ''
#    try:
#       opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
#    except getopt.GetoptError:
#       print 'test.py -i <inputfile> -o <outputfile>'
#       sys.exit(2)
#    for opt, arg in opts:
#       if opt == '-h':
#          print 'test.py -i <inputfile> -o <outputfile>'
#          sys.exit()
#       elif opt in ("-i", "--ifile"):
#          inputfile = arg
#       elif opt in ("-o", "--ofile"):
#          outputfile = arg
#    print 'Input file is "', inputfile
#    print 'Output file is "', outputfile

# if __name__ == "__main__":
#    main(sys.argv[1:])


# $ test.py -h
# usage: test.py -i <inputfile> -o <outputfile>

# $ test.py -i BMP -o
# usage: test.py -i <inputfile> -o <outputfile>

# $ test.py -i inputfile
# Input file is " inputfile
# Output file is "