#Copyright (c) 2023 tanuking
#This software is released under the MIT License, see LICENSE.
import numpy as np
from manager.abstruct_manager import AbstructManager

from model.hp import HpList, LearningRates
from generater.lr_search_generater import LRSearchGenerater
from generater.uniform_generater import UniformGenerater
from generater.genetic_generater import GeneticGenerater
from generater.std_generater import StdGenerater
from generater.nelder_mead_generater import NelderMeadGenerater

from generater.test_generater import TestGenerater

class Manager(AbstructManager):

	def __init__(self):
		super().__init__()

		self.generater_index = 0
		self.generaters = []
		#if HpList.has(LearningRates().names()):
		#	self.generaters.append(LRSearchGenerater())
		self.generaters.append(UniformGenerater(n_gen_max=15))
		self.generaters.append(GeneticGenerater(n_gen_max=10))
		#self.generaters.append(NelderMeadGenerater(n_gen_max=100)) 遅すぎた
		for i in range(2,20):
			self.generaters.append(StdGenerater(n_gen_max=10, std_ratio=(1 / (25 * i))))

	def get_next_generater(self):
		generater = self.generaters[self.generater_index]
		self.generater_index += 1
		return generater

	def before_generater_change(self, last_generater, objectives):
		if isinstance(last_generater, LRSearchGenerater):
			last_generater.set_lr_range(objectives)