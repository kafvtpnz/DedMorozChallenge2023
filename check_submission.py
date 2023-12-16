# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 22:08:53 2023

@author: AM4
"""

import pandas as pd
import math
import argparse


def check(pred):
    import numpy as np
    from collections import Counter

    n_children = 184000 
    n_gift_type = 1000
    n_gift_quant = 250
    n_gift_pref = 100
    n_child_pref = 184 
    twins = math.ceil(0.03 * n_children / 2.) * 2    # 3% близнецов
    ratio_gift_happiness = 2
    ratio_child_happiness = 2


    gift_pref = pd.read_csv('./kids_wish.csv',header=None).drop(0, 1).values
    child_pref = pd.read_csv('./ded_moroz_wish.csv',header=None).drop(0, 1).values
    
    # проверка количества подарков
    ppp = [elem[1] for elem in pred]
    gift_counts = Counter(elem[1] for elem in pred)
    for i, count in zip(gift_counts.keys(), gift_counts.values()):
        print(i, count)
        assert count <= n_gift_quant
        
    # проверка подарков близнецов            
    for t1 in np.arange(0,twins,2):
        twin1 = pred[t1]
        twin2 = pred[t1+1]
        # print(t1)
        assert twin1[1] == twin2[1]


    total_child_happiness = 0
    total_gift_happiness = np.zeros(n_gift_type)
    
    for row in pred:
        child_id = row[0]
        gift_id = row[1]
        
        # проверки id подарков и детей
        assert child_id < n_children
        assert gift_id < n_gift_type
        assert child_id >= 0 
        assert gift_id >= 0
        child_happiness = (n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ratio_child_happiness
        if not child_happiness:
            child_happiness = -1

        gift_happiness = ( n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ratio_gift_happiness
        if not gift_happiness:
            gift_happiness = -1

        total_child_happiness += child_happiness
        total_gift_happiness[gift_id] += gift_happiness
    
    print('normalized child happiness=',float(total_child_happiness)/(float(n_children)) , \
        ', normalized gift happiness',np.mean(total_gift_happiness) / float(n_gift_quant))


    return (float(total_child_happiness)/float(n_children))+np.mean(total_gift_happiness) / float(n_gift_quant)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', type=str, default='solution_example.csv', help='path to file')
    opt = parser.parse_args()
    sub_file = pd.read_csv(opt.path).values.tolist()
    print('Total happiness', check(sub_file))











