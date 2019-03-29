from database_connection import Session
import database_modify as dbModify
import database_query as dbQuery

def main():
	result = success = dbQuery.filterGalleryImages(None,None)

	print('result:',result)

	if(len(result) > 0):
		print('Success!!!!')
	else:
		print('Fail....')

	for image in result:
		print(image.type)
	

main()