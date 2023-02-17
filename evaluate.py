# Evaluation of our solutions, using if_random.py example case.

# Personnal
from main import naive_algo, all_servers_algo, KServerInstance

# Std
from os import listdir
import sys

# Thrid party
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


def eval_instance(instance, algo, n_runs=100, confidence=0.95, plot=False):
  '''
  Evaluation of an algorithm over n_runs. If plotting is enabled, plot the scores
  and the confidence interval.
  
  Returns a tuple with:
  - The mean score (int)
  - The confidence interval (tuple of int * int)

  (The algo argument should be a callable object)
  '''
  scores = []
  for epoch in range(n_runs):
    scores.append(algo(instance))

  average = np.mean(scores)
  (low, high) = stats.norm.interval(confidence, loc=average, scale=stats.sem(scores))
  print(low, high)

  if plot:
    plt.plot()
    x = np.arange(len(scores))
    plot_curve(x, scores, "score")
    plot_fill(x, [(low, high) for i in range(len(x))])
    plot_set_yticks(scores)
    plt.legend()
    plt.show()

  return (average, (low, high))


def all_eval(instances, algo, n_runs=100, confidence=0.95, plot=False):
  '''
  Evaluate all the given instances using the eval_instance function.
  If plotting is enabled, plot x=nth-instance y=(score, confidence interval)
  '''
  averages  = []
  intervals = []
  opts = []
  for instance in instances:
    avg, confidence_interval = eval_instance(instance, algo, n_runs, confidence)
    averages.append(avg)
    intervals.append(confidence_interval)
    opts.append(instance.opt)

  if plot:
    x = np.arange(len(averages))
    plot_curve(x, averages, "scores")
    plot_curve(x, opts, "opt")
    plot_fill(np.arange(len(averages)), intervals)
    plot_set_yticks(averages)
    plt.legend()
    plt.show()

  return averages, intervals


def plot_curve(x, y, l):
  plt.plot(x, y, label=l)
  max_y = np.max(y)


def plot_fill(x, intervals):
  y_lower = []
  y_upper = []
  for l, u in intervals:
    y_lower.append(l)
    y_upper.append(u)
  plt.fill_between(x, y_lower, y_upper, color="orange", alpha=0.3, linewidth=0.6)


def plot_set_yticks(y):
  max_y = int(np.max(y))
  plt.ylim(ymin=0, ymax=(max_y+int(max_y/3)))


_instances_dir_str = "./instances/"
_instances_str = listdir("instances")


if __name__ == "__main__":
  i = 0
  for index, f_name in enumerate(_instances_str):
    if i % 2 == 0:
      print("%2d"%index, f_name.ljust(35), end="")
    else:
      print(index, f_name)
    i = (i+1) % 2
  print()
  n = int(input(f"-1 for all, 0-{len(_instances_str)} otherwise.\n"))

  if (n != -1):
    i = KServerInstance()
    f_name = _instances_str[n]
    i.parse(f_name)
    eval_instance(i, naive_algo, plot=True)
  else:
    instances = []
    for f_name in _instances_str:
      i = KServerInstance()
      i.parse(f_name)
      instances.append(i)
    all_eval(instances, naive_algo, plot=True)



# Class to test evaluate-functions behaviors
class RandomAlgo:
  def __init__(self, lower_bound, upper_bound):
    self.rng   = np.random.default_rng()
    self.low_b = lower_bound
    self.up_b  = upper_bound

  def __call__(self, some_stuff):
    rd = self.rng.random()
    rd = (self.up_b - self.low_b) * rd + self.low_b
    return rd

'''
if __name__ == "__main__":
  instance = None
  algo = RandomAlgo(70, 120)

  eval_instance(None, algo, plot=True)
  all_eval(range(15), algo, plot=True)
'''

  
