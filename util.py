from typing import *
from math import sqrt

def minor(matrix: List[List[float]], i, j) -> List[List[float]]:
  n = len(matrix)
  return [
    [matrix[row][col] for col in range(n) if col != j] for row in range(n) if row != i
  ]

def det(matrix: List[List[float]]) -> float:
  n = len(matrix)
  if n == 1:
    return matrix[0][0]
  d = 0
  sgn = 1
  for j in range(n):
    d += sgn * matrix[0][j] * det(minor(matrix, 0, j))
    sgn *= -1
  return d

def calc_s(y, f):
  n = len(y)
  return sum((f[i] - y[i]) ** 2 for i in range(n))

def calc_delta(y, f):
  n = len(y)
  return sqrt(calc_s(y, f) / n)

def define_accuracy_str(acc: float) -> str:
  if acc < 0.5:
    return 'Insufficient approximation accuracy'
  elif acc < 0.75:
    return 'Poor approximation accuracy'
  elif acc < 0.95:
    return 'Satisfactory approximation accuracy'
  else:
    return 'High approximation accuracy'
