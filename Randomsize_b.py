import random

sizes = ['s', 's','s']
def Random_size():
    chosen_size = random.choice(sizes)
    return chosen_size
if __name__ == '__main__':
    Random_size()
