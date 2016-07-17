import requests
from ExpLib import ExpList

#Init Global Variables
AvailableEXP = []
TargetURL = ""
ExpVersion = ""
HTTPMethod = ""

def initAvailableExp():
	for exp in ExpList:
		AvailableEXP.append(exp.upper())

def exploit(TargetURL, ExpVersion, HTTPMethod):
	pass


if __name__ == "__main__":
	

