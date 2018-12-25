import sys
from math import inf, sqrt
from heapq import heappop, heappush

STACK_SIZE = 4

class Battle:

	def __init__(self, actors):
		self.energy = {}
		self.stack = []

		self.side1 = []
		self.side2 = []

		for actor,side in actors:
			if side == 1:
				self.side1.append(actor)
			else:
				self.side2.append(actor)

		for char in self.side1+self.side2:
			self.energy[char] = 0

		for i in range(STACK_SIZE):
			self.stack.append(self.next_character())

	def update_stack(self):
		turn_character = self.stack.pop(0)
		print('\n'+"It's", turn_character+"'s turn!")
		self.stack.append(self.next_character())

		self.print_stack()
		

	def next_character(self):
		trigger = False

		while(not trigger):
			for key, val in self.energy.items():
				if(val >= 10000):
					trigger = True

			for key in self.energy.keys():
				self.energy[key] += key.SPD

		actions = []
		for key, val in self.energy.items():
			if(val >= 10000):
				actions.append((key, val))

		action = max(actions, key = lambda item:item[1])[0]
		self.energy[action] = 0

		return(action.name)

	def print_stack(self):
		print("\nStack is:")
		for char in self.stack:
			print(char)




class Character:

	def __init__(self, name, HP, mHP, SP, mSP, STR, mSTR, MGI, mMGI, \
				DEX, mDEX, DEF, mDEF, RES, mRES, SPD, mSPD, element):
		self.name = name
		self.HP = HP
		self.SP = SP
		self.STR = STR
		self.MGI = MGI
		self.DEX = DEX
		self.DEF = DEF
		self.RES = RES
		self.SPD = SPD
		self.element = element


		self.bHP = HP
		self.bSP = SP
		self.bSTR = STR
		self.bMGI = MGI
		self.bDEX = DEX
		self.bDEF = DEF
		self.bRES = RES
		self.bSPD = SPD

		self.mHP = mHP
		self.mSP = mSP
		self.mSTR = mSTR
		self.mMGI = mMGI
		self.mDEX = mDEX
		self.mDEF = mDEF
		self.mRES = mRES
		self.mSPD = mSPD
		
		self.level = 1
		self.XP = 0
		self.AP = 0

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

	def print_stats(self):
		print()
		print(self.name+"'s stats are now:")
		print("HP =",int(self.HP),"	STR =",int(self.STR),"	MGI =",int(self.MGI))
		print("DEX =",int(self.DEX),"	DEF =",int(self.DEF),"	RES =",int(self.RES))
		print("SPD =",int(self.SPD))


		print('\n'+"XP:",str(self.XP)+"/100" if self.level != 90 else str(self.XP))
		print("AP:",str(self.AP))


def main():

	kiyomi = Character("Kiyomi", 1000, 40000, 300, 6500, 500, 25000, 250, 10000,\
						300, 15000, 400, 16000, 300, 12000, 350, 15000, 'L')

	kiyomi2 = Character("Kiyomi2", 1000, 40000, 300, 6500, 500, 25000, 250, 10000,\
						300, 15000, 400, 16000, 300, 12000, 550, 15000, 'L')

	kiyomi3 = Character("Kiyomi3", 1000, 40000, 300, 6500, 500, 25000, 250, 10000,\
						300, 15000, 400, 16000, 300, 12000, 700, 15000, 'L')

	battle = Battle([(kiyomi,1), (kiyomi2,1), (kiyomi3,1)])


	battle.print_stack()

	battle.update_stack()


	kiyomi.gain_xp(4050)


	return

if __name__ == '__main__':
	main()