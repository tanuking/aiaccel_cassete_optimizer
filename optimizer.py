#Copyright (c) 2023 tanuking
#This software is released under the MIT License, see LICENSE.

import json
import numpy as np
import os
import random
import csv
from aiaccel.optimizer.abstract_optimizer import AbstractOptimizer

from model.hp import HpList
from model.objectives import Objectives
from manager.manager import Manager

RANDOM_SEED = 1215
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

class MyOptimizer(AbstractOptimizer):

    def __init__(self, options: dict) -> None:
        super().__init__(options)

    def pre_process(self) -> None:
        super().pre_process()
        HpList.set(self.params.get_parameter_list())
        self.manager = Manager()

    def generate_initial_parameter(self):
        return self.generate_parameter()

    def generate_parameter(self) -> None:
        trial_ids = self.storage.trial.get_all_trial_id()
        next_trial_id = self.trial_id.get()
        if trial_ids is not None:
            objs = Objectives(trial_ids, [self.storage.result.get_any_trial_objective(t_id) for t_id in trial_ids])
        else:
            objs = Objectives([], [])

        self.manager.put(next_trial_id, objs)
        param = self.manager.generate(next_trial_id)
        print(next_trial_id, param)

        with open('objs.csv', 'w') as f:
            writer = csv.writer(f)
            if trial_ids is not None:
                for trial_id in trial_ids:
                    writer.writerow(["", objs.get(trial_id)])
        return param