# aiaccel_cassete_optimizer

This program is an optimizer for aiaccel. By passing the results of each trial to a Manager that contains multiple Generators for generating parameters, it searches for the optimal hyperparameters. The Manager can be switched like a cassette, allowing for the exploration of hyperparameters that adapt to various situations by changing the combination of Generators. In other words, it is a system that allows for the adjustment of hyperparameters for the purpose of searching for hyperparameters.

Additionally, this code is an award-winning entry in the Signate HPO competition. In the competition, the challenge was to search for the optimal solution in a very small number of trials (about 50 times), which required trying various combinations, leading to the creation of this code.

# License
The source code is licensed MIT. The website content is licensed CC BY 4.0,see LICENSE.