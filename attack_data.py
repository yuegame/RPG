import sys
import csv

class Attack:

	def __init__(self, data):
		self.name = data[0]
		self.speed = data[1]
		self.target = data[2]
		self.turn = data[3]
		self.mod = data[4]
		self.damage = data[5]
		self.type = data[6]
		self.desc = data[7]

	def deal_damage(self, source, target_list):
		for target in target_list:
			target.HP = target.HP - (self.damage*self.modifier(source,target))
			print(source.name,"dealt",str(self.damage),"damage to",target.name, "with",self.name+'!')

	def modifier(self, source, target):
		# Used in elemental modification, to be enabled after writing more data for enemies like weakness
		return 1

		if(self.type == "physical"):
			# DO ARMOR THINGS HERE
			pass
		elif(self.type == target.weakness):
			return 1.5

	def apply_buff(self, source, target_list):
		for target in target_list:
			if("Recover" in self.name):
				target.HP = target.HP + self.damage
				print(source.name,"healed",str(self.damage),"health to",target.name, "with",self.name+'!')
		pass

	# Called by battle, resolves attacks in attack specific ways
	def resolve_attack(self, source, target_list):
			if(self.type == "physical" or self.type == "magic"):
				self.deal_damage(source, target_list)
			if(self.type == "buff"):
				self.apply_buff(source, target_list)

			

	# Print functions
	def print_attack(self):
		print(self.name,self.speed,self.target,self.turn,self.mod,self.damage,self.desc)