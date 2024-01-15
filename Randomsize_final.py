import random

sizes = []
size = ['s', 'm', 'l', 'xl']
def Random_size():
    if sizes == []:
        Fill_size()
    chosen_size = random.choice(sizes)
    sizes.remove(chosen_size)
    return chosen_size

def Fill_size():
    for i in range(14):
        sizes.append(size[0])
        sizes.append(size[1])
    for i in range(10):
        sizes.append(size[2])
    for i in range(6):
        sizes.append(size[3])


if __name__== '__main__':
    print(Random_size())
