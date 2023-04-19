#Copyright (c) 2023 tanuking
#This software is released under the MIT License, see LICENSE.
import numpy as np
from generater.abstract_generater import AbstractGenerater
from model.hp import LearningRates, ValueLogic

class LRSearchGenerater(AbstractGenerater):

	def __init__(self):
		super().__init__(n_gen_max=len(LearningRates.values()))
		self.count = 0

	def put(self, next_trial_id, param_history, id_obj_dict):
		return

	def func(self, hp, smaller, bigger):
		if LearningRates.is_lr_name(hp.name):
			val = LearningRates.values()[self.count]
			self.count += 1
			return ValueLogic.to_calc_val(hp, val)
		return ValueLogic.to_calc_val(hp, hp.initial)

	def set_lr_range(self, objectives):
		objs = [objectives.get(t_id) for t_id in self.processed_ids]
		best_diff = 0
		best_lr_idx = 0
		for i in range(1, len(objs)):
			diff = objs[i] - objs[i-1]
			if diff < best_diff:
				best_diff = diff
				best_lr_idx = i

		print(best_lr_idx)
		learning_rates = LearningRates.values()
		#最後だった場合
		if best_lr_idx == len(learning_rates)-1:
			LearningRates.search_range = (learning_rates[-2], learning_rates[-1])
		else:
			LearningRates.search_range = (learning_rates[best_lr_idx -1], learning_rates[best_lr_idx + 1])
		'''
		elif learning_rates[best_lr_idx] < learning_rates[best_lr_idx+1]:
			LearningRates.search_range = (learning_rates[best_lr_idx-1], learning_rates[best_lr_idx])
			print("b", (learning_rates[best_lr_idx-1], learning_rates[best_lr_idx]))
		else:
			LearningRates.search_range = (learning_rates[best_lr_idx - 1], learning_rates[best_lr_idx + 1])
			print("c",  (learning_rates[best_lr_idx - 1], learning_rates[best_lr_idx + 1]))
		'''