# Evaluation of our solutions, using if_random.py example case.

# Std
from os import listdir

# Thrid party
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


def eval_instance(instance, algo, n_runs=100, confidence=0.95, plot=False):
  '''
  Evaluation of an algorithm on an already parsed k-server instance over n_runs.
  If plotting is enabled, plot x=nth-run y=score-of-nth-run
  The algo argument should provide a run() function that takes an instance and returns
  a score.
  Returns a tuple with:
  - The mean score (int)
  - The confidence interval (tuple of int * int)
  '''
  scores = []
  for epoch in range(n_runs):
    scores.append(algo(instance))

  average = np.mean(scores)
  (low, high) = stats.norm.interval(confidence, loc=average, scale=stats.sem(scores))

  if plot:
    plt.plot(np.arange(len(scores)), scores)
    # Confidence interval ploting test (Good)
    #plt.fill_between(np.arange(0, n_runs, n_runs/len(scores)), np.array(scores)+5, np.array(scores)-5, 
    #                 color="orange", alpha=0.3, linewidth=0.6)
    plt.yticks(np.arange(0, 200, 25))
    plt.show()

  return (average, (low, high))


def all_eval(instances, algo, n_runs=100, confidence=0.95, plot=False):
  '''
  Evaluate all the given instances using the eval_instance function.
  If plotting is enabled, plot x=nth-instance y=(score, confidence interval)
  '''
  averages  = []
  intervals = []
  for instance in instances:
    avg, confidence_interval = eval_instance(instance, algo, n_runs, confidence)
    averages.append(avg)
    intervals.append(confidence_interval)

  if plot:
    plot_curve(np.arange(len(averages)), averages)
    plot_fill(np.arange(len(averages)), intervals)
    plot_set_yticks(averages)
    plt.show()

  return averages, intervals


def plot_curve(x, y):
  plt.plot(x, y)
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
  plt.yticks(np.arange(0, int(max_y + max_y/2), step=(int(max_y/8))))


_instances_dir_str = "./instances/"
_instances_str = listdir("instances")


# Class to test evaluate-functions behaviors
class RandomAlgo:
  def __init__(self, lower_bound, upper_bound):
    self.rng   = np.random.default_rng()
    self.low_b = lower_bound
    self.up_b  = upper_bound

  def run(self, some_stuff):
    rd = self.rng.random()
    rd = (self.up_b - self.low_b) * rd + self.low_b
    return rd


if __name__ == "__main__":

  instance = None
  algo = RandomAlgo(70, 120)

  eval_instance(None, algo, plot=True)
  all_eval(range(15), algo, plot=True)

  
