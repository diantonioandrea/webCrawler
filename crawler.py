import utils

class crawler:
	def __init__(self, cSize: int, sPoint: str):
		self.crawlSize = cSize
		self.startingPoint = sPoint
		self.stopped = False

	def __str__(self) -> str:
		returnString =  "crawler: " + utils.getSite(self.startingPoint)

		if self.stopped:
			returnString += ", stopped"

		else:
			returnString +=  + " -> " + str(self.crawlSize)

		return returnString

	def crawl(self) -> dict:
		crawlResult = {}
		crawlUrl = self.startingPoint

		if self.stopped:
			return {}

		for _ in range(self.crawlSize):
			crawlResult = utils.updateDict(crawlResult, utils.getSite(crawlUrl))
			crawlUrl = utils.getNext(crawlUrl)

			if crawlUrl == "stopCrawling":
				self.stopped = True
				break
		
		if not self.stopped:
			self.startingPoint = crawlUrl

		return crawlResult