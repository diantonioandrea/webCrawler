# webCrawler.py

import os, sys

import crawler
import utils


print(utils.colorPrint("webCrawler", utils.bcolors.BLUE))
print(utils.colorPrint("A utility with CLI written in Python to create submaps of the internet starting from a single website", utils.bcolors.BLUE))
print(utils.colorPrint("Developed by Andrea Di Antonio", utils.bcolors.BLUE))
print(utils.colorPrint("\nType \'help\' if needed", utils.bcolors.BLUE))

try:
	user = os.getlogin()

	if user == "":
		user = "user"

except:
	user = "user"

crawlers = []

# INTERFACE, USES A SIMILAR INTERFACE TO NBODY

while True:
	hostName = "webCrawler"

	instructions, sdOpts, ddOpts = utils.getCommand("\n" + user + "@" + hostName + ": ")

	if len(instructions) > 0:

		if instructions[0] == "skip": # Ctrl+C, EOF handler
			continue

		# EXIT PROGRAM

		elif instructions[0] in ["exit", "quit"]:
			sys.exit(0)

		# HELP

		elif instructions[0] == "help":
			utils.help()
			continue