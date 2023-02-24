# Personnal
from run_state import RunState
from parse import KServerInstance

# Std
import random
import math

# Third party
import numpy as np


def naive_algo(k_instance: KServerInstance):
    """
    Choose the closest server to treat the customer for every request
    20 instances difference of sum_distance: 148,614
    :param k_instance:
    :return:
    """
    state = RunState(k_instance)

    while state.num_request <= len(state.k_instance.requests) - 1:
        distances = state.distances
        min_distance = min(distances)
        # index of minimum distance server
        index = distances.index(min_distance)
        # choose the closest server to treat the costumer
        state.update(index)
    return state


def all_servers_algo(k_instance: KServerInstance):
    """
    Choose the closest server to treat the costumer for every request
    AND, if there are servers that never move, we prioritize them so that we use all servers we have.
    20 instances difference of sum_distance: 13,667
    :param k_instance:
    :return:
    """
    state = RunState(k_instance)

    while state.num_request <= len(state.k_instance.requests) - 1:
        distances = state.distances

        min_distance = min(distances)
        # index of minimum distance server
        index = distances.index(min_distance)

        for server in state.servers:
            if server.never_move():
                index = server.id

        # choose the closest server to treat the costumer
        state.update(index)
    # print("The offline result is: " + str(state.k_instance.opt))
    # print("The online algorithm result is: " + str(state.sum_distance))
    return state


def naive_random_algo(k_instance: KServerInstance):
    """
    Choose randomly servers to treat the costumer for every request
    :param k_instance:
    :return:
    """
    state = RunState(k_instance)

    while state.num_request <= len(state.k_instance.requests) - 1:
        index = random.randint(0, len(state.servers)-1)

        state.update(index)
    # print("The offline result is: " + str(state.k_instance.opt))
    # print("The online algorithm result is: " + str(state.sum_distance))
    return state


def random_all_servers_algo(k_instance: KServerInstance):
    """
    Choose randomly servers to treat the costumer for every request
    AND, if there are servers that never move, we prioritize them so that we use all servers we have.
    20 instances difference of sum_distance: around 275,500
    :param k_instance:
    :return:
    """
    state = RunState(k_instance)

    while state.num_request <= len(state.k_instance.requests) - 1:
        index = random.randint(0, len(state.servers)-1)

        for server in state.servers:
            if server.never_move():
                index = server.id

        state.update(index)
    # print("The offline result is: " + str(state.k_instance.opt))
    # print("The online algorithm result is: " + str(state.sum_distance))
    return state


def move_all_server_algo(k_instance):
  '''
  Phase 1 : move all servers
  Phase 2 : prioritize closest server

  20 instances difference of sum_distance: 12,691
  '''
  state      = RunState(k_instance)
  n_servers  = k_instance.k
  n_reqs     = len(k_instance.requests)
  num_server = 0

  # -------- Phase 1 --------
  while (state.num_request < n_servers 
        and state.num_request < n_reqs):
    distances = state.distances
    if np.min(distances) == 0:
      state.update(np.argmin(distances))
      continue
    state.update(num_server)
    num_server  += 1

  # -------- Phase 2 --------
  while state.num_request < n_reqs:
    num_server = np.argmin(state.distances)
    state.update(num_server)

  return state


def move_all_server_randalgo(k_instance):
  '''
  Phase 1 : move all servers
  Phase 2 : random (uniform distribution) / closest server

  20 instances difference of sum_distance: 12,691
  '''
  state      = RunState(k_instance)
  n_servers  = k_instance.k
  n_reqs     = len(k_instance.requests)
  num_server = 0

  # -------- Phase 1 --------
  while (state.num_request < n_servers 
        and state.num_request < n_reqs):
    state.update(num_server)
    num_server  += 1

  # -------- Phase 2 --------
  while state.num_request < n_reqs:
    num_server = (np.random.randint(0, k_instance.k) 
                  if np.random.rand() < 0.1 else 
                  np.argmin(state.distances))
    state.update(num_server)

  return state


def sigmoid(x):
    # return 1 / (1 + math.exp(-0.1*(x-40)))
    return 1 / (1 + math.exp(-x))


def is_tired(n):
    rand = random.random()
    proba = sigmoid(n)
    return rand < proba


def random_tired_algo(k_instance):
    """
        Choose randomly servers to treat the costumer for every request
        :param k_instance:
        :return:
        """
    state = RunState(k_instance)

    while state.num_request <= len(state.k_instance.requests) - 1:
        index = random.randint(0, len(state.servers) - 1)
        #
        # # while is_tired(state.servers[index].move_times):
        #     # index = random.randint(0, len(state.servers) - 1)
        # print(is_tired(state.servers[index].move_times))
        if is_tired(state.servers[index].nb_moves):
            index = np.argmin(state.distances)

        state.update(index)
    # print("The offline result is: " + str(state.k_instance.opt))
    # print("The online algorithm result is: " + str(state.sum_distance))
    return state