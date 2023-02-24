# Evaluation of our solutions, using if_random.py example case.

# Personnal
from algorithms import (
  naive_algo, 
  all_servers_algo, 
  random_all_servers_algo, 
  move_all_server_algo,
  move_all_server_randalgo,
  random_tired_algo,
  naive_random_algo
)

from parse import KServerInstance

# Std
from os import listdir

# Thrid party
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


_instances_dir_str = "./instances/"
_instances_str = listdir("instances")


def eval_main():
  # straightforward process of evaluating and plotting on all instances

  # get algo and instances
  algos = {
    "move all server algo": move_all_server_algo,
    #"naive algo": naive_algo,
    #"random all servers algo": random_all_servers_algo,
    "all servers algo" :all_servers_algo,
    "naive random algo": naive_random_algo,
    "random tired algo" : random_tired_algo
  }
  instances = []
  for f_name in _instances_str:
      i = KServerInstance()
      i.parse(f_name)
      instances.append(i)
  n_instances = len(instances)
  confidence = 0.95

  # compute averages and intervals on each instance. Of course it doesn't make sense
  # for deterministic algorithms.
  algos_data = {}
  for algo_name in algos:
    algo = algos[algo_name]
    algo_data = {}
    averages = []
    intervals = []
    for i in instances:
      scores = [algo(i).sum_distance for _ in range(100)]
      average = np.mean(scores)
      averages.append(average)
      intervals.append(stats.norm.interval(confidence, loc=average, scale=stats.sem(scores)))
    algo_data["averages"] = averages
    algo_data["intervals"] = intervals
    algos_data[algo_name] = algo_data

  # now compute ratio and stuff about it
  opts = [i.opt for i in instances]
  for algo_name in algos:
    algo_data = algos_data[algo_name]
    ratios = [algo_data["averages"][i]/opts[i] for i in range(n_instances)]
    algo_data["ratio_data"] = {
      "mean": np.mean(ratios),
      "worst" : np.max(ratios),
      "best" : np.min(ratios),
      "confidence" : stats.norm.interval(confidence, loc=(np.mean(ratios)), scale=stats.sem(ratios))  
    }
    algo_data["ratios"] = ratios

  # Finally we can plot
  # one figure to plot the score, one to plot the data
  fig, (axis_scores, axis_ratios, axis_data) = plt.subplots(1, 3, figsize=(40, 10))
  # fig, (axis_scores, axis_ratios, axis_data) = plt.subplots(3, 1, figsize=(10, 40))
  x_ticks = np.arange(n_instances)
  font = {
    'family': 'serif',
    'color':  'black',
    'weight': 'normal',
    'size': 12,
  }

  data_txt = ""
  for algo_name in algos:
    algo_data = algos_data[algo_name]

    axis_scores.plot(x_ticks, algo_data["averages"], label=algo_name)
    axis_ratios.plot(x_ticks, algo_data["ratios"], label=algo_name)

    data_txt += algo_name + " : \n"
    ratio_data = algo_data["ratio_data"]
    data_txt += "\tratio data : \n"
    for prop in ratio_data:
      data_txt += "\t" + prop + " : " + str(np.around(ratio_data[prop], 3)) + "  "
    data_txt += "\n"

  axis_data.text(0.01, 0, data_txt.expandtabs(), fontdict=font)
  axis_scores.plot(x_ticks, opts, label="optimal values")
  axis_ratios.plot(x_ticks, np.full((n_instances, 1) , 1), label="reference value")
  
  # stuff to make things more clear
  axis_scores.set_xticks(x_ticks)
  axis_ratios.set_xticks(x_ticks)
  max_ratio = int(np.max(ratios)) + 2
  axis_ratios.set_ylim(ymin=0, ymax=(max_ratio+int(max_ratio/3)))
  plt.setp(axis_data.get_xticklabels(), visible=False)
  plt.setp(axis_data.get_yticklabels(), visible=False)
  axis_data.tick_params(axis='both', which='both', length=0)
  axis_scores.legend()
  axis_ratios.legend()
  axis_data.legend()
  plt.show()


def eval_instance_det(instance, algo):
  '''
  Evaluation of a deterministic algorithm
  '''
  state = algo(instance)
  print("Opt   : ", instance.opt)
  print("Score : ", state.sum_distance)
  print("servers distances : ", list([s.sum_distance for s in state.servers]))
  #print("Moves : ", list(state.moves))

  return state


