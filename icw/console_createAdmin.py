import sys

from database_connection import Session
import database_classes as table
import database_query as dbQuery
import database_modify as dbModify

import console_argv

# def insertAdmin(username,password):
# 	newUser = None
# 	existingUser = dbQuery.nameUser(username)

# 	if existingUser == None:
# 		newUser = table.User(username=username,password=password,admin=True)
# 		Session.add(newUser)
# 		success = safeCommit()

# 		if not success:
# 			newUser = None

# 	return newUser

def main():
	username, password = console_argv.getX(sys.argv, 2, '<username> <password>')
	result = dbModify.insertAdmin(username,password)

	if(result != None):
		print('Success!!!!')
	else:
		print('Fail....')


main()