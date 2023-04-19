#Copyright (c) 2023 tanuking
#This software is released under the MIT License, see LICENSE.
import numpy as np
from generater.abstract_generater import AbstractGenerater
from model.hp import HpList, ValueLogic
from model.objectives import Objectives

#StdGeneraterの後の実行を想定
#過去の結果から、最良値とstdで得られたlen(HpList)分の点を取得
#最悪点をもとめ、それ以外の重心を計算
#最悪点の重心に対する反射点を計算し、処理を実行(A)
#分岐
#反射点が最良点よりよい->反射拡大点を計算し処理実行(B)
#  ->(1)反射拡大点が拡大点より良いなら、反射点と最悪点を捨てる->(A)へ
#  ->(2)反射拡大点が拡大点より悪いなら、反射拡大点と最悪点を捨てる->(A)へ
#反射点が最良点より悪いが、第二最悪点より良い->反射点をいれて最悪点を落とす->(A)へ
#反射点が第二最悪点より悪い->収縮点を求めて実行(C)
#  ->(1)収縮点が最悪点より良い->反射点と最悪点を捨て、収縮点を格納->(A)へ
#  ->(2)収縮点が最悪点より悪い->shrink処理を行う->(A)へ

class NelderMeadGenerater(AbstractGenerater):

	def __init__(self, n_gen_max):
		super().__init__(n_gen_max)
		self.my_objectives = None
		self.ref = None
		self.ref_id_obj = None
		self.double_ref = None
		self.shrink = None
		
		self.mode = "initial"
		'''
		"initial", #初期状態
		"normal" #Aを打った状態
		"calc_double", #反射点が最良点より良くて反射拡大点を計算している状態
		"calc_shrink" #反射点が第二最悪点より悪くて収縮点を求めている場合
		'''

	def _get_initial_trial_ids(self, objectives):
		best_id = objectives.get_best_id()
		hp_list_len = len(HpList.get())
		trial_ids = list(objectives.id_obj_dict.keys())
		if best_id in trial_ids[-1 * hp_list_len:]:
			return trial_ids[-1 * (hp_list_len + 1):]
		else:
			ids = trial_ids[-1 * hp_list_len:]
			ids.append(best_id)
			return ids

	def _calc_centroid(self, past_params):
		trial_ids = self.my_objectives.get_ids_sorted_by_obj()[:-1]
		centroid = {}
		for hp in HpList.get():
			num = 0
			for t_id in trial_ids:
				num += ValueLogic.to_calc_val(hp, past_params.get(t_id).get(hp.name))
			centroid[hp.name] = num / len(trial_ids)
		return centroid

	def _calc_reflections(self, centroid, worst_param):
		ref = {}
		double_ref = {}
		shrink = {}
		for hp in HpList.get():
			c_val = centroid[hp.name]
			print(f"w_param {worst_param.get(hp.name)}")
			w_val = ValueLogic.to_calc_val(hp, worst_param.get(hp.name))
			ref[hp.name] = c_val + (c_val - w_val) 
			double_ref[hp.name] = c_val + (c_val - w_val) * 2
			shrink[hp.name] = c_val - (c_val - w_val) * 0.5
		return ref, double_ref, shrink

	#最悪点をもとめ、それ以外の重心を計算
	#最悪点の重心に対する反射点を計算し、処理を実行(A)
	def _normal_calc(self, past_params):
		centroid = self._calc_centroid(past_params)
		worst_param = past_params.get(self.my_objectives.get_worst_id())
		self.ref, self.double_ref, self.shrink = self._calc_reflections(centroid, worst_param)
		print(f"centroid, {centroid} ref {self.ref}")

	def put(self, next_trial_id, past_params, objectives):
		if self.my_objectives is None:
			trial_ids = self._get_initial_trial_ids(objectives)
			self.my_objectives = Objectives(trial_ids, [objectives.get(t_id) for t_id in trial_ids])

		print("***", self.mode, self.my_objectives.id_obj_dict)
		if self.mode == "initial":
			self._normal_calc(past_params)
			self.mode = "normal"
		elif self.mode == "normal":
			last_id = objectives.get_last_trial_id()
			ref_obj = objectives.get(last_id)
			self.ref_id_obj = (last_id, ref_obj)
			best_result = self.my_objectives.get(self.my_objectives.get_best_id())
			worst2_result = self.my_objectives.get(self.my_objectives.get_ids_sorted_by_obj()[-2])
			#反射点が最良点よりよい->反射拡大点を計算し処理実行(B)
			if ref_obj < best_result:
				self.mode = "calc_double"
			#反射点が最良点より悪いが、第二最悪点より良い->反射点をいれて最悪点を落とす->(A)へ
			elif ref_obj < worst2_result:
				self.my_objectives.pop(self.my_objectives.get_worst_id())
				self.my_objectives.put(last_id, ref_obj)
				self._normal_calc(past_params)
				self.mode = "normal"
			#反射点が第二最悪点より悪い->収縮点を求めて実行(C)
			elif ref_obj > worst2_result:
				self.mode = "calc_shrink"
		#反射点が最良点よりよい->反射拡大点を計算し処理実行(B)
		#  ->(1)反射拡大点が拡大点より良いなら、反射点と最悪点を捨てる->(A)へ
		#  ->(2)反射拡大点が拡大点より悪いなら、反射拡大点と最悪点を捨てる->(A)へ
		elif self.mode == "calc_double":
			last_id = objectives.get_last_trial_id()
			double_ref_obj = objectives.get(last_id)
			self.my_objectives.pop(self.my_objectives.get_worst_id())
			if double_ref_obj < self.ref_id_obj[1]:
				self.my_objectives.put(last_id, double_ref_obj)
			else:
				self.my_objectives.put(self.ref_id_obj[0], self.ref_id_obj[1])
			self._normal_calc(past_params)
			self.mode = "normal"
		#反射点が第二最悪点より悪い->収縮点を求めて実行(C)
		#  ->(1)収縮点が最悪点より良い->反射点と最悪点を捨て、収縮点を格納->(A)へ
		#  ->(2)収縮点が最悪点より悪い->shrink処理を行う->(A)へ *これに手間がかかりすぎるのでもう一度shrinkする
		elif self.mode == "calc_shrink":
			last_id = objectives.get_last_trial_id()
			shrink_obj = objectives.get(last_id)
			worst_obj = self.my_objectives.get(self.my_objectives.get_worst_id())
			if shrink_obj < worst_obj:
				self.my_objectives.pop(self.my_objectives.get_worst_id())
				self.my_objectives.put(last_id, shrink_obj)
				self._normal_calc(past_params)
				self.mode = "normal"
			else:
				best_param = past_params.get(objectives.get_best_id())
				new_shrink = {}
				for hp in HpList.get():
					b_val = ValueLogic.to_calc_val(hp, best_param.get(hp.name))
					s_val = shrink[hp.name]
					new_shrink[hp.name] = (b_val + s_val) / 2
				self.shrink = new_shrink
				self.mode = "calc_shrink"
			
	def _shrink_all(self):
		self.warning_out()

	def func(self, hp, smaller, bigger):
		if self.mode == "normal":
			return self.ref[hp.name]
		if self.mode == "calc_double":
			return self.double_ref[hp.name]
		if self.mode == "calc_shrink":
			return self.shrink[hp.name]

