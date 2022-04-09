import utils, random

class crawler:
	def __init__(self):
		self.creationFlag = False
		self.stopped = False
		self.path = ""

		self.code = "[" + chr(random.randint(65, 90)) + str(random.randint(10000, 99999)) + "]"

		try:
			self.crawlSize = abs(int(input("\n\tCrawler depth: ")))
			self.startingPoint = input("\n\tStarting point [URL]: ")

			print(utils.colorPrint("\n\tNew crawler created", utils.bcolors.GREEN))
			self.path += self.startingPoint
			self.creationFlag = True

		except(ValueError):
			print(utils.colorPrint("\n\tError: value error", utils.bcolors.RED))

		except(KeyboardInterrupt):
			print() # Needed space
			print(utils.colorPrint("\n\tCancelled", utils.bcolors.RED))

		except(EOFError):
			print(utils.colorPrint("\n\tCancelled", utils.bcolors.RED))

	def __str__(self) -> str:
		returnString =  "crawler " + self.code + ": " + utils.getSite(self.startingPoint)

		if self.stopped:
			returnString += ", stopped"

		else:
			returnString += " -> " + str(self.crawlSize)

		return returnString

	def crawl(self) -> dict:
		crawlResult = {}
		crawlUrl = self.startingPoint

		if self.stopped:
			return {}

		for _ in range(self.crawlSize):
			try:
				crawlResult = utils.updateDict(crawlResult, utils.getSite(crawlUrl))
				crawlUrl = utils.getNext(crawlUrl)

				if crawlUrl == "stopCrawling":
					self.stopped = True
					break

				self.path += " -> " + crawlUrl
			
			except:
				print(utils.colorPrint("\n\tCancelled: " + self.code, utils.bcolors.RED))
		
		if not self.stopped:
			self.startingPoint = crawlUrl

		return crawlResult