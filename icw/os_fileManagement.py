import os

def deleteFile(path):
	success = False
	if os.path.exists(path):
		os.remove(path)

		success = True
	else:
		print("Delete file failed : File does not exist")