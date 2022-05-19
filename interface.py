import os, sys

import crawler
import utils
import submap

print(utils.colorPrint("webCrawler", utils.bcolors.BLUE))
print(utils.colorPrint("A utility with CLI written in Python to create submaps of the internet starting from a single website", utils.bcolors.BLUE))
print(utils.colorPrint("Developed by Andrea Di Antonio", utils.bcolors.BLUE))
print(utils.colorPrint("\nType \'help\' if needed", utils.bcolors.BLUE))

try:
	if not os.path.exists(str(os.getcwd()) + "/data"):
		os.makedirs(str(os.getcwd()) + "/data")
	
except:
	print(utils.colorPrint("\n\tError: couldn't create \'data\' folder\n\tExited\n", utils.bcolors.RED))
	sys.exit(-1)

try:
	user = os.getlogin()

	if user == "":
		user = "user"

except:
	user = "user"

crawlers = []
smap = None

# INTERFACE, USES A SIMILAR INTERFACE TO NBODY

while True: # Interface
	hostName = "webCrawler"

	if len(crawlers) != 0:
		hostName += "+" + str(len(crawlers))

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

		# LIST CRAWLERS
		
		elif instructions[0] == "list":
			if len(crawlers) == 0:
				print(utils.colorPrint("\n\tError: not enough crawlers", utils.bcolors.RED))
				continue

			for c in crawlers:
				print(utils.colorPrint(str(c), utils.bcolors.BLUE))
			
			continue

		# CLEAR CRAWLERS

		elif instructions[0] == "clear":
			crawlers = []
			print(utils.colorPrint("\n\tCleared crawlers list", utils.bcolors.GREEN))
			continue

		# CREATE A NEW CRAWLER
	
		elif instructions[0] == "new":
			crawlersNumber = 1

			for opts in sdOpts:
				if opts[0] == "-n": # output file
					try:
						crawlersNumber = abs(int(opts[1]))
					
					except:
						pass

			newCrawler = crawler.crawler()

			if newCrawler.creationFlag:
				crawlers.append(newCrawler)

				if crawlersNumber > 1:
					for _ in range(crawlersNumber - 1):
						crawlers.append(crawler.crawler(newCrawler.genCopy()))
					
					print(utils.colorPrint("\t" + str(crawlersNumber - 1) + " new other crawlers created", utils.bcolors.GREEN))
			continue

		# DUMP BODIES AND ORBITS LIST TO A .pck FILE
		
		elif instructions[0] == "dump":
			utils.dump(crawlers, sdOptions=sdOpts) # dumps to a .pck file
			continue

		# LOAD BODIES AND ORBITS LIST FROM A .pck OR BODIES LIST FROM A .csv FILE

		elif instructions[0] == "load":
			loadContent, loadExt = utils.load(sdOptions=sdOpts, ddOptions=ddOpts, noneObject=[])

			# LOADS .pck

			if loadExt == ".pck":
				crawlers = loadContent
				loadColor = utils.bcolors.GREEN
			
			if len(crawlers) > 0:
				print(utils.colorPrint("\tLoaded " + str(len(crawlers)) + " crawlers", loadColor))

			continue

		# ACTIVATES CRAWLERS

		elif instructions[0] == "crawl":
			if len(crawlers) == 0:
				print(utils.colorPrint("\n\tError: not enough crawlers", utils.bcolors.RED))
				continue
			
			crawlers = crawler.multiCrawl(crawlers, sdOptions=sdOpts, ddOptions=ddOpts)
			continue
	
		# CREATES SUBMAP

		elif instructions[0] == "map":
			if len(crawlers) == 0:
				print(utils.colorPrint("\n\tError: not enough crawlers", utils.bcolors.RED))
				continue
			
			smap = submap.makeMap(crawlers)
			print(utils.colorPrint("\n\tMap succesfully generated", utils.bcolors.GREEN))
			continue

		# SHOWS MAP

		elif instructions[0] == "plot":
			if smap == None:
				print(utils.colorPrint("\n\tError: no map to show", utils.bcolors.RED))
				continue
			
			print(utils.colorPrint("\n\tWeb submap starting from: " + str(smap), utils.bcolors.GREEN))
			print("\n\t" + smap.__str__(1))
			continue

	print(utils.colorPrint("\n\tError: syntax error", utils.bcolors.RED))