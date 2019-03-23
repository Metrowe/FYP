import jwt
import configuration_strings

# def encodeToken(payload):
def encode(payload):
	return jwt.encode(payload, configuration_strings.tokenSecret, algorithm='HS256').decode('utf-8')
	# token = jwt.encode({'userid': user.id}, 'secret', algorithm='HS256').decode('utf-8')

	# response = {
	# 	'token': token.decode('utf-8')
	# }

def decode(token):
# def decodeToken(token):
	try:
		payload = jwt.decode(token.encode('utf-8'), configuration_strings.tokenSecret, algorithms=['HS256'])
	except jwt.exceptions.DecodeError:
		print('failed decode')
		payload = None

	return payload