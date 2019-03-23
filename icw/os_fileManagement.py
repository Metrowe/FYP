import os
import random
import string
import time

def deleteFile(path):
	success = False
	if os.path.exists(path):
		os.remove(path)

		success = True
	else:
		print("Delete file failed : File does not exist")

def getUniqueTimeStamp():
	t = time.localtime(time.time())

	timeString = '{}-{}-{}_{}-{}-{}'.format(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
	randomString = ''.join(random.choice(string.ascii_letters) for i in range(5))
	return timeString + '_' + randomString