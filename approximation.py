from util import *
from math import sqrt, exp, log

def linear_func(x: List[float], y: List[float]):
  data: Dict = {}

  # calculate sums for the least square method
  n: int = len(x)
  sx: float = sum(x)
  sxx: float = sum([x_i ** 2 for x_i in x])
  sy: float = sum(y)
  sxy: float = sum([x[i] * y[i] for i in range(0, len(x))])

  # calculate correlation coefficient
  x_m: float = sx / n
  y_m: float = sy / n
  numerator = sum((x[i] - x_m) * (y[i] - y_m) for i in range(n))
  denominator1 = sum((x[i] - x_m) ** 2 for i in range(n))
  denominator2 = sum((y[i] - y_m) ** 2 for i in range(n))
  r = numerator / sqrt(denominator1 * denominator2)

  # calculate determinants for the Cramer's method
  d = det([[sxx, sx], [sx, n]])
  d1 = det([[sxy, sx], [sy, n]])
  d2 = det([[sxx, sxy], [sx, sy]])
  
  try:
    # calculate linear approximation coefficients
    a = d1 / d # linear approximation coefficient
    b = d2 / d # linear approximation coefficient
    fi = [a * x_i + b for x_i in x] # approximate function with new coefficients

    # calculate determination coefficient
    numerator = [(y[i] - fi[i]) ** 2 for i in range(n)]
    denominator = [(y[i] - (sum(fi) / n)) ** 2 for i in range(n)]
    R2 = 1 - (sum(numerator) / sum(denominator))

    # coefficient calculation succeed: store results
    data['a'] = a # approximation coefficient
    data['b'] = b # approximation coefficient
    data['x'] = x # initial data
    data['y'] = y # initial data
    data['fi'] = fi # approximated function
    data['R2'] = define_accuracy_str(R2) # accuracity based on the determination coefficient
    data['s'] = calc_s(y, fi) # deviation squares sum
    data['delta'] = calc_delta(y, fi) # standard deviation
    data['r'] = r # correlation coefficient
    data['eps'] = [(fi[i] - y[i]) for i in range(len(fi)) ]
    return data
  except Exception:
    raise Exception('Unable to solve equation system with Cramer\'s method: division by zero is prohibited :C')

def polynomial_2_func(x: List[float], y: List[float]):
  data: Dict = {}

  # calculate sums for the least square method
  n: int = len(x)
  sx: float = sum(x)
  sx2: float = sum([xi ** 2 for xi in x])
  sx3: float = sum([xi ** 3 for xi in x])
  sx4: float = sum([xi ** 4 for xi in x])
  sy: float = sum(y)
  sxy: float = sum([x[i] * y[i] for i in range(n)])
  sx2y: float = sum([(x[i] ** 2) * y[i] for i in range(n)])

  # calculate determinants for the Cramer's method
  d = det([[n, sx, sx2], [sx, sx2, sx3], [sx2, sx3, sx4]])
  d1 = det([[sy, sx, sx2], [sxy, sx2, sx3],[sx2y, sx3, sx4]])
  d2 = det([[n, sy, sx2],[sx, sxy, sx3],[sx2, sx2y, sx4]])
  d3 = det([[n, sx, sy], [sx, sx2, sxy], [sx2, sx3, sx2y]])

  try:
    # calculate polynomial(2) approximation coefficients
    a = d1 / d # polynomial(2) approximation coefficient
    b = d2 / d # polynomial(2) approximation coefficient
    c = d3 / d # polynomial(2) approximation coefficient
    fi = [a + b * x_i + c * x_i ** 2 for x_i in x] # approximate function with new coefficients

    # calculate determination coefficient
    numerator = [(y[i] - fi[i]) ** 2 for i in range(n)]
    denominator = [(y[i] - (sum(fi) / n)) ** 2 for i in range(n)]
    R2 = 1 - (sum(numerator) / sum(denominator))

    # coefficient calculation succeed: store results
    data['a'] = a
    data['b'] = b
    data['c'] = c
    data['x'] = x
    data['y'] = y
    data['fi'] = fi
    data['R2'] = define_accuracy_str(R2)
    data['s'] = calc_s(y, fi)
    data['delta'] = calc_delta(y, fi)
    data['message'] = 'reduced to linear' if (c == 0) else ''
    data['eps'] = [(fi[i] - y[i]) for i in range(len(fi)) ]
    return data
  except Exception:
    raise Exception('Unable to solve equation system with Cramer\'s method: division by zero is prohibited :C')

