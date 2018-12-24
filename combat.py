import sys
from math import inf, sqrt
from heapq import heappop, heappush

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

	## Elements : Fire = F / Ice = I / Wind = W / Lightning = L

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

	k.gain_xp(4050)

	return


if __name__ == '__main__':
	main()