def eval_instance_rand(instance, algo, n_runs=100, confidence=0.95, plot=False):
  '''
  Evaluation of a random algorithm over n_runs. If plotting is enabled, plot the scores
  and the confidence interval.

  Returns a tuple with:
  - The mean score (int)
  - The confidence interval (tuple of int * int)

  (The algo argument should be a callable object)
  '''
  scores = []
  for epoch in range(n_runs):
    state = algo(instance)
    scores.append(state.sum_distance)

  average = np.mean(scores)
  (low, high) = stats.norm.interval(confidence, loc=average, scale=stats.sem(scores))
  # print(low, high, average)

  if plot:
    plt.plot()

    low_diff  = average - low
    high_diff = high - average

    x = np.arange(len(scores))
    plot_scatter(x, scores, "score")
    plot_fill(x, [(scores[i] - low_diff, scores[i] + high_diff) for i in range(len(x))])
    plot_smoothen_yticks(scores)
    plt.legend()
    plt.show()

  return (average, (low, high))

if __name__ == "__main__":
  # print instances
  i = 0
  for index, f_name in enumerate(_instances_str):
    if i % 2 == 0:
      print("%2d"%index, f_name.ljust(35), end="")
    else:
      print(index, f_name)
    i = (i+1) % 2
  print()

  # evaluation script
  eval_main()




def all_eval(instances, algo, n_runs=100, confidence=0.95, plot=False):
  '''
  Evaluate all the given instances using the eval_instance function.
  If plotting is enabled, plot x=nth-instance y=(score, confidence interval)
  '''
  averages  = []
  intervals = []
  opts = []
  for instance in instances:
    avg, confidence_interval = eval_instance_rand(instance, algo, n_runs, confidence)
    averages.append(avg)
    intervals.append(confidence_interval)
    opts.append(instance.opt)

  if plot:
    x = np.arange(len(averages))
    plot_scatter(x, averages, "scores")
    plot_scatter(x, opts, "opt")
    plot_fill(np.arange(len(averages)), intervals)
    plot_smoothen_yticks(averages)
    plt.legend()

  sum_diff = 0
  for i in range(len(averages)):
    sum_diff += averages[i] - opts[i]
  print("The 20 instances difference of sum distance between opt and average: " + str(sum_diff))

  return averages, intervals


def eval_ratio(instances, averages, confidence=0.95, plot=False):
  ratios = list([average / instances[i].opt for i, average in enumerate(averages)])
  print("Ratios : ", ratios)
  print("Worst ratio : ", np.max(ratios))
  mean = np.mean(ratios)
  print("Average ratio : ", mean)
  print("Confidence : ", stats.norm.interval(confidence, loc=mean, scale=stats.sem(ratios)))
  print("Best ratio  : ", np.min(ratios))

  if plot:
    n = len(averages)
    # plot_scatter(np.arange(n), np.full((n, 1), 1), "opt")
    # plot_scatter(np.arange(n), ratios, "ratio")
    # plot_smoothen_yticks(ratios)
    plt.text(3*n/4, 3*n/4, "HELLLLLLo")


def plot_scatter(x, y, l):
  plt.plot(x, y, label=l)


def plot_fill(x, intervals):
  y_lower = []
  y_upper = []
  for l, u in intervals:
    y_lower.append(l)
    y_upper.append(u)
  plt.fill_between(x, y_lower, y_upper, color="orange", alpha=0.3, linewidth=0.6)


def plot_smoothen_yticks(y):
  max_y = int(np.max(y))
  plt.ylim(ymin=0, ymax=(max_y+int(max_y/3)))


def pick_instance():
  i = 0
  for index, f_name in enumerate(_instances_str):
    if i % 2 == 0:
      print("%2d"%index, f_name.ljust(35), end="")
    else:
      print(index, f_name)
    i = (i+1) % 2
  print()
  return int(input(f"-1 for all, 0-{len(_instances_str)} otherwise.\n"))


def run_eval(algo, eval_type="det"):
  n = pick_instance()
  if n == -1:
    instances = []
    for f_name in _instances_str:
      i = KServerInstance()
      i.parse(f_name)
      instances.append(i)
    averages, intervals = all_eval(instances, algo, plot=True)
    eval_ratio(instances, averages, plot=True)
    plt.show()
  else:
    i = KServerInstance()
    i.parse(_instances_str[n])
    if eval_type == "det":
      eval_instance_det(i, algo)
    elif eval_type == "rand":
      eval_instance_rand(i, algo, plot=True)


'''
if __name__ == "__main__":

  algo = 0
  eval_type = sys.argv[1]

  if eval_type == "rand":
    # algo = move_all_server_randalgo 
    algo = random_all_servers_algo
  elif eval_type == "det":
    # algo = all_servers_algo
    # algo = naive_algo
    algo = move_all_server_algo
  else:
    print("please specify rand or det")

  run_eval(algo, eval_type)
'''
