from customtkinter import *
from typing import *

from approximation import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure, Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from error_window import ErrorWindow
from os import stat, path
import numpy as np

CURRENT_RESULT: str = None

root: CTk = CTk()
root.geometry('700x900')
root.title('LAB4: comp-math')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

x_values_input: CTkEntry = CTkEntry(root, placeholder_text='Enter x values separated by space: ', width=240)
x_values_input.grid(row=0, pady=3)

y_values_input: CTkEntry = CTkEntry(root, placeholder_text='Enter y values separated by space: ', width=240)
y_values_input.grid(row=1, pady=3)

calculate_btn: CTkButton = CTkButton(root, text='Calculate (ui)', command=lambda: perform_calculation_ui())
calculate_btn.grid(row=2, pady=3)

input_filename: CTkEntry = CTkEntry(root, placeholder_text='Input file: ', width=100)
input_filename.grid(row=3, pady=3)

calculate_btn: CTkButton = CTkButton(root, text='Calculate (file)', command=lambda: perform_calculation_file())
calculate_btn.grid(row=4, pady=3)

output_filename: CTkEntry = CTkEntry(root, placeholder_text='Output file: ', width=100)
output_filename.grid(row=5, pady=3)

calculate_btn: CTkButton = CTkButton(root, text='Save', command=lambda: perform_result_save())
calculate_btn.grid(row=6, pady=3)


def parse_data(x_line: str, y_line: str) -> Tuple[List[float], List[float]]:
  try:
    x_vals: List[float] = [ float(xv) for xv in x_line.strip().replace(',', '.').split(' ') ]
    y_vals: List[float] = [ float(yv) for yv in y_line.strip().replace(',', '.').split(' ') ]
  except ValueError:
    raise Exception('Inappropriate data. Dumb user :C')
  
  if len(x_vals) != len(y_vals):
    raise Exception('Amounts of points are not equal.')

  if len(x_vals) < 8 or len(x_vals) > 12:
    raise Exception('Should be provided from 8 to 12 x-points.')
    
  if len(y_vals) < 8 or len(y_vals) > 12:
    raise Exception('Should be provided from 8 to 12 y-points.')

  if all(x == x_vals[0] for x in x_vals) and all(y == y_vals[0] for y in y_vals):
    raise Exception('Invalid data provided: that\'s a point, not a function')
  
  if all(x == x_vals[0] for x in x_vals) and any(y != y_vals[0] for y in y_vals):
    raise Exception('Invalid data provided: function cannot have different values on the same x')

  return (x_vals, y_vals)

def read_data_file(name: str) -> Tuple[List[float], List[float]]:
  name = name.strip()
  if not path.exists(name) or not path.isfile(name):
    raise Exception('File does not exist or file is not a file. :C')

  if not os.access(name, os.R_OK):
    raise Exception('File is not readable: lack of permissions')
  
  f = open(name, 'r')
  x_vals_str = f.readline()
  y_vals_str = f.readline()
  f.close()

  return parse_data(x_vals_str, y_vals_str)

def read_data_ui() -> Tuple[List[float], List[float]]:
  return parse_data(x_values_input.get(), y_values_input.get())

def draw_plots(ax: Axes, data: Tuple[List[float], List[float]], prepared_data: Dict[str, Dict]):
  ax.scatter(data[0], data[1], label="Исходные точки")
  plt.xlabel("x")
  plt.ylabel("y")
  ax.grid(True)

  x = np.arange(min(data[0]), max(data[1]), 0.01)
  ax.set_xlim(min(data[0]) - 0.5, max(data[0]) + 0.5)
  ax.set_ylim(min(data[1]) - 0.5, max(data[1]) + 0.5)
  ax.plot(x, prepared_data['linearf']['a'] * x + prepared_data['linearf']['b'], color='r', label='lin')
  ax.plot(x, prepared_data['polynomial_2f']['c'] * x ** 2 + prepared_data['polynomial_2f']['b'] * x + prepared_data['polynomial_2f']['a'], color='g', label='p_2')
  ax.plot(x, prepared_data['polynomial_3f']['d'] * x ** 3 + prepared_data['polynomial_3f']['c'] * x ** 2 + prepared_data['polynomial_3f']['b'] * x + prepared_data['polynomial_3f']['a'], color='b', label='p_3')
  
  if (prepared_data['exponentialf'].get('error') == None):
    ax.plot(x, prepared_data['exponentialf']['a'] * np.exp(prepared_data['exponentialf']['b'] * x), color='y', label='exp')
  
  if (prepared_data['logarithmicf'].get('error') == None):
    ax.plot(x, prepared_data['logarithmicf']['a'] * np.log(x) + prepared_data['logarithmicf']['b'], color='m', label='log')
  
  if (prepared_data['powf'].get('error') == None):
    ax.plot(x, prepared_data['powf']['a'] * x ** prepared_data['powf']['b'], color='c', label='pow')
  
  ax.legend()

