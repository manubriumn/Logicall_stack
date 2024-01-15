import time
from threading import Thread
from download import Download as DL
import doosan2
import vision_check
import barcode_scanner
import storage
import customtkinter as CTK


class HUI:
    def __init__(self, Login_val):
        time.sleep(1)
        self.Login_val = Login_val
        if self.Login_val:
            self.Main_frame()
        else:
            exit()

    def start(self):
        robot = Thread(target=doosan2.run)
        robot.start()

    def box_vision(self):
        vision1 = Thread(target=vision_check.look_vision())
        vision1.start()

    def barcode_vision(self):
        vision2 = Thread(target=barcode_scanner.look_barcode())
        vision2.start()

    def Main_frame(self):
        self.MainHUI_frame = CTK.CTk()
        self.MainHUI_frame.geometry(f"{1920 - 960}x{1080 / 2}")
        CTK.set_appearance_mode("dark")
        CTK.set_default_color_theme("dark-blue")

        Box_stack = CTK.CTkLabel(master=self.MainHUI_frame, text="Box Buffer", font=("Arial", 40))
        Box_stack.pack(pady=5, padx=150)
        Box_stack.place(x=50, y=30)

        Logout_button = CTK.CTkButton(master=self.MainHUI_frame,
                                      text="Log out",
                                      font=("Arial", 18),
                                      command=self.Logout)
        Logout_button.pack(pady=20, padx=40)
        Logout_button.place(x=1350, y=50)

        if not self.Login_val:
            quit()

        Start_button = CTK.CTkButton(master=self.MainHUI_frame,
                                     text="start",
                                     width=550,
                                     height=100,
                                     fg_color="green",
                                     font=("Arial", 50),
                                     command=self.start)
        Start_button.pack(pady=20, padx=100), Start_button.place(x=500, y=50)

        Vision_button = CTK.CTkButton(master=self.MainHUI_frame,
                                      text="Vision Robot",
                                      width=550,
                                      height=100,
                                      font=("Arial", 50),
                                      command=self.box_vision)
        Vision_button.pack(pady=20, padx=100), Vision_button.place(x=500, y=175)

        Vision_button2 = CTK.CTkButton(master=self.MainHUI_frame,
                                       text="Vision barcode",
                                       width=550,
                                       height=100,
                                       font=("Arial", 50),
                                       command=self.barcode_vision)
        Vision_button2.pack(pady=20, padx=100), Vision_button2.place(x=500, y=300)

        Download_button = CTK.CTkButton(master=self.MainHUI_frame,
                                        text="Download excel",
                                        width=550,
                                        height=100,
                                        font=("Arial", 50),
                                        command=self.Download)
        Download_button.pack(pady=20, padx=100), Download_button.place(x=500, y=425)

        self.box_displays = []
        box = ['small', 'medium', 'large', 'extra large', 'wanted size']
        for pallet_index in range(len(box)):
            label, palleter = self.Box_display(f"{box[pallet_index]}", self.MainHUI_frame, pallet_index, 0)
            self.box_displays.append((label, palleter))

        self.Update_boxes_periodically()

        self.MainHUI_frame.mainloop()

    def Box_display(self, Name, master, Pallet: int, count_var):
        Label = CTK.CTkLabel(master=master, text=f"{Name} box", font=("Arial", 26))
        Label.pack(pady=0, padx=10)
        Label.place(x=10, y=50 * Pallet + 100)

        Palleter = CTK.CTkLabel(master=master, text=f"{None}", font=("Arial", 26))
        Palleter.pack(pady=0, padx=10)
        Palleter.place(x=300, y=50 * Pallet + 100)

        return Label, Palleter

    def Logout(self):
        self.MainHUI_frame.destroy()
        self.Login_val = False
        return self.Login_val

    def Download(self):
        download_instance = DL()
        download_instance.download()

    def Box_counts(self):
        count_list = storage.count()

        if sum(count_list) >= 11:
            last_buf = count_list.copy()  # Create a copy of count_list to store the last buffer
            sizes = {0: 'small', 1: 'medium', 2: 'large', 3: 'extra large'}
            count_list.append(sizes[count_list.index(max(count_list))])
        return count_list

    def Update_boxes_periodically(self):
        box_counts = self.Box_counts()

        for pallet_index in range(len(box_counts)):
            label, palleter = self.box_displays[pallet_index]
            palleter.configure(text=box_counts[pallet_index])

        self.MainHUI_frame.after(1000, self.Update_boxes_periodically)


if __name__ == '__main__':
    HUI(Login_val=True)
