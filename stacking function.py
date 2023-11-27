height_small_box = 1
height_medium_box = 2
height_large_box = 3
max_height_pallet = 5
stacking_matrix =  [
        [0,0,0,0],
        [0,0,0,0]
                ]

def boxes(box_size):
    sizes = {'small': height_small_box, 'medium': height_medium_box, 'large': height_large_box}
    if box_size in sizes:
       return sizes.get(box_size) 

def stack(box_size_val, stacking_matrix = None):
        
    if len(stacking_matrix) != 2 or any(len(row) != 4 for row in stacking_matrix):
        return "not in matrix, expected a 2x4 matrix."
    
    min_waarde = min(min(row) for row in stacking_matrix)
    min_index = [(i, j) for i, row in enumerate(stacking_matrix) for j, val in enumerate(row) if val == min_waarde][0]

    stacking_matrix[min_index[0]][min_index[1]] += box_size_val

    return stacking_matrix

while any(val <= max_height_pallet for row in stacking_matrix for val in row):
    box_size_val = boxes(input('fill in size:'))
    print(f'size:',box_size_val)
    stacking_matrix = stack(box_size_val, stacking_matrix)
    print(stacking_matrix)
