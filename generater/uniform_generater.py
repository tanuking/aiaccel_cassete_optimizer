#Copyright (c) 2023 tanuking
#This software is released under the MIT License, see LICENSE.
import numpy as np
from generater.abstract_generater import AbstractGenerater
from model.hp import LearningRates, ValueLogic

class  UniformGenerater(AbstractGenerater):

	def put(self, next_trial_id, param_history, id_obj_dict):
		return

	def func(self, hp, smaller, bigger):
		#if LearningRates.is_lr_name(hp.name):
		#	low = ValueLogic.to_calc_val(hp, LearningRates.search_range[0])
		#	high = ValueLogic.to_calc_val(hp, LearningRates.search_range[1])
		#	return np.random.uniform(low=low, high=high, size=None)
		return np.random.uniform(low=smaller, high=bigger, size=None)
