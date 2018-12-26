import sys
import csv
import copy
from math import inf, sqrt
from heapq import heappop, heappush
from attack_data import Attack

STACK_SIZE = 10

class Battle:

	def __init__(self, actors):
		self.counter = {}
		#self.stack = []

		self.side1 = []
		self.side2 = []

		for actor,side in actors:
			if side == 1:
				self.side1.append(actor)
			else:
				self.side2.append(actor)

		for char in self.side1+self.side2:
			self.counter[char] = 100-char.SPD

	# Battle control flow functions
	def battle_start(self):
		while(self.battle_ended() is False):
			self.update_counter()

	def battle_ended(self):
		if(len(self.side1) > 0  and len(self.side2) > 0):
			return False
		if(len(self.side1) == 0):
			print('\n'+"Side 2 wins!")
		elif(len(self.side2) == 0):
			print('\n'+"Side 1 wins!")
		return True

    # Begins next turn
	def update_counter(self):
		turn_character = self.next_character()
		print('\n'+"It's", turn_character.name+"'s turn!")
		
		self.take_turn(turn_character)
		self.print_counter()

	# Picks next character to go and updates counters
	def next_character(self):
		trigger = False

		while(True):
			for key, val in self.counter.items():
				if(val <= 0):
					trigger = True
					turn_character = key
			if(trigger):
				break
			for key in self.counter.keys():
				self.counter[key] -= 1

		self.counter[turn_character] = 100-turn_character.SPD

		return(turn_character)

	# Choose attack
	def take_turn(self, character):
		options_list = []
		for attack in character.attacks:
			options_list.append(attack)

		index = 1
		option_display = ""
		for option in options_list:
			if("Attack" in str(type(option))):
				option_display = option_display+str(index)+'.'+option.name+"     "
				index += 1
		print(option_display)

		choice = input("\nEnter a move: ")

		self.execute_attack(options_list[int(choice)-1], character)
		
	# Figures out targets for attack
	def execute_attack(self, attack, source):
		if(attack.target == "ST"):
			targets = []
			if(source in self.side1):
				for character in self.side2 if attack.type != "buff" else self.side1:
					targets.append(character)
			elif(source in self.side2):
				for character in self.side1 if attack.type != "buff" else self.side1:
					targets.append(character)

			index = 1
			target_display = ""
			for target in targets:
				target_display = target_display+str(index)+'.'+target.name+"     "
			print(target_display)

			choice = input("\nPick a target: ")
			chosen_target = targets[int(choice)-1]

			attack.resolve_attack(source, [chosen_target])

		elif(attack.target == "AoE"):
			targets = []
			if(source in self.side1):
				for character in self.side2:
					targets.append(character)
			elif(source in self.side2):
				for character in self.side1:
					targets.append(character)

			attack.resolve_attack(source, targets)

		self.end_attack()

	# Finish turn
	def end_attack(self):

		for char in self.side1+self.side2:
			if(char.HP <= 0):
				self.counter.pop(char)
				if(char in self.side1):
					self.side1.remove(char)
				else:
					self.side2.remove(char)

		self.print_status()

	# Print functions

	def print_counter(self):
		print("\nCharacter           Time Remaining")
		print("___________         _______________")

		for key,val in self.counter.items():
			spaces = ""
			for i in range(0,20-len(key.name)):
				spaces = spaces + ' '
			print(key.name+spaces+str(val))

	def print_status(self):
		print('\n'+"*******Side 1*******")
		for char in self.side1:
			char.print_stats()

		print('\n'+"*******Side 2*******")
		for char in self.side2:
			char.print_stats()