def perform_calculation_ui():
  try:
    data: Tuple[List[float], List[float]] = read_data_ui()
    prepared_data: Dict[str, Dict] = prepare_results_data(data)
    prepared_text: str = prepare_result_text(prepared_data)
    global CURRENT_RESULT
    CURRENT_RESULT = prepared_text

    results: CTk = CTkToplevel(master=root)
    results.geometry('1700x900')
    results.title('Results')
    scrollable_frame: CTkScrollableFrame = CTkScrollableFrame(results, width=1680, height=900)
    scrollable_frame.grid(row=0)

    text: CTkLabel = CTkLabel(scrollable_frame, text=prepared_text)
    fig: Figure = plt.figure(figsize=(10,10))
    ax: Axes = fig.add_subplot(1, 1, 1)
    draw_plots(ax, data, prepared_data)
    canvas: FigureCanvasTkAgg = FigureCanvasTkAgg(figure=fig, master=scrollable_frame)
    canvas.draw()

    text.pack()
    canvas.get_tk_widget().pack()
    results.mainloop()
  except BaseException as e:
    error_window: ErrorWindow = ErrorWindow(message=e.args[0], master=root)

def perform_calculation_file():
  try:
    if (len(input_filename.get().strip()) == 0):
      raise Exception('Invalid input file name')

    data: Tuple[List[float], List[float]] = read_data_file(input_filename.get().strip())
    prepared_data: Dict[str, Dict] = prepare_results_data(data)
    prepared_text: str = prepare_result_text(prepared_data)
    global CURRENT_RESULT
    CURRENT_RESULT = prepared_text

    results: CTk = CTkToplevel(master=root)
    results.geometry('1700x900')
    results.title('Results')
    scrollable_frame: CTkScrollableFrame = CTkScrollableFrame(results, width=1680, height=900)
    scrollable_frame.grid(row=0)

    text: CTkLabel = CTkLabel(scrollable_frame, text=prepared_text)
    fig: Figure = plt.figure(figsize=(10,10))
    ax: Axes = fig.add_subplot(1, 1, 1)
    draw_plots(ax, data, prepared_data)
    canvas: FigureCanvasTkAgg = FigureCanvasTkAgg(figure=fig, master=scrollable_frame)
    canvas.draw()

    text.pack()
    canvas.get_tk_widget().pack()
    results.mainloop()
  except BaseException as e:
    error_window: ErrorWindow = ErrorWindow(message=e.args[0], master=root)

def perform_result_save():
  if (len(output_filename.get().strip()) == 0):
    error_window: ErrorWindow = ErrorWindow(message='Invalid output file name', master=root)
    return
  
  global CURRENT_RESULT
  f = open(output_filename.get().strip(), 'w')
  f.write(CURRENT_RESULT)
  f.close()
  CURRENT_RESULT = None

def prepare_results_data(results_data: Tuple[List[float], List[float]]) -> Dict[str, Dict]:
  prepared_results: Dict[str, Dict] = {}

  prepared_results['linearf'] = linear_func(results_data[0], results_data[1])
  prepared_results['polynomial_2f'] = polynomial_2_func(results_data[0], results_data[1])
  prepared_results['polynomial_3f'] = polynomial_3_func(results_data[0], results_data[1])
  prepared_results['exponentialf'] = exponential_func(results_data[0], results_data[1])
  prepared_results['logarithmicf'] = logarithmic_func(results_data[0], results_data[1])
  prepared_results['powf'] = pow_func(results_data[0], results_data[1])
  
  return prepared_results

