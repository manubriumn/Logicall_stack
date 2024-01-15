import openpyxl as xl
from Stacking_function import Stacking_boxes as SB

class Download():
    def __init__(self):
        self.Download_file = xl.load_workbook("Download.xlsx")
        self.Sheet = self.Download_file.active
        self.Sheet.title = "info stacked pallets"
        #self.Add_boxes()
        self.Head_key()
        self.Save()

    def Head_key(self):
        self.Sheet.insert_rows(1)
        self.Sheet['A1'] = 'Pallet'
        self.Sheet['B1'] = 'Small'
        self.Sheet['C1'] = 'Medium'
        self.Sheet['D1'] = 'Large'
        self.Sheet['E1'] = 'Extra Large'
    
    # def Add_boxes(self):
    #     Box_list = SB.update_Pallets
    #     self.Sheet[f'A{Pallet}'] = f'{Box_list[0]}'
    #     self.Sheet[f'B{Pallet}'] = f'{Box_list[1]}'
    #     self.Sheet[f'C{Pallet}'] = f'{Box_list[2]}'
    #     self.Sheet[f'D{Pallet}'] = f'{Box_list[3]}'
    #     self.Sheet[f'E{Pallet}'] = f'{Box_list[4]}'
    #     pallet =+ 1
        
    def Save(self):
        self.Download_file.save("Download.xlsx")

if __name__ == '__main__':
    Pallet = 1
    Download()
