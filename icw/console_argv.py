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
	op1, op2 = getX(sys.argv, 2, '<val 1> <val2>')
	print('op1 = ' + op1)
	print('op2 = ' + op2)