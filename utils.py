import requests, random, pickle, colorama
from bs4 import BeautifulSoup

# WEB

def getSource(url: str) -> str:
	try:
		return requests.get(url, "html.parser").text

	except:
		return ""

def getUrls(url: str) -> list:
	newUrls = []
	source = getSource(url)

	if source == "":
		return newUrls # Empty list

	bSoup = BeautifulSoup(source, "html.parser")
	possibleUrls = [link.get("href") for link in bSoup.find_all("a")]

	for newUrl in possibleUrls:
		try: 
			if "http" in newUrl  and url not in newUrl: # Avoids same site
				newUrls.append(newUrl)
		except:
			pass

	return newUrls

def getNext(url: str) -> str:
	urls = getUrls(url)

	if len(urls) == 0: # No urls found
		return "stopCrawling" # Stop message

	return random.choice(urls)

def getSite(url: str) -> str:
	toBeRemoved = ["https", "http", "://"]

	for string in toBeRemoved:
		url = url.replace(string, "")

	siteName = ""

	for char in url:
		if char != "/":
			siteName += char

		else:
			break
	
	return siteName

# GENERAL PURPOSE

def updateDict(oldDict: dict, key: str) -> dict:
	try:
		oldDict[key] += 1
	except:
		oldDict[key] = 1

	return oldDict

# FROM NBODY

colorama.init()
class bcolors:
	GREEN = '\033[92m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	RED = '\033[91m'
	ENDC = '\033[0m'

def colorPrint(string: str, color: str):
	return color + string + '\033[0m'

def getCommand(commandString: str) -> tuple:
	command = " ".join(input(commandString).split()).lower()
	instructions = command.split(" ")

	# OPTIONS, SINGLE DASH [[-key1, value1], ...] AND DOUBLE DASH [--key1, ...]

	try: 
		sdOpts = []
		ddOpts = []

		for inst in instructions:
			if "--" in inst:
				ddOpts.append(inst)
			
			elif "-" in inst:
				try:
					if type(float(inst)) == float: # avoids passing negative numbers as options
						pass

				except(ValueError):
					sdOpts.append([inst, instructions[instructions.index(inst) + 1]])
	
	except(IndexError):
		return [], [], []
	
	except(EOFError, KeyboardInterrupt):
		return ["skip"], [], []
		
	return instructions, sdOpts, ddOpts

def checkOptions(rOpts: list, sdOpts=[], ddOpts=[]):
	for opts in rOpts:
		if opts not in ddOpts and "--" in opts:
			print(colorPrint("\n\tError: not enough options", bcolors.RED))
			return False
	
	for opts in rOpts:
		if opts not in [col[0] for col in sdOpts] and "-" in opts and "--" not in opts:
			print(colorPrint("\n\tError: not enough options", bcolors.RED))
			return False
	
	return True

def dump(tbDumped, sdOptions=[]):
	rOptions = ["-o"]

	if not checkOptions(rOptions, sdOpts=sdOptions):
		return None

	path = "data/"

	for opts in sdOptions:
		if opts[0] == "-o": # output file
			filename = opts[1] + ".pck"

		elif opts[0] == "-p": # path
			path = opts[1]

	try:
		dumpFile = open(path + filename, "wb")
	
	except(FileNotFoundError):
		print(colorPrint("\n\tError: file or directory not found", bcolors.RED))
		return None

	pickle.dump(tbDumped, dumpFile)
	dumpFile.close()

	print(colorPrint("\n\tDumped data to file: " + filename, bcolors.GREEN))

def load(sdOptions=[], ddOptions=[], noneObject=None):
	rOptions = ["-i"]

	# DEFAULTS

	path = "data/"
	ext = ".pck"
	rMode = "rb"

	if not checkOptions(rOptions, sdOpts=sdOptions):
		return noneObject, ext

	for opts in sdOptions:
		if opts[0] == "-i": # input file
			filename = opts[1]

		elif opts[0] == "-p": # path (until folder before)
			path = opts[1]

	for opts in ddOptions:
		if opts == "--csv": # csv files
			ext = ".csv"
			rMode = "r"

	filename += ext

	try:
		loadFile = open(path + filename, rMode)
	
	except(FileNotFoundError):
		print(colorPrint("\n\tError: file or directory not found", bcolors.RED))
		return noneObject, ext

	if ext == ".pck":
		loadContent = pickle.load(loadFile)
		loadFile.close()

		print(colorPrint("\n\tLoaded data from file: " + filename, bcolors.GREEN))

	elif ext == ".csv":
		loadContent = loadFile.readlines()
		loadFile.close()

		print(colorPrint("\n\tLoaded data from file: " + filename, bcolors.GREEN))

	return loadContent, ext

def help():
	print(colorPrint("\n\twebCrawler HELP", bcolors.BLUE))

	print(colorPrint("\n\texit, quit", bcolors.BLUE))
	print("\t\tExits from program")