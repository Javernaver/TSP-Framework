"""Paquete principal del framework que contiene los modulos para obtener soluciones a problemas TSP"""
import argparse
import math
import os
import sys
import time
from enum import Enum
from decimal import Decimal

from src import utilities
from src.utilities import bcolors, Trajectory
from src.TSPlibReader import TSPlibReader
from src.AlgorithmsOptions import AlgorithmsOptions, InitialSolution, CoolingType, MHType, SelectionStrategy, SelectionType, CrossoverType, TSPMove
from src.Tsp import Tsp
from src.Tour import Tour
from src import plot