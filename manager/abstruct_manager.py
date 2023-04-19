#Copyright (c) 2023 tanuking
#This software is released under the MIT License, see LICENSE.
from abc import ABC, ABCMeta, abstractmethod
from model.past_params import PastParams

class AbstructManager():
	def __init__(self):
		self.generater = None
		self.past_params = PastParams()

	def put(self, next_trial_id, objectives):
		if self._need_generater_change():
			self.before_generater_change(self.generater, objectives)
			self.generater = self.get_next_generater()
		self.generater.put(next_trial_id, self.past_params, objectives)

	def generate(self, trial_id):
		params = self.generater.generate(trial_id)
		self.past_params.put(trial_id, params)
		return params.result_form()

	def _need_generater_change(self):
		if self.generater is None:
			return True
		return self.generater.is_finished()

	@abstractmethod
	def get_next_generater(self):
		pass

	@abstractmethod
	def before_generater_change(self, last_generater, objectives):
		pass