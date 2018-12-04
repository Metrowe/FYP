import sys

# Throws an error with specified message and exits the program
def manualThrow(errorMessage):
	formattedErrorMessage = "ERROR: " + errorMessage
	sys.exit(formattedErrorMessage)