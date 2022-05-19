import crawler, utils

class node:
	def __init__(self, name: str, start=False):
		self.name = name
		self.start = start
		self.weight = 1
		self.children = []

	def __str__(self, depth=0):
		if depth == 0 or len(self.children) == 0:
			return self.name

		returnString = self.name

		childrens = ["\n" + "\t" * (depth + 1) + "[" + str(child.weight) + "] " + child.__str__(depth + 1) for child in self.children]

		for child in childrens:
			returnString += child

		return returnString

	def addChildren(self, parent: str, newChild: str):
		for child in self.children:
			if str(child) == newChild:
				child.weight += 1
				return None

		if str(self) == parent:
			self.children.append(node(newChild))
			self.reorder()
			return None
		
		for child in self.children:
			child.addChildren(parent, newChild)
			self.reorder()

	def reorder(self):
		for i in range(len(self.children)):
			for j in range(i, len(self.children)):
				if str(self.children[i]) > str(self.children[j]):
					self.children[i], self.children[j] = self.children[j], self.children[i]

def makeMap(crawlersList: list) -> node:
	submap = None

	for crawler in crawlersList:
		for siteIndex in range(len(crawler.pathList)):
			if submap == None:
				submap = node(crawler.pathList[siteIndex], True)
				continue

			try:
				submap.addChildren(crawler.pathList[siteIndex], crawler.pathList[siteIndex + 1])

			except(IndexError):
				continue

	return submap