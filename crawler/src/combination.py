from itertools import product 

def generate_combine(filter_dict):
  keys = list(filter_dict.keys()) # key 값 
  value_lists = [list(filter_dict[key].keys()) for key in keys] # value값

  for combined in product(*value_lists): # 동적 인자로 변경 파라미터 값이 유동적이라서
    yield dict(zip(keys, combined))