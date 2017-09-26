import math
import re
integers_regex = re.compile(r'\b[\d\.]+\b')

def calc(expr, advanced=False):
   def safe_eval(expr, symbols={}):
       return eval(expr, dict(__builtins__=None), symbols)
   def whole_number_to_float(match):
       group = match.group()
       if group.find('.') == -1:
           return group + '.0'
       return group
   expr = expr.replace('^', '**')
   expr = integers_regex.sub(whole_number_to_float, expr)
   if advanced:
       return safe_eval(expr, vars(math))
   else:
       return safe_eval(expr)

e = calc('12+2/3*3-6')
print e