#Copyright (c) 2023 tanuking
#This software is released under the MIT License, see LICENSE.
import numpy as np
from generater.abstract_generater import AbstractGenerater
from model.hp import HpList, ValueLogic

class GeneticGenerater(AbstractGenerater):

	def __init__(self, n_gen_max):
		super().__init__(n_gen_max)
		self.weaker_params = [] #need to save so as not to update when best is updated
		self.child_param = None
		self.count = 0

	def put(self, next_trial_id, past_params, objs):
		if len(self.weaker_params) == 0: 
			self.weaker_params = self._get_weaker_params(past_params, objs)

		current_best_param = past_params.get(objs.get_best_id())
		self._generate_next_child(current_best_param)

	def _get_weaker_params(self, past_params, objs):
		trial_ids = objs.get_ids_sorted_by_obj()
		weaker_trial_ids = trial_ids[1:]
		return [past_params.get(trial_id) for trial_id in weaker_trial_ids]

	def _generate_next_child(self, parent_param):
		hp_num = len(HpList.get())
		while True:
			weaker = self.weaker_params[self.count // hp_num]
			update_hp = HpList.get()[self.count % hp_num]
			gene_val = weaker.get(update_hp.name)
			if parent_param.get(update_hp.name) != gene_val:
				break
			self.count += 1

		self.child_param = parent_param.copy()
		self.child_param.put(update_hp.name, gene_val)
		self.count += 1
		print("*****", update_hp.name, gene_val, self.child_param.result_form())
		
	def func(self, hp, smaller, bigger):
		return ValueLogic.to_calc_val(hp, self.child_param.get(hp.name))
