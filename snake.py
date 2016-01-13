from tkinter import *
from random import choice

l = "Left"
r = "Right"
u = "Up"
d = "Down"

class SnakeLink:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.next = None
		self.prev = None

class SnakeLinks:
	def __init__(self):
		self.size = 0
		self.head = None
		self.tail = None

	def moveHead(self, link):
		assert type(link) == SnakeLink
		if self.size == 0:
			self.head = link
			self.tail = link
			link.next = self
			link.prev = self
		else:
			link.next = self.head
			link.prev = self
			self.head.prev = link
			self.head = link
		self.size += 1

	def popTail(self):
		assert self.size > 0
		x = self.tail.x
		y = self.tail.y
		if self.size == 1:
			self.head = None
			self.tail = None
		else:
			self.tail = self.tail.prev
			self.tail.next = self.tail
		self.size -= 1
		return x, y

	def eatHere(self, x, y):
		self.moveHead(SnakeLink(x, y))

	def moveHere(self, x, y):
		self.moveHead(SnakeLink(x, y))
		return self.popTail()

	def getHeadLocation(self):
		return [self.head.x, self.head.y]

	def getTailLocation(self):
		return [self.tail.x, self.tail.y]



class game:
	def __init__(self, boardSizeX=15, boardSizeY=15, safety=False):
		self.root = Tk()
		self.sizeX = max(boardSizeX, 5)
		self.sizeY = max(boardSizeY, 5)
		self.factor = 20
		self.running = False
		self.score = 0
		self.grid = [[False for _ in range(self.sizeY)] for _ in range(self.sizeX)]
		self.snake = SnakeLinks()
		self.foodX = None
		self.foodY = None
		self.LEFT = True
		self.RIGHT = False
		self.UP = False
		self.DOWN = False
		self.count = 0
		self.inverseSpeed = 10
		self.lastMove = ""
		self.safety = safety

		self.console = Frame(bg="grey")
		self.console.pack()

		self.scoreBoard = Label(self.console, text="Score: " + str(self.score), fg="black", bg="grey")
		self.scoreBoard.pack(side="top")

		self.board = Canvas(self.console, bg="black",width=self.factor*self.sizeX, height=self.factor*self.sizeY)
		self.board.pack(side="top")

		self.root.bind("<Key>", self.handler)

		self.entry = Entry(self.console)
		self.entry.pack(side="top")

		self.startButton = Button(self.console, text="Start", command=self.start, bg="grey", fg="white")
		self.startButton.pack(side="left")

		self.quitButton = Button(self.console, text="Quit", command=self.root.destroy, bg="grey", fg="white")
		self.quitButton.pack(side="right")

		self.leaveButton = Button(self.console, text="Leave", command=self.runningOff, bg="grey", fg="white")
		self.leaveButton.pack(side="right")

		self.root.lift()
		self.root.mainloop()

	def handler(self, event):
		#Prioritizes left
		key = event.keysym
		tempL = False
		tempR = False
		tempU = False
		tempD = False
		if key == l and not self.lastMove == r:
			tempL = True
		elif key == r and not self.lastMove == l:
			tempR = True
		elif key == u and not self.lastMove == d:
			tempU = True
		elif key == d and not self.lastMove == u:
			tempD = True
		else:
			return
		self.LEFT = tempL
		self.RIGHT = tempR
		self.UP = tempU
		self.DOWN = tempD

	def update(self):
		moveVector = [0, 0]
		if self.LEFT:
			moveVector[0] = -1
			self.lastMove = l
		elif self.RIGHT:
			moveVector[0] = 1
			self.lastMove = r
		elif self.UP:
			moveVector[1] = -1
			self.lastMove = u
		elif self.DOWN:
			moveVector[1] = 1
			self.lastMove = d
		oldPos = self.snake.getHeadLocation()
		newPos = [oldPos[0]+moveVector[0], oldPos[1]+moveVector[1]]
		tailPos = self.snake.getTailLocation()
		tailEqualNewHead = newPos[0] == tailPos[0] and newPos[1] == tailPos[1]
		if not tailEqualNewHead and (newPos[0] >= self.sizeX or newPos[0] < 0 or \
			newPos[1] >= self.sizeY or newPos[1] < 0 or self.grid[newPos[0]][newPos[1]]):
		    self.running = False
		elif self.foodX == newPos[0] and self.foodY == newPos[1]:
			self.score += 1
			self.foodX, self.foodY = self.newFood()
			self.grid[newPos[0]][newPos[1]] = True
			self.snake.eatHere(newPos[0], newPos[1])
			self.scoreBoard.config(text="Score: " + str(self.score))
		else:
			self.grid[newPos[0]][newPos[1]] = True
			removePos = self.snake.moveHere(newPos[0], newPos[1])
			self.grid[removePos[0]][removePos[1]] = False if not tailEqualNewHead else True


	def newFood(self):
		okay = []
		boundsX = [1, self.sizeX-1] if self.safety else [0, self.sizeX]
		boundsY = [1, self.sizeY-1] if self.safety else [0, self.sizeY]
		for x in range(boundsX[0], boundsX[1]):
			for y in range(boundsY[0], boundsY[1]):
				if not self.grid[x][y]:
					okay += [(x, y)]
		return choice(okay)

	def drawScreen(self):
		self.board.delete(ALL)
		for x in range(self.sizeX):
			for y in range(self.sizeY):
				if self.grid[x][y]:
					self.board.create_rectangle(x*self.factor, y*self.factor, (x+1)*self.factor, (y+1)*self.factor, fill="green")
		x, y = self.snake.getHeadLocation()
		self.board.create_rectangle(x*self.factor, y*self.factor, (x+1)*self.factor, (y+1)*self.factor, fill="dark green")
		self.board.create_rectangle(self.foodX*self.factor, self.foodY*self.factor, (self.foodX+1)*self.factor, (self.foodY+1)*self.factor, fill="red")

	def null(self):
		return

	def start(self):
		self.board.focus_set()
		textEntry = self.entry.get()
		self.entry.delete(0, len(textEntry))
		try:
			temp = int(textEntry)
			if temp > 1 and temp <= 50:
				self.inverseSpeed = temp
		except ValueError:
			pass
		self.running = True
		self.LEFT = True
		self.RIGHT = self.UP = self.DOWN = False
		self.lastMove = ""
		self.score = 0
		self.startButton.config(text="Running", command=self.null)
		self.scoreBoard.config(text="Score: " + str(self.score))
		self.grid[int(self.sizeX/2)][int(self.sizeY/2)] = True
		self.snake.moveHead(SnakeLink(int(self.sizeX/2), int(self.sizeY/2)))
		self.foodX, self.foodY = self.newFood()
		self.run()

	def run(self):
		if self.running:
			self.drawScreen()
			if self.count == self.inverseSpeed-1:
				self.update()
			self.count = (self.count + 1) % self.inverseSpeed
			self.root.after(5, self.run)
		else:
			self.end()

	def runningOff(self):
		self.running = False
		
	def end(self):
		self.board.delete(ALL)
		self.snake = SnakeLinks()
		self.inverseSpeed = 10
		for x in range(self.sizeX):
			for y in range(self.sizeY):	
				self.grid[x][y] = False
		self.startButton.config(text="Start", command=self.start)
		
snake = game(40, 20, True)