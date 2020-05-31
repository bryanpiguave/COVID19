# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 15:52:05 2020

@author: Bryan Piguave
"""

import nl4py
import os
file_to_open = os.path.join(".","spatialCOVID19-master","epiDEM COV_v13.nlogo")
path_to_netlogo = 'C:/Program Files/NetLogo 6.1.1/'
nl4py.startServer(path_to_netlogo)
ws=nl4py.newNetLogoHeadlessWorkspace()
ws.openModel(file_to_open)
ws.closeModel()
nl4py.deleteAllHeadlessWorkspaces()
nl4py.stopServer()
