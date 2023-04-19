#Copyright (c) 2023 tanuking
#This software is released under the MIT License, see LICENSE.
import math

class Hp:
	def __init__(self, raw_hp):
		self.name = raw_hp.name
		self.upper = raw_hp.upper
		self.lower = raw_hp.lower
		self.initial = raw_hp.initial
		self.type = raw_hp.type

	def range_type(self):

		if self.is_int():
			CRITERIA = 32
			if (self.upper > (self.lower * CRITERIA)) & (self.lower != 0):
				return "log_int"
			else:
				return "normal"

		CRITERIA = 32
		if self.lower > 0:
			return "log" if self.upper / self.lower >= CRITERIA else "normal"
		elif self.upper < 0:
			return "log_minus" if self.lower / self.upper >= CRITERIA else "normal"
		elif self.lower==0: #if lower=0, see lower as initial / upper
			if self.initial is None:
				return "normal"
			return "log_zero" if ((self.upper / self.initial) >= CRITERIA) else "normal"
		elif self.upper==0: #if upper=0, see lower as initial / lower
			if self.initial is None:
				return "normal"
			return "log_zero_minus" if ((self.lower / self.initial) >= CRITERIA) else "normal"
		else:
			return "normal"

	def is_int(self):
		return self.type in ["uniform_int", "int", "INT"]

class ValueLogic:
	#計算用の値に変換(logならmath.log(val))
	@classmethod
	def to_calc_val(cls, hp, val):
		if hp.range_type()=="normal":
			return val
		elif hp.range_type()=="log":
			return math.log10(val)
		elif hp.range_type()=="log_int":
			return math.log2(val)
		elif hp.range_type()=="log_minus":
			return math.log10(-1 * val)
		elif hp.range_type()=="log_zero":
			if val == 0:
				val = hp.initial / hp.upper
			return math.log10(val)
		elif hp.range_type()=="log_zero_minus":
			if val == 0:
				val = (hp.initial / hp.lower) * -1
			return math.log10(-1 * val)
		pass

	@classmethod
	def to_real_val(cls, hp, val):
		if hp.range_type()=="normal":
			if hp.is_int(): 
				return round(val) #偶数丸め
			return val
		elif hp.range_type()=="log_int":
			return round(pow(2, val))
		elif hp.range_type()=="log":
			return pow(10, val)
		elif hp.range_type()=="log_minus":
			return -1 * pow(10, val)
		elif hp.range_type()=="log_zero":
			return pow(10, val)
		elif hp.range_type()=="log_zero_minus":
			return -1 * pow(10, val)
		pass

	@classmethod
	def calc(cls, hp, func):
		lower, upper = ValueLogic.to_calc_val(hp, hp.lower), ValueLogic.to_calc_val(hp, hp.upper)
		smaller, bigger = min(lower, upper), max(lower, upper)
		return ValueLogic.to_real_val(hp, func(hp, smaller, bigger))

class HpList:
	@classmethod
	def set(cls, hps):
		cls.hps = [Hp(h) for h in hps]

	@classmethod
	def get(cls):
		return cls.hps

	@classmethod
	def has(cls, hp_names):
		for hp in cls.hps:
			for hp_name in hp_names:
				if hp.name == hp_name:
					return True
		return False


class LearningRates:
	search_range = ()

	@classmethod
	def names(cls):
		return ["lr", "learning_rate", "LR", "Learning_Rate"]

	@classmethod
	def is_lr_name(cls, name):
		return name in LearningRates.names()

	@classmethod
	def values(cls):
		lr_hp = None
		for hp in HpList.get():
			if LearningRates.is_lr_name(hp.name):
				lr_hp= hp

		if lr_hp is None:
			return []

		values = []
		val = lr_hp.lower
		while True:
			values.append(val)
			val *= 10
			if val > lr_hp.upper:
				break
		return values





