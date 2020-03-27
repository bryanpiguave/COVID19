#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 20:09:32 2020

@author: dcecchis

Example number 1 to test the installation 
of the pyNetLogo
"""

#%matplotlib inline

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('white')
sns.set_context('talk')


import pyNetLogo

netlogo = pyNetLogo.NetLogoLink(gui='True')

netlogo.load_model('./Wolf Sheep Predation_v6.nlogo')

netlogo.command('setup')


