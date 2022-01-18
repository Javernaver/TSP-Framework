"""Paquete principal del framework que contiene los modulos para obtener soluciones a problemas TSP"""
import argparse
import math
import os
import sys
import time
from enum import Enum
from decimal import Decimal

from src.tspf import utilities
from src.tspf.utilities import bcolors, Trajectory
from src.tspf.TSPlibReader import TSPlibReader
from src.tspf.AlgorithmsOptions import AlgorithmsOptions, InitialSolution, CoolingType, MHType, SelectionStrategy, SelectionType, CrossoverType, TSPMove, PerturbationType
from src.tspf.Tsp import Tsp
from src.tspf.Tour import Tour
from src.tspf import plot