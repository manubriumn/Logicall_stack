from randomsize import Random_size as RS
import randomsize as Rdm
import time

def count():
    count_list = []
    count_list.append(Buf.count('s')), count_list.append(Buf.count('m')), count_list.append(Buf.count('l')), count_list.append(Buf.count('xl'))
    return count_list

def fill_buf():
    if len(Buf) < buf_size:
        for i in range(len(Buf), buf_size):
            size = RS()
            Buf.append(size)

    return Buf

def refill_buf():
    while True:
        last_buf = Buf
        while len(Buf) < buf_size:
            Buf.append(RS())

        return Buf

def take_buf(Buf):



    count_list = []

    count_list.append(Buf.count('s')), count_list.append(Buf.count('m')), count_list.append(
        Buf.count('l')), count_list.append(Buf.count('xl'))


    # Find the index of the maximum count
    max_count_index = count_list.index(max(count_list))

    take_size = ''
    if count_list[max_count_index] >= 4 or count_list[3] >= 3:
        if max_count_index == 0: take_size = 's'
        elif max_count_index == 1 and take_size == '' : take_size = 'm'
        elif max_count_index == 2 and take_size == '' : take_size = 'l'
        elif max_count_index == 3 and take_size == '' : take_size = 'xl'

    time.sleep(0.1)
    if take_size in Rdm.sizes:
        if take_size != 'xl':
            for i in range(4):
                # Remove only one occurrence at a time
                Buf.remove(take_size)

        else:
            for i in range(3):
                # Remove only one occurrence at a time
                Buf.remove(take_size)

    return Buf, take_size

buf_size = 12
Buf = []
count_list = []
if __name__ == '__main__':
    fill_buf()
