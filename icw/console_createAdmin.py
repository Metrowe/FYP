import sys

import database_modify as dbModify
import console_argv

def main():
	username, password = console_argv.getX(sys.argv, 2, '<username> <password>')
	result = dbModify.insertAdmin(username,password)

	if(result != None):
		print('Success!!!!')
	else:
		print('Fail....')


main()