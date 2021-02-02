import function

# basic ability class
class Ability:
	def __init__(self,name, user, range):
		self.user = user
		self.name = name
		self.range = range
		#This will be used as a marker for an ability being used. It will also be used to "interrupt" abilities. I.e. Counterspell
		self.active = False
		pass

	def Use(self,target):
		#set ability toa"ctive"
		self.active = True
		log_text = None
		#check target is within range (this might be handled elswhere in later versions)
		#if self.range <= self.checkRange(target):
		# check whether any reactions occur from the ability's use.
		self.checkReaction(target,"Used")
		# this check is simply to see if the ability has been interrupted
		if self.active:
			log_text = self.Effect(target)
		# do we need another reaction check?
		self.checkReaction(target, "After")
		return log_text
	def checkRange(self, target):
		dx = self.user.pos[0] - target.pos[0]
		dy = self.user.pos[1] - target.pos[1]
		print ("range =", abs(dx+dy))
		return abs(dx + dy)

	def checkReaction(self,target, name):
		pass

	def Effect(self,target):
		pass

class Attack(Ability):
	def __init__ (self, user):
		self.weapon = user.weapon
		super().__init__("Attack",user,self.weapon.range)

	def Effect(self,target):
		return function.Attack(self.user, target)[2]
