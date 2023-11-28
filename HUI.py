import customtkinter as CTK

class HUI:
    def __init__(self):
        self.Small_boxes = 1
        self.Medium_boxes = 2
        self.Large_boxes = 3

        self.Login_CTK()    #comment out to skip
        self.Main_frame()   #comment out to skip
        
    def Login_val(self, entry_name, entry_password, Main_login_frame):
        name = entry_name.get()
        password = entry_password.get()

        Data_login = {"Freek": "Verloop", "Janmartijn": "Lobregt", "Ibnu": "Yoga", "Mumtaz": "Rahmawan"}

        if name in Data_login and password == Data_login[name]:
            print("Login successful!")
            Main_login_frame.destroy()
        else:
            print("Incorrect username or password!")

    def Login_CTK(self):
        Main_login_frame = CTK.CTk()
        Main_login_frame.geometry("1920/2x1080/2")

        CTK.set_appearance_mode("dark")
        CTK.set_default_color_theme("dark-blue")

        Login_frame = CTK.CTkFrame(master=Main_login_frame)
        Login_frame.pack(pady=50, padx=60, fill="both", expand=True)

        Login_label = CTK.CTkLabel(master=Login_frame, text="Login System")
        Login_label.pack(pady=12, padx=10)

        entry_name = CTK.CTkEntry(master=Login_frame, placeholder_text="Username")
        entry_name.pack(pady=10, padx=30)

        entry_password = CTK.CTkEntry(master=Login_frame, placeholder_text="Password", show="*")
        entry_password.pack(pady=10, padx=30)

        login_button = CTK.CTkButton(master=Login_frame, text="Login", 
                                     command=lambda: self.Login_val
                                     (entry_name, entry_password, Main_login_frame))
        
        login_button.pack(pady=20, padx=50)

        Main_login_frame.mainloop()

    def Main_frame(self):
        while True:
            self.MainHUI_frame = CTK.CTk()
            self.MainHUI_frame.geometry("1920x1080")
            CTK.set_appearance_mode("dark")
            CTK.set_default_color_theme("dark-blue")

            Box_stack = CTK.CTkLabel(master=self.MainHUI_frame, text="Box Stacking", font=("Airal", 26))
            Box_stack.pack(pady=5, padx=150)
            Box_stack.place(x=50,y=30)

            Logout_button = CTK.CTkButton(master=self.MainHUI_frame,
                                          text="Log out", 
                                          font=("Airal", 10),
                                          command= self.Logout)
            Logout_button.pack(pady=20, padx=40)
            Logout_button.place(x=1380,y=10)

            Start_button = CTK.CTkButton(master=self.MainHUI_frame, 
                                        text="start",
                                        width= 500,
                                        height= 100,
                                        font=("Airal", 50), 
                                        command= "")
            Start_button.pack(pady=20, padx=100)

            self.Box_display("Small Odido", self.MainHUI_frame, 1, self.Small_boxes)
            self.Box_display("medium Odido", self.MainHUI_frame, 2, self.Medium_boxes)
            self.Box_display("Large Odido", self.MainHUI_frame, 3, self.Large_boxes)
            
            MainHUI = self.MainHUI_frame.mainloop()
            return MainHUI
    
    def Box_display(self, Name, master, count, size):
        master = master
        Label = CTK.CTkLabel(master=master, text= f"{Name} box", font=("Arial", 18))
        Label.pack(pady=0,padx=10)
        Label.place(x=10, y= 25*count + 50)
        counter = CTK.CTkLabel(master=master, text=f"{size}")
        counter.pack(pady=0,padx=10)
        counter.place(x=200,y=25*count+50)
        return Label,counter
    
    def Logout(self):
        self.MainHUI_frame.destroy()
        self.Login_CTK()

HUI()