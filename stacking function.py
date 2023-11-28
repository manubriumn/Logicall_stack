class Stacking_boxes:
    def __init__(self):
        self.height_small_box = 1
        self.height_medium_box = 2
        self.height_large_box = 3
        self.max_height_pallet = 2
        self.stacking_matrix = [
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.box_counts = {'small': 0, 'medium': 0, 'large': 0}
        self.Smallest_stack()

    def boxes(self, box_size):
        sizes = {'small': self.height_small_box, 'medium': self.height_medium_box, 'large': self.height_large_box}
        if box_size in sizes:
            return sizes.get(box_size)
        return 0  # Return 0 als de doosmaat niet overeenkomt met de gedefinieerde maten

    def stack(self, box_size_val):
        if len(self.stacking_matrix) != 2 or any(len(row) != 4 for row in self.stacking_matrix):
            return "Not in matrix, expected a 2x4 matrix."

        min_waarde = min(min(row) for row in self.stacking_matrix)
        min_index = [(i, j) for i, row in enumerate(self.stacking_matrix) for j, val in enumerate(row) if val == min_waarde][0]

        self.stacking_matrix[min_index[0]][min_index[1]] += box_size_val

        return self.stacking_matrix

    def Smallest_stack(self):
        while any(val <= self.max_height_pallet for row in self.stacking_matrix for val in row):
            box_size = input('Fill in size (small/medium/large): ')
            box_size_val = self.boxes(box_size)
            print(f'Size: {box_size_val}')
            self.stacking_matrix = self.stack(box_size_val)
            print(self.stacking_matrix)
            if box_size_val > 0:
                self.update_counts(box_size)
    
    def update_counts(self, box_size):
        if box_size == 'small':
            self.box_counts['small'] += 1
        elif box_size == 'medium':
            self.box_counts['medium'] += 1
        elif box_size == 'large':
            self.box_counts['large'] += 1

    def show_box_counts(self):
        print("Box counts:")
        for box_size, count in self.box_counts.items():
            print(f"{box_size.capitalize()} boxes: {count}")

main = Stacking_boxes()
main.show_box_counts()