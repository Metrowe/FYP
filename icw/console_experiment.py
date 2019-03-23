from database_connection import Session
import database_modify as dbModify
import database_query as dbQuery

def main():
	# result = submissionId = dbModify.insertGuestSubmission('originalPath','isolatePath','summaryPath','animalLabel',True,True)
	# result = success = dbModify.deleteSubmission(1)
	result = success = dbQuery.filterGalleryImages(None,None)

	print('result:',result)

	# if(submissionId != None):
	# if(submissionId != None):
	if(len(result) > 0):
		print('Success!!!!')
	else:
		print('Fail....')

	for image in result:
		print(image.type)
	

main()