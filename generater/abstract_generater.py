#Copyright (c) 2023 tanuking
#This software is released under the MIT License, see LICENSE.
from abc import ABC, ABCMeta, abstractmethod
from model.hp import HpList, ValueLogic
from model.params import Params

class  AbstractGenerater(metaclass = ABCMeta):
	def __init__(self, n_gen_max):
		self.n_gen_max = n_gen_max
		self.n_gen = 0
		self.processed_ids = []

	def is_finished(self):
		return self.n_gen >= self.n_gen_max

	def generate(self, trial_id):
		p = Params()
		for hp in HpList.get():
			value = ValueLogic.calc(hp, self.func)
			value = min(max(value, hp.lower), hp.upper)
			p.put(hp.name, value)
		self.processed_ids.append(trial_id)
		self.n_gen += 1
		return p

	@abstractmethod
	def put(self, next_trial_id, past_params, objs):
		pass

	@abstractmethod
	def func(self, hp, smaller, bigger):
		pass
