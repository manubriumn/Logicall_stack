"""
measurements:               [LxWxH]
small box measurements :    [400x205x85]
medium box measurements:    [400x205x125]
large box measurements:     [400x205x165]
extra large measurements:   [420x260x260]
"""

class Stacking_boxes():
    def __init__(self):
        self.height_small_box = 85
        self.height_medium_box = 125
        self.height_large_box = 165
        self.height_extralarge_box = 260
        self.max_height_pallet = 1000
        self.stacking_matrix = [
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]
                                ]
        self.box_Pallets = {'small': 0, 'medium': 0, 'large': 0, 'extra large': 0}

    def boxes(self, box_size):
        sizes = {'small': self.height_small_box,
                'medium': self.height_medium_box,
                'large': self.height_large_box,
                'extra large': self.height_extralarge_box}
        
        if box_size in sizes:
            return sizes.get(box_size)
        return 0

    def stack(self, box_size_val):
        if len(self.stacking_matrix) != 2 or any(len(row) != 5 for row in self.stacking_matrix):
            return "Not in matrix, expected a 2x4 matrix."

        min_waarde = min(min(row) for row in self.stacking_matrix)
        min_index = [(i, j) for i, row in enumerate(self.stacking_matrix) for j, val in enumerate(row) if val == min_waarde][0]

        self.stacking_matrix[min_index[0]][min_index[1]] += box_size_val

        return self.stacking_matrix

    def Smallest_stack(self, Input_val= "" ):
        while any(val <= self.max_height_pallet for row in self.stacking_matrix for val in row):
            box_size = input(f'Fill in size (small/medium/large): ')
            box_size_val = self.boxes(box_size)
            print(f'Size: {box_size_val}')
            self.stacking_matrix = self.stack(box_size_val)
            print(self.stacking_matrix)
            if box_size_val > 0:
                self.update_Pallets(box_size)
            self.show_box_Pallets()
    
    def update_Pallets(self, box_size):
        Box_list = [0,0,0,0]
        if box_size == 'small':
            self.box_Pallets['small'] += 1
            Box_list[0]+=1
        elif box_size == 'medium':
            self.box_Pallets['medium'] += 1
            Box_list[1]+=1
        elif box_size == 'large':
            self.box_Pallets['large'] += 1
            Box_list[2]+=1
        elif box_size == 'extra large':
            self.box_Pallets['extra large'] += 1
            Box_list[3]+=1
        return Box_list

    def show_box_Pallets(self):
        print("Box Pallets:")
        for box_size, Pallet in self.box_Pallets.items():
            print(f"{box_size.capitalize()} boxes: {Pallet}")

if __name__ == '__main__':
    stacker = Stacking_boxes()
    stacker.Smallest_stack()
if __name__ == '__Download':
    stacker.update_Pallets()
else: 
    Stacking_boxes()
