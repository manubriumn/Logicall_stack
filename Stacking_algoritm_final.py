import storage as ST
import time
matrix = [-420]
L_coords1 = [(-755, -185),(-755, 81),(-755, 350)]
# L_coords1 = [(-965, -185), (-965, 81), (-965, 350)]
L_coords2 = [(-545, -185), (-545, 81), (-545, 350)]
#coords1 = [(-1065, -128), (-863, -128),(-1065, 270), (-863, 270)]
coords1 =  [(-863, -128),(-648, -128),(-863, 270),(-648, 280)]
coords2 = [(-648, -128), (-443, -128),(-648, 280), (-443, 280)]
coords3 = [(-230, 280), (-230, 280), (-230, -128), (-230, -128)]


def last_matrix(matrix):
    old_matrix = matrix
    print(old_matrix)
    return old_matrix

def place(size):
    coords_val = [False, False, False]

    height_size = {'s': 85, 'm': 125, 'l': 210, 'xl': 260}
    height = height_size[size]

    if size == 'xl':
        # if matrix[0] <= matrix[1]:  # Ensure index 1 doesn't exceed index 0
        matrix[0] += height
        coords_val[0] = True
        # else:
        #     extra_height = matrix[1] + height - matrix[0]
        #     matrix[0] += height + extra_height
        #     matrix[1] += extra_height
        #     coords_val[1] = True
    else:
        smallest = matrix.index(min(matrix))
        if smallest != 2:
            matrix[smallest] += height
        if smallest == 2:
            matrix[smallest] += height * 2
        coords_val[smallest] = True

    print(matrix)
    if all(value >= 1750 for value in matrix):
        return True, coords_val, height
    return False, coords_val, height

def coordinates(Coords_val, size, Height):
    index = Coords_val.index(True)
    if size == 'xl' and index == 0:
        L_coords_1 = [(x[0], x[1], matrix[0]) for x in L_coords1]
        return L_coords_1
    # elif size == 'xl' and index == 1:
    #     L_coords_2 = [(x[0], x[1], matrix[1]) for x in L_coords2]
    #     return L_coords_2
    elif size != 'xl' and index == 0:
        coords_1 = [(x[0], x[1], matrix[0]) for x in coords1]
        return coords_1
    elif size != 'xl' and index == 1:
        coords_2 = [(x[0], x[1], matrix[1]) for x in coords2]
        return coords_2
    elif size != 'xl' and index == 2:
        [(x[0], x[1], matrix[2]) for x in coords3]
        coords_3 = [(x[0], x[1], matrix[2] - Height) if i < 2 else (x[0], x[1], matrix[2]) for i, x in
                    enumerate(coords3)]
        return coords_3


def give_coords(coords):
    if len(coords) == 3:
        for i in range(3):
            place = coords[i]
            print(place)
    else:
        for i in range(4):
            place = coords[i]
            print(place)
    return place



if __name__ == '__main__':
    time.sleep(.1)
    print("start")
    _, size = ST.take_buf(ST.Buf)
    x, Coords_val, Height = place()
    coords = coordinates()
    print(coords)
    give_coords(coords)
