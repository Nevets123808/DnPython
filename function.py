
import random
import ast
def Dice(number, size):
	count = 0
	for i in range(number):
		count += random.randint(1,size)
	print("rolled ", number,"d",size, " = ", count)
	return count

def LoadDict(fileName):
	with open(fileName,"r") as file:
		dict = ast.literal_eval(file.read())
	return dict
#This gives us a way of rolling a d20 normally, or with advantage/disadvantage)
def SkillRoll(advantage):

	#always roll 2 dice
	dice1 = Dice(1,20)
	dice2 = Dice(1,20)

	#choose dice based on the state of advantage 
	if ( (advantage < 0 and dice1>dice2) or (advantage > 0 and dice1<dice2) ):
		roll = dice2
	else:
		roll = dice1
	return(roll)


#in skillchecks, "mod" is for any generic modifier, this includes proficiency, but can
#also include spell effects such as guidance, etc. As skill checks are simply pass/fail
#the result can be a boolean.
def SkillCheck(abMod, difficulty, mod=0, advantage = 0):
	roll = SkillRoll(advantage)+abMod+mod
	return(roll >= difficulty)

#An attack roll has 4 different results: critical miss, miss, hit and critical hit.
#A critical miss (natural 1) is a miss regardless of the opposing AC
#on a natural 20, it is an automatic hit, unless the roll exceeds the AC, in which
#case the hit is counted as a critical hit.
def AttackRoll(hitMod, AC, advantage = 0):
	#this is the natural roll of the dice used, including advantage.
	roll = SkillRoll(advantage)
	score = roll + hitMod
	#Handle critical misses
	if roll==1: return "MISS"
	elif (roll == 20 and score >= AC): return "CRITICAL"
	elif (roll == 20 or score >= AC): return "HIT"
	else: return "MISS"

#This is the damage handler
def Damage(diceNum, damDice, mod = 0, resist = False):
	score = Dice(diceNum, damDice) + mod
	if resist: score = math.floor(score/2)
	return score

#This is the attack handler
#hitMod and damMod represent any modifiers that aren't covered by ability score or proficiency 
def Attack(attacker, defender, hitMod = 0, advantage = 0, damMod = 0, resist = False):
	weapon = attacker.weapon
	print(attacker.name, " attacks ", defender.name, " with ", weapon.name,".")
	text = str(attacker.name)+ " attacks " + str(defender.name) + " with "+ str(weapon.name)
	attackMod = attacker.strMod + hitMod
	attack = AttackRoll(attackMod, defender.AC, advantage)
	print ("attack roll = ", attack)
	if attack == "CRITICAL":
		damage = Damage(2*weapon.diceNum, weapon.damDice, damMod, resist)
		print("Critical hit! ", damage, " damage.")
		text = text +" Critical hit! "+ str(damage)+ " damage."
	elif attack == "HIT":
		damage = Damage(weapon.diceNum, weapon.damDice,damMod,resist)
		print("Hit for ", damage, " damage.")
		text = text+" Hit for "+ str(damage)+ " damage."
	else:
		damage = 0
		print(attacker.name, " misses.")
		text = text + " " +str(attacker.name)+ " misses."

	defender.HP -= damage
	if (defender.HP <= 0):
		defender.alive = False
	return [attack, damage, text]

def addPos(vector1, vector2):
	return([vector1[0]+vector2[0], vector1[1]+vector2[1]])

def subPos(vector1, vector2):
	return ([vector1[0]-vector2[0], vector1[1] - vector2[1]])
def main():
	for i in range(100):
		SkillRoll(0)
		print("\n")

if __name__ == "__main__":
	main()

