#Copyright (c) 2023 tanuking
#This software is released under the MIT License, see LICENSE.

class PastParams():
	def __init__(self):
		self.history = {}

	def get(self, trial_id):
		return self.history[trial_id].copy()

	def put(self, trial_id, param):
		self.history[trial_id] = param