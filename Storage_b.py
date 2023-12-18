from randomsize import Random_size as RS
import randomsize as Rdm
import time

def fill_buf():
    if len(Buf)< buf_size:
        for i in range (0,buf_size):
            size = RS()
            Buf.append(size)
            print(Buf)
    return Buf

def refill_buf():
    while True:
        time.sleep(0.1)
        while len(Buf) < buf_size:
            Buf.append(RS())
        return Buf

def take_buf(Buf):
    count_list = []
    print(Buf)
    count_list.append(Buf.count('s')), count_list.append(Buf.count('m')), count_list.append(Buf.count('l')), count_list.append(Buf.count('xl'))
    print(count_list)
    for i in range(4):
        if count_list[i] >= 4 or count_list[3] >= 3:
            if i == 0 : take_size = 's'
            if i == 1 : take_size = 'm'
            if i == 2 : take_size = 'l'
            if i == 3 : take_size = 'xl'
    time.sleep(0.1)
    if take_size in Rdm.sizes:
        if take_size != 'xl':
            for i in range(0,4):
                Buf.remove(take_size)
                refill_buf()
                print(Buf)
        else:
            for i in range(0,3):
                Buf.remove(take_size)
                refill_buf()
                print(Buf)
    return Buf, take_size

buf_size = 9
Buf = []
if __name__ == '__main__':
    fill_buf()
