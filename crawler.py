import utils, time, multiprocessing, sys, random

class crawler:
	def __init__(self, copy=[]):
		self.creationFlag = False
		self.stopped = False
		self.path = ""

		self.code = "[" + chr(random.randint(65, 90)) + str(random.randint(10000, 99999)) + "]"

		try:
			if copy == []:
				self.crawlSize = abs(int(input("\n\tCrawler depth: ")))
				self.startingPoint = input("\n\tStarting point [URL]: ")

				print(utils.colorPrint("\n\tNew crawler created", utils.bcolors.GREEN))
				self.creationFlag = True
			
			else:
				self.crawlSize = copy[0]
				self.startingPoint = copy[1]
				self.creationFlag = True

		except(ValueError):
			print(utils.colorPrint("\n\tError: value error", utils.bcolors.RED))

		except(KeyboardInterrupt):
			print() # Needed space
			print(utils.colorPrint("\n\tCancelled", utils.bcolors.RED))

		except(EOFError):
			print(utils.colorPrint("\n\tCancelled", utils.bcolors.RED))

	def __str__(self) -> str:
		if self.stopped:
			returnString =  utils.colorPrint("\n\tcrawler " + self.code, utils.bcolors.RED)
		
		else:
			returnString =  utils.colorPrint("\n\tcrawler " + self.code, utils.bcolors.GREEN)

		if self.path != "":
			returnString += ": " + self.path

		return returnString
	
	def genCopy(self):
		return [self.crawlSize, self.startingPoint]

	def crawl(self):
		crawlUrl = self.startingPoint

		if self.path == "":
			self.path += utils.getSite(self.startingPoint)
		
		else:
			self.path += " -> " + utils.getSite(self.startingPoint)

		if not self.stopped:
			for _ in range(self.crawlSize):
				crawlSite = utils.getSite(crawlUrl)
				crawlUrl = utils.getNext(crawlUrl)

				if crawlUrl == "stopCrawling":
					self.stopped = True
					break

				self.path += " -> " + crawlSite
			
			self.startingPoint = crawlUrl
		
		return self

def singleCrawl(singleCrawler: crawler) -> None:
	singleCrawler.crawl()

def multiCrawl(crawlers: list, sdOptions=[], ddOptions=[]):

	# ACTIVATES CRAWLERS

	# DEFAULTS

	parallelFlag = False
	updatedCrawlers = crawlers

	for opts in ddOptions:
		if opts == "--parallel":
			if "linux" not in sys.platform: # parallel computing only available on linux
				print(utils.colorPrint("\n\tError: feature not available on this platform yet", utils.bcolors.RED))

			else:
				parallelFlag = True

	computeStart = time.time()

	print(utils.colorPrint("\n\tCrawling", utils.bcolors.GREEN))

	try:

		if parallelFlag:

			# PARALLEL COMPUTING

			print(utils.colorPrint("\tUsing parallel computing", utils.bcolors.GREEN))
			workers = min([len(crawlers), multiprocessing.cpu_count()])

			with multiprocessing.Pool(workers) as parallelPool: # automatic selection of processes count
				updatedCrawlers = parallelPool.map(singleCrawl, [singleCrawler for singleCrawler in crawlers], chunksize=int(len(crawlers) / workers))
				computeEnd = time.time()
				parallelPool.close()
		
		else:

			# "SINGLE CORE" COMPUTING

			for singleCrawler in crawlers:
				singleCrawler.crawl()

			computeEnd = time.time()
			
		print(utils.colorPrint("\tDone, elapsed time: " + str(round(computeEnd - computeStart, 4)) + " seconds", utils.bcolors.GREEN))
	
	except(KeyboardInterrupt):
		computeEnd = time.time()
		print() # needed space
		print(utils.colorPrint("\tStopped, elapsed time: " + str(round(computeEnd - computeStart, 4)) + " seconds", utils.bcolors.RED))

	except(EOFError):
		computeEnd = time.time()
		print(utils.colorPrint("\tStopped, elapsed time: " + str(round(computeEnd - computeStart, 4)) + " seconds", utils.bcolors.RED))

	return updatedCrawlers