def polynomial_3_func(x: List[float], y: List[float]):
  data: Dict = {}

  # calculate sums for the least square method
  n: int = len(x)
  sx: float = sum(x)
  sx2: float = sum([xi ** 2 for xi in x])
  sx3: float = sum([xi ** 3 for xi in x])
  sx4: float = sum([xi ** 4 for xi in x])
  sx5: float = sum([xi ** 5 for xi in x])
  sx6: float = sum([xi ** 6 for xi in x])
  sy: float = sum(y)
  sxy: float = sum([x[i] * y[i] for i in range(n)])
  sx2y: float = sum([(x[i] ** 2) * y[i] for i in range(n)])
  sx3y: float = sum([(x[i] ** 3) * y[i] for i in range(n)])

  # calculate determinants for the Cramer's method
  d0 = det([[n, sx, sx2, sx3], [sx, sx2, sx3, sx4], [sx2, sx3, sx4, sx5], [sx3, sx4, sx5, sx6]])
  d1 = det([[sy, sx, sx2, sx3], [sxy, sx2, sx3, sx4], [sx2y, sx3, sx4, sx5], [sx3y, sx4, sx5, sx6]])
  d2 = det([[n, sy, sx2, sx3], [sx, sxy, sx3, sx4], [sx2, sx2y, sx4, sx5], [sx3, sx3y, sx5, sx6]])
  d3 = det([[n, sx, sy, sx3], [sx, sx2, sxy, sx4], [sx2, sx3, sx2y, sx5], [sx3, sx4, sx3y, sx6]])
  d4 = det([[n, sx, sx2, sy], [sx, sx2, sx3, sxy], [sx2, sx3, sx4, sx2y], [sx3, sx4, sx5, sx3y]])

  try:
    # calculate polynomial(3) approximation coefficients
    a = d1 / d0 # polynomial(3) approximation coefficient
    b = d2 / d0 # polynomial(3) approximation coefficient
    c = d3 / d0 # polynomial(3) approximation coefficient
    d = d4 / d0 # polynomial(3) approximation coefficient
    fi = [a + b * x_i + c * x_i ** 2 + d * x_i ** 3 for x_i in x] # approximate function with new coefficients

    # calculate determination coefficient
    numerator = [(y[i] - fi[i]) ** 2 for i in range(n)]
    denominator = [(y[i] - (sum(fi) / n)) ** 2 for i in range(n)]
    R2 = 1 - (sum(numerator) / sum(denominator))

    # coefficient calculation succeed: store results
    data['a'] = a
    data['b'] = b
    data['c'] = c
    data['d'] = d
    data['x'] = x
    data['y'] = y
    data['fi'] = fi
    data['R2'] = define_accuracy_str(R2)
    data['s'] = calc_s(y, fi)
    data['delta'] = calc_delta(y, fi)
    data['eps'] = [(fi[i] - y[i]) for i in range(len(fi)) ]

    if (d == 0 and c != 0):
      data['message'] = 'reduced to polynomial(2)'
    elif (d == 0 and c == 0):
      data['message'] = 'reduced to linear'
    else:
      data['message'] = ''
    return data
  except Exception:
    raise Exception('Unable to solve equation system with Cramer\'s method: division by zero is prohibited :C')