def prepare_result_text(approx_data: Dict[str, Dict]) -> str:
  linearf: Dict = approx_data['linearf']
  linear_text_part: str = f"""
  Linear
  coefficients: 
    a: {linearf['a']}
    b: {linearf['b']}

  data:
    x: {linearf['x']}
    y: {linearf['y']}
    fi: {linearf['fi']}

  correlation coefficient: {linearf['r']}
  measure of deviation: { linearf['s'] }
  standard deviation: {linearf['delta']}
  determination: {linearf['R2']}
  eps: { linearf['eps'] }
  ----------------------------------------
  """

  polynomial_2f: Dict = approx_data['polynomial_2f']
  polynomial_2f_text_part: str = f"""
  Polynomial(2){': ' + polynomial_2f['message'] if polynomial_2f['message'] else ''}
  coefficients:
    a: {polynomial_2f['a']}
    b: {polynomial_2f['b']}
    c: {polynomial_2f['c']}

  data:
    x: {polynomial_2f['x']}
    y: {polynomial_2f['y']}
    fi: {polynomial_2f['fi']}

  measure of deviation: { polynomial_2f['s'] }
  standard deviation: {polynomial_2f['s']}
  determination: {polynomial_2f['R2']}
  eps: { polynomial_2f['eps'] }
  ----------------------------------------
  """
  
  polynomial_3f: Dict = approx_data['polynomial_3f']
  polynomial_3f_text_part: str = f"""
  Polynomial(3){': ' + polynomial_3f['message'] if polynomial_3f['message'] else ''}
  coefficients: 
    a: {polynomial_3f['a']}
    b: {polynomial_3f['b']}
    c: {polynomial_3f['c']}
    d: {polynomial_3f['d']}

  data:
    x: {polynomial_3f['x']}
    y: {polynomial_3f['y']}
    fi: {polynomial_3f['fi']}

  measure of deviation: { polynomial_3f['s'] }
  standard deviation: {polynomial_3f['s']}
  determination: {polynomial_3f['R2']}
  eps: { polynomial_3f['eps'] }
  ----------------------------------------
  """

  exponentialf: Dict = approx_data['exponentialf']
  exponentialf_text_part: str = f"""
  Exponential
  coefficients:
    a: {exponentialf['a']}
    b: {exponentialf['b']}
        
  data:
    x: {exponentialf['x']}
    y: {exponentialf['y']}
    fi: {exponentialf['fi']}

  measure of deviation: { exponentialf['s'] }
  standard deviation: {exponentialf['s']}
  determination: {exponentialf['R2']}
  eps: { exponentialf['eps'] }
  ----------------------------------------
  """ if exponentialf.get('error') == None else exponentialf.get('error')

  logarithmicf: Dict = approx_data['logarithmicf']
  lofarithmicf_text_part: str = f"""
  Logarithmic
  coefficients: 
    a: {logarithmicf['a']}
    b: {logarithmicf['b']}
        
  data:
    x: {logarithmicf['x']}
    y: {logarithmicf['y']}
    fi: {logarithmicf['fi']}

  measure of deviation: { logarithmicf['s'] }
  standard deviation: {logarithmicf['s']}
  determination: {logarithmicf['R2']}
  eps: { logarithmicf['eps'] }
  ----------------------------------------
  """ if logarithmicf.get('error') == None else logarithmicf.get('error')

  powf: Dict = approx_data['powf']
  powf_text_part: str = f"""
  Pow
  coefficients: 
    a: {powf['a']}
    b: {powf['b']}
        
  data:
    x: {powf['x']}
    y: {powf['y']}
    fi: {powf['fi']}

  measure of deviation: { powf['s'] }
  standard deviation: {powf['s']}
  determination: {powf['R2']}
  eps: { powf['eps'] }
  ----------------------------------------
  """ if powf.get('error') == None else powf.get('error')

  min_deltas: List[float] = [linearf['delta'], polynomial_2f['delta'], polynomial_3f['delta']]
  if (exponentialf.get('error') == None):
    min_deltas.append(exponentialf['delta'])
  
  if (logarithmicf.get('error') == None):
    min_deltas.append(logarithmicf['delta'])

  if (powf.get('error') == None):
    min_deltas.append(powf['delta'])

  min_delta = min(min_deltas)
  best = []
  if linearf['delta'] == min_delta:
    best.append('Linear')
  if polynomial_2f['delta'] == min_delta:
    best.append('Polynomial(2)')
  if polynomial_3f['delta'] == min_delta:
    best.append('Polynomial(3)')
  if exponentialf.get('error') == None and exponentialf['delta'] == min_delta:
    best.append('Exponential')
  if logarithmicf.get('error') == None and logarithmicf['delta'] == min_delta:
    best.append('Logarithmic')
  if powf.get('error') == None and powf['delta'] == min_delta:
    best.append('Pow')
  
  best_approx_text_part: str = f"""
  Best approximation provided by: { best }
  """

  result_text: str = linear_text_part + polynomial_2f_text_part + polynomial_3f_text_part + exponentialf_text_part + lofarithmicf_text_part + powf_text_part + best_approx_text_part
  return result_text

if __name__ == '__main__':
  root.mainloop()
