import requests
from ExpLib import ExpList
import argparse

#Init Global Variables
AvailableEXP = []
TargetURL = ""
ExpVersion = ""
HTTPMethod = ""
AttackVector = ""

def initAvailableExp():
	for exp in ExpList:
		AvailableEXP.append(exp.upper())
'''
def PoC_GET(TargetURL, ExpVersion):
	result = requests.get(TargetURL+ExpList[ExpVersion]["PoC"]).content.decode("utf-8").strip()
	return result

def exploit(TargetURL, ExpVersion, HTTPMethod):
	print("Testing PoC...")
	print(PoC_GET(TargetURL,ExpVersion))
'''

#Initialise Exploit Database
initAvailableExp()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Automated Struts2 Exploit Set")
	parser.add_argument("-u","--url", help="Target Vulnerable URL", required=True)
	parser.add_argument("-m","--method", help="HTTP Method: [GET / POST]. Leave this field Blank will default to GET")
	parser.add_argument("-o","--option", help="[POC: Proof Of Concept / CMD : Command Execution / UP: File Upload]", required=True)
	#*Exploit can be set to non-compulsory later on
	parser.add_argument("-e","--exploit", help="Exploit Version Choice", required=True)
	args = vars(parser.parse_args())
	if "http://" not in args["url"]:
		TargetURL = "http://" + args["url"]
	else:
		TargetURL = args["url"]
	#Check if argument "Method" has been set, defaults to GET Method
	if args["method"] == None or args["method"] == "GET":
		HTTPMethod = "GET"
	elif args["method"].upper() == "POST":
		HTTPMethod = "POST"
	else:
		print("HTTP Method not Supported. Use GET or POST")
		exit()
	if args["exploit"].upper() in AvailableEXP:
		ExpVersion = args["exploit"].upper()
	else:
		print("Exploit not found in database!")
		exit()

	if args["option"].upper() == "POC":
		AttackVector = "POC"
	elif args["option"].upper() == "CMD":
		AttackVector = "CMD"
	elif args["option"].upper() == "FILEUPLOAD":
		AttackVector = "FILEUPLOAD"
	else:
		print("Available Options are 'POC', 'CMD', and 'UP'.")
		exit()

	print("All Set:\n\tTarget URL:\t%s\n\tHTTP Method:\t%s\n\tExploit:\t%s\n\tAttack Vector:\t%s" %(TargetURL,HTTPMethod,ExpVersion,AttackVector))