def exponential_func(x: List[float], y: List[float]):
  data: Dict = {}
  
  # check if data is invalid
  for i in y:
    if (i <= 0):
      data['error'] = 'Invalid input data format: non-positive y values are prohibited'
      return data
  
  # data seems valid - continue approximation
  
  # linearize the exponential formula
  n: int = len(y)
  lin_y: float = [log(y[i]) for i in range(n)]
  lin_result: Dict = linear_func(x, lin_y)

  # invert the linear results coefficients for the exponential approximation
  a = exp(lin_result['b'])
  b = lin_result['a']
  fi = [a * exp(b * x_i) for x_i in x]

  # calculate determination coefficient
  numerator = [(y[i] - fi[i]) ** 2 for i in range(n)]
  denominator = [(y[i] - (sum(fi) / n)) ** 2 for i in range(n)]
  R2 = 1 - (sum(numerator) / sum(denominator))

  # coefficient calculation succeed: store results
  data['a'] = a
  data['b'] = b
  data['x'] = x
  data['y'] = y
  data['fi'] = fi
  data['R2'] = define_accuracy_str(R2)
  data['s'] = calc_s(y, fi)
  data['delta'] = calc_delta(y, fi)
  data['eps'] = [(fi[i] - y[i]) for i in range(len(fi)) ]

  return data

def logarithmic_func(x: List[float], y: List[float]):
  data: Dict = {}

  # check if data is invalid
  for i in x:
    if (i <= 0):
      data['error'] = 'Invalid input data format: non-positive x values are prohibited'
      return data
  
  # approx using the logaritmic formula
  n: int = len(x)
  lin_x = [log(x[i]) for i in range(n)]
  lin_result: Dict = linear_func(lin_x, y)

  # calculate logarithmic approximation coefficients
  a = lin_result['a'] # logarithmic approximation coefficient
  b = lin_result['b'] # logarithmic approximation coefficient
  fi = [a * log(x_i) + b for x_i in x] # approximate function with new coefficients

  # calculate determination coefficient
  numerator = [(y[i] - fi[i]) ** 2 for i in range(n)]
  denominator = [(y[i] - (sum(fi) / n)) ** 2 for i in range(n)]
  R2 = 1 - (sum(numerator) / sum(denominator)) # determination coefficient

  # coefficient calculation succeed: store results
  data['a'] = a
  data['b'] = b
  data['x'] = x
  data['y'] = y
  data['fi'] = fi
  data['R2'] = define_accuracy_str(R2)
  data['s'] = calc_s(y, fi)
  data['delta'] = calc_delta(y, fi)
  data['eps'] = [(fi[i] - y[i]) for i in range(len(fi)) ]
  return data

def pow_func(x: List[float], y: List[float]):
  data: Dict = {}
  
  # check if data is invalid
  for i in range(len(x)):
    if x[i] <= 0 or y[i] <= 0:
      data['error'] = 'Invalid input data format: non-positive x or y values are prohibited'
      return data
  
  # data seems valid - continue approximation
  
  # linearize the pow formula
  n = len(x)
  lin_x = [log(x[i]) for i in range(n)]
  lin_y = [log(y[i]) for i in range(n)]
  lin_result = linear_func(lin_x, lin_y)

  # invert the linear results coefficients for the pow approximation
  a = exp(lin_result['b'])
  b = lin_result['a']
  fi = [a * x_i ** b for x_i in x]

  # calculate determination coefficient
  numerator = [(y[i] - fi[i]) ** 2 for i in range(n)]
  denominator = [(y[i] - (sum(fi) / n)) ** 2 for i in range(n)]
  R2 = 1 - (sum(numerator) / sum(denominator))

  # coefficient calculation succeed: store results
  data['a'] = a
  data['b'] = b
  data['x'] = x
  data['y'] = y
  data['fi'] = fi
  data['R2'] = define_accuracy_str(R2)
  data['s'] = calc_s(y, fi)
  data['delta'] = calc_delta(y, fi)
  data['eps'] = [(fi[i] - y[i]) for i in range(len(fi)) ]
  return data
