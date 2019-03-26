from flask import Flask, render_template, request, jsonify
import cv2

def getArgs(requestValues, *expected):
	results = []

	for arg in expected:
		if arg in requestValues.keys() and isinstance(requestValues[arg], str):
			results.append(requestValues[arg])
		else:
			results.append(None)

	return tuple(results)

def getAuthorization(requestHeaders):
	token = None
	if 'Authorization' in requestHeaders.keys():
		token = requestHeaders['Authorization']

	return token



# def allNotNone(items):
# 	results = list

# 	for arg in expected:
# 		if arg in requestValues.keys() and isinstance(requestValues[arg], str):
# 			results.append(requestValues[arg])
# 		else:
# 			results.append(None)

# 	return tuple(results)

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

def getValidString(text):
	# if not (' ' in text) and not ('	' in text)and text != '':
	if not (' ' in text) and not ('	' in text)and text != '':
		return text
	else:
		return None
