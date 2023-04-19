#Copyright (c) 2023 tanuking
#This software is released under the MIT License, see LICENSE.


class  Objectives:
	def __init__(self, trial_ids, objs):
		self.id_obj_dict = {t_id:obj for t_id, obj in zip(trial_ids, objs)}
		self.trial_ids = trial_ids

	def get(self, trial_id):
		return self.id_obj_dict[trial_id]

	def put(self, trial_id, obj):
		self.id_obj_dict[trial_id] = obj

	def pop(self, trial_id):
		return self.id_obj_dict.pop(trial_id)

	def get_best_id(self):
		sorted_ids = self.get_ids_sorted_by_obj()
		if len(sorted_ids) > 0:
			return sorted_ids[0]
		return 0

	def get_worst_id(self):
		sorted_ids = self.get_ids_sorted_by_obj()
		if len(sorted_ids) > 0:
			return sorted_ids[-1]
		return 0

	def get_last_trial_id(self):
		return self.trial_ids[-1]
	
	def get_ids_sorted_by_obj(self):
		temp = {t_id:obj for t_id, obj in self.id_obj_dict.items() if (obj is not None) & (t_id != 0)}
		temp = sorted(temp.items(), key=lambda x:x[1])
		return [t[0] for t in temp]

	def has_not_null(self):
		return len([v for v in self.id_obj_dict.values() if v is not None]) == len(self.id_obj_dict)