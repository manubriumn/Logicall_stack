import random

sizes = ['s', 'm', 'l', 'xl']
def Random_size():
    chosen_size = random.choice(sizes)
    return chosen_size
if __name__ == '__main__':
    Random_size()
