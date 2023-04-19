#Copyright (c) 2023 tanuking
#This software is released under the MIT License, see LICENSE.
import numpy as np
from generater.abstract_generater import AbstractGenerater
from model.hp import ValueLogic

class  StdGenerater(AbstractGenerater):

	def __init__(self, n_gen_max, std_ratio):
		super().__init__(n_gen_max)
		self.center_params = None
		self.std_ratio = std_ratio

	def put(self, next_trial_id, past_params, objs):
		best_trial_id = objs.get_best_id()
		self.center_params = past_params.get(best_trial_id)

	def func(self, hp, smaller, bigger):
		center = ValueLogic.to_calc_val(hp, self.center_params.get(hp.name))
		std = (bigger - smaller) * self.std_ratio
		return np.random.normal(center, std)