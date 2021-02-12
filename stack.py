class stack:
	def __init__(self):
		self.list = []

	class Action:
		def __init__ (self, function,actor, target, length):
			self.function = function
			self.count = length
			self.actor = actor
			self.target = target

	def createAction(self, function, actor,target, length):
		action = self.Action(function,actor,target, length)
		self.list.append(action)

	def call(self):
		item = self.list[-1]
		item.function(item.actor,item.target)
		item.count -= 1
		if item.count == 0:
			self.list.pop(-1)

def counting(number):
	print (number)
def end(number):
	print ("Blast off!")
def main():
	stack = stack()
	stack.createAction(counting,10)
	stack.createAction(end,1)
	while len(stack.list)>0:
		stack.call()

if __name__ == "__main__":
	main()
