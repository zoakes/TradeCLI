import fire

def add(x, y):
  return x + y

def multiply(x, y):
  return x * y

if __name__ == '__main__':
  fire.Fire()


  # $ python example.py add 10 20
  # 30
  # $ python example.py multiply 10 20
  # 200