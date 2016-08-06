# -*- coding:utf-8 -*-
# Filename: test_weather.py
# Author：hankcs
# Date: 2016-08-06 PM6:04
import numpy as np

import hmm

states = ('Healthy', 'Fever')

observations = ('normal', 'cold', 'dizzy')

start_probability = {'Healthy': 0.6, 'Fever': 0.4}

transition_probability = {
    'Healthy': {'Healthy': 0.7, 'Fever': 0.3},
    'Fever': {'Healthy': 0.4, 'Fever': 0.6},
}

emission_probability = {
    'Healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
    'Fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6},
}


def generate_index_map(lables):
    index_label = {}
    label_index = {}
    i = 0
    for l in lables:
        index_label[i] = l
        label_index[l] = i
        i += 1
    return label_index, index_label


states_label_index, states_index_label = generate_index_map(states)
observations_label_index, observations_index_label = generate_index_map(observations)


def convert_observations_to_index(observations, label_index):
    list = []
    for o in observations:
        list.append(label_index[o])
    return list


def convert_map_to_vector(map, label_index):
    v = np.empty(len(map), dtype=float)
    for e in map:
        v[label_index[e]] = map[e]
    return v


def convert_map_to_matrix(map, label_index1, label_index2):
    m = np.empty((len(label_index2), len(label_index1)), dtype=float)
    for line in map:
        for col in map[line]:
            m[label_index2[col]][label_index1[line]] = map[line][col]
    return m


observations_index = convert_observations_to_index(observations, observations_label_index)
start_probability_vector = convert_map_to_vector(start_probability, states_label_index)
# print start_probability_vector
transition_probability_matrix = convert_map_to_matrix(transition_probability, states_label_index, states_label_index)
# print transition_probability_matrix
emission_probability_matrix = convert_map_to_matrix(emission_probability, states_label_index, observations_label_index)
# print emission_probability_matrix

h = hmm.HMM(transition_probability_matrix, emission_probability_matrix, start_probability_vector)
sequence, score = h.viterbi(observations_index)
for s in sequence:
    print states_index_label[s],
print np.exp(score)