class Character:

	#format = name, HP, mHP, SP, mSP, STR, mSTR, MGI, mMGI, DEX, mDEX, DEF, mDEF, RES, mRES, SPD, mSPD, element

	def __init__(self, data):
		self.name = data[0]
		self.HP = data[1]
		self.SP = data[3]
		self.STR = data[5]
		self.MGI = data[7]
		self.DEX = data[9]
		self.DEF = data[11]
		self.RES = data[13]
		self.SPD = data[15]
		self.element = data[17]


		self.bHP = self.HP
		self.bSP = self.SP
		self.bSTR = self.STR
		self.bMGI = self.MGI
		self.bDEX = self.DEX
		self.bDEF = self.DEF
		self.bRES = self.RES
		self.bSPD = self.SPD

		self.mHP = data[2]
		self.mSP = data[4]
		self.mSTR = data[6]
		self.mMGI = data[8]
		self.mDEX = data[10]
		self.mDEF = data[12]
		self.mRES = data[14]
		self.mSPD = data[16]

		self.attacks = []

		self.level = 1
		self.XP = 0
		self.AP = 0

	# Adds attacks to a character given a list of strings and attacks
	def add_attack(self, data_list, attack_list):
		for attack_to_add in data_list:
			for each_attack in attack_list:
				if(each_attack.name == attack_to_add):
					attack = each_attack
			self.attacks.append(attack)

	def stat_update(self):
		level_gained = 0

		while(self.XP >= 100 and self.level+level_gained <= 89):
			self.XP -= 100
			level_gained += 1

		if(level_gained != 0):
			self.level += level_gained
			print('\n'+self.name,"is now level",str(self.level)+'!')

		self.HP = self.HP + level_gained*((self.mHP - self.bHP)/89)
		self.SP = self.SP + level_gained*((self.mSP - self.bSP)/89)
		self.STR = self.STR + level_gained*((self.mSTR - self.bSTR)/89)
		self.MGI = self.MGI + level_gained*((self.mMGI - self.bMGI)/89)
		self.DEX = self.DEX + level_gained*((self.mDEX - self.bDEX)/89)
		self.DEF = self.DEF + level_gained*((self.mDEF - self.bDEF)/89)
		self.RES = self.RES + level_gained*((self.mRES - self.bRES)/89)
		self.SPD = self.SPD + level_gained*((self.mSPD - self.bSPD)/90)

		self.print_stats()

	def gain_xp(self, xp_gain):
		self.XP += xp_gain
		self.stat_update()

	# Print functions	

	def print_stats(self):
		print()
		print(self.name+":")
		print("________________________________________")
		print("HP =",int(self.HP),"	STR =",int(self.STR),"	MGI =",int(self.MGI))
		print("DEX =",int(self.DEX),"	DEF =",int(self.DEF),"	RES =",int(self.RES))
		print("SPD =",int(self.SPD))


		print('\n'+"XP:",str(self.XP)+"/100" if self.level != 90 else str(self.XP))
		print("AP:",str(self.AP))

	def print_attacks(self):
		print('\n'+self.name+"'s attacks are:")
		for attack in self.attacks:
			attack.print_attack()

	def print_simple_attacks(self):
		print('\n'+self.name+"'s attacks are:")
		for attack in self.attacks:
			print(attack.name+':',attack.desc)

def new_character(name, char_list):
	new_char = None
	for character in char_list:
		if(character.name == name):
			new_char = copy.deepcopy(character)
	if(new_char	is None):
		print("Invalid character initialization!")

	return new_char

def main():

	attack_list = []

	character_list = []
	## Elements : Fire = F / Ice = I / Wind = W / Lightning = L

	# Load character data

	with open("character_info.csv") as char_info_file:
		info = csv.reader(char_info_file, delimiter = ',')
		info.__next__()
		for data_line in info:
			for i in range(1, len(data_line)-1):
				data_line[i] = int(data_line[i])
			character_list.append(Character(data_line))

	# Load attack data
	with open('attack_info.csv') as attack_info_file:
		info = csv.reader(attack_info_file, delimiter = ',')
		info.__next__()
		for row in info:
			row[5] = int(row[5])
			attack_list.append(Attack(row))


	# Initialize characters
	kiyomi = new_character("Kiyomi", character_list)
	airi = new_character("Airi", character_list)
	ayame = new_character("Ayame", character_list)

	# Give attacks to characters
	kiyomi_attacks = ["Cut", "Slice", "Recover"]
	kiyomi.add_attack(kiyomi_attacks, attack_list)
	airi_attacks = ["Cut", "Slice", "Recover"]
	airi.add_attack(airi_attacks, attack_list)
	ayame_attacks = ["Cut", "Slice"]
	ayame.add_attack(ayame_attacks, attack_list)

	kiyomi.print_simple_attacks()
	airi.print_simple_attacks()
	ayame.print_simple_attacks()

	#airi.print_stats()
	#airi.print_attacks()

	"""
	k = Character("Kiyomi",		120, 600, 70, 350, \
                    			5, 80, 3, 68, \
				     			4, 74, 3, 68, \
                            	3, 74, 4, 74, 'L')

	ai = Character("Airi",		120, 600, 80, 400, \
                    			4, 74, 4, 74, \
				     			3, 68, 3, 68, \
                            	2, 64, 4, 78, 'W')

	s = Character("Shinji", 	100, 500, 60, 300, \
                    			2, 62, 1, 56, \
				     			3, 68, 2, 62, \
                            	5, 80, 5, 90, 'N')

	aya = Character("Ayame", 	150, 750, 55, 275, \
                    			6, 86, 2, 62, \
				     			4, 82, 2, 62, \
                            	1, 56, 2, 62, 'F')
    """

    # Begin battle
	battle = Battle([(kiyomi,2), (airi,1), (ayame,2)])


	battle.print_counter()

	battle.battle_start()

	"""

	r = Character("Rika", 		100, 500, 90, 450, \
                    			1, 56, 5, 80, \
				     			2, 62, 4, 74, \
                            	3, 74, 3, 68, 'I')

	y = Character("Yuki",	 	100, 500, 80, 400, \
                    			2, 62, 3, 68, \
				     			2, 62, 5, 80, \
                            	4, 78, 3, 71, 'N')

	h = Character("Hiro", 		120, 600, 80, 400, \
                    			3, 68, 4, 74, \
				     			3, 68, 4, 74, \
                            	5, 80, 4, 82, 'N')

	t = Character("Tamiko", 	120, 600, 70, 350, \
                    			3, 68, 2, 62, \
				     			5, 90, 4, 74, \
                            	3, 68, 3, 68, 'N')
    """


	return


if __name__ == '__main__':
	main()
