#Copyright (c) 2023 tanuking
#This software is released under the MIT License, see LICENSE.
from model.hp import HpList

class Params():

	def __init__(self):
		self.hp_val_dict = {} #{trial_id:{param_name:val}}

	def put(self, hp_name, val):
		self.hp_val_dict[hp_name] = val

	def get(self, hp_name):
		return self.hp_val_dict[hp_name]

	def result_form(self):
		return [{'parameter_name': hp.name, 'type': hp.type, 'value': self.hp_val_dict[hp.name]} for hp in HpList.get()]

	def copy(self):
		p = Params()
		p.hp_val_dict = self.hp_val_dict.copy()
		return p
