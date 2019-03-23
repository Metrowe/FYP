
def responseError(text):
	return {
		'error': text
	}

def stringToBool(text):
	result = None
	
	if text == 'true':
		result = True
	elif text == 'false':
		result = False

	return result

def validString(text):
	# if not (' ' in text) and not ('	' in text)and text != '':
	if not (' ' in text) and not ('	' in text)and text != '':
		return True
	else:
		return False