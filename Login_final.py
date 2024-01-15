import customtkinter as CTK
import time


class Login():
    def __init__(self):
        time.sleep(1)
        self.Login_CTK()  # comment out to skip

    def Login_val(self, entry_name, entry_password, Main_login_frame):
        name = entry_name.get()
        password = entry_password.get()
        self.Login_val = False
        Data_login = {"Freek": "Verloop", "Janmartijn": "Lobregt", "Ibnu": "Yoga", "Mumtaz": "Rahmawan", "": ""}
        time.sleep(1)
        if name in Data_login and password == Data_login[name]:
            print("Login successful!")
            Main_login_frame.destroy()
            self.Login_val = True
            return self.Login_val
        else:
            print("Incorrect username or password!")

    def Login_CTK(self):
        time.sleep(1)
        Main_login_frame = CTK.CTk()
        Main_login_frame.geometry("1920/2x1080/2")

        CTK.set_appearance_mode("dark")
        CTK.set_default_color_theme("dark-blue")

        Login_frame = CTK.CTkFrame(master=Main_login_frame)
        Login_frame.pack(pady=50, padx=60, fill="both", expand=True)

        Login_label = CTK.CTkLabel(master=Login_frame, text="Login System")
        Login_label.pack(pady=12, padx=10)

        self.entry_name = CTK.CTkEntry(master=Login_frame, placeholder_text="Username")
        self.entry_name.pack(pady=10, padx=30)

        self.entry_password = CTK.CTkEntry(master=Login_frame, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=10, padx=30)

        login_button = CTK.CTkButton(master=Login_frame, text="Login", command=lambda:
        self.Login_val(self.entry_name, self.entry_password, Main_login_frame))

        login_button.pack(pady=20, padx=50)

        Main_login_frame.mainloop()


Log = Login()
Login = Log.Login_val
