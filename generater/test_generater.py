#Copyright (c) 2023 tanuking
#This software is released under the MIT License, see LICENSE.
import numpy as np
from generater.abstract_generater import AbstractGenerater

class  TestGenerater(AbstractGenerater):

	def put(self, next_trial_id, param_history, id_obj_dict):
		return

	def func(self, hp, smaller, bigger):
		return np.random.normal(3, 0.1)
