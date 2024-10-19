import tkinter as tk
from tkinter import *
from customtkinter import CTkEntry, CTkButton
from PIL import Image, ImageTk
from datetime import datetime
import locale
import random
import string
from ar.page4ar import Page4AR

class Page3AR:
    def __init__(self, master, main_app, cursor, conn):
        self.master = master
        self.main_app = main_app  # Save the MainApplication instance
        self.cursor = cursor  # Save the cursor
        self.conn = conn  # Save the conn
        self.setup_gui()

    def setup_gui(self):
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

        self.master.title("AMAN")
        self.master.iconbitmap("image/AMAN-LOGO.ico")
        self.master.geometry("800x480")
        self.master.minsize(800, 480)
        self.master.maxsize(800, 480)
        self.master.config(bg="#F2F7F9")

        self.frm1 = tk.Frame(self.master, bg="#1679EF", height=50)
        self.frm1.pack(fill=tk.X, side=tk.TOP, pady=15)

        # Load and display logo image
        self.old_image_frm1 = Image.open("image/AMAN-BLEU.png")
        self.resized_frm1 = self.old_image_frm1.resize((60, 50), Image.LANCZOS)
        self.new_image_frm1 = ImageTk.PhotoImage(self.resized_frm1)
        self.label1 = tk.Label(
            self.frm1, image=self.new_image_frm1, highlightthickness=0, bd=0
        )
        self.label1.image = self.new_image_frm1  # Keep a reference to the image object
        self.label1.pack(expand=tk.YES)

        self.frm2 = tk.Frame(self.master, bg="#F2F7F9", height=360, width=800)

        # Display message
        self.label_msg = tk.Label(
            self.frm2,
            text="الرجاء إدخال رقم بطاقة الهوية البيومترية الخاصة بك",
            font=("Arial", 18, "bold"),
            fg="#095CD3",
            bg="#F2F7F9",
        )
        self.label_msg.place(x=345, y=25)

        # Entry field
        self.entry = CTkEntry(
            master=self.frm2,
            font=("Arial", 23, "bold"),
            fg_color="#F2F7F9",
            border_width=2,
            width=365,
            border_color="#1679EF",
            corner_radius=4,
            text_color="black",
            height=50,
        )
        self.entry.place(x=370, y=90)

        self.error_label = Label(
            self.frm2,
            text="",
            font=("Arial", 12),
            fg="red",
            bg="#F2F7F9",
        )
        self.error_label.place(x=370, y=140)

        # Register button
        self.btn = CTkButton(
            master=self.frm2,
            text="تسجيل",
            font=("Arial", 27),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=355,
            height=50,
            border_width=0,
            corner_radius=4,
            command=self.save_and_switch,
        )
        self.btn.place(x=375, y=200)

        # Exit button
        self.btn_srt = CTkButton(
            master=self.frm2,
            text="خروج",
            font=("Arial", 20),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=100,
            height=30,
            border_width=0,
            corner_radius=3,
            command=self.return_to_main,
        )
        self.btn_srt.place(x=40, y=320)

        # Arrows
        self.image_flch = Image.open("image/fleche3.png")
        self.img_flch = ImageTk.PhotoImage(self.image_flch)
        self.label_flch = tk.Label(self.frm2, image=self.img_flch, bg="#F2F7F9")
        self.label_flch.image = self.img_flch  # Keep a reference to the image object
        self.label_flch.place(x=730, y=194)

        self.image_flch2 = Image.open("image/fleche3.png")
        self.rotated_img = self.image_flch2.rotate(180)
        self.resize = self.rotated_img.resize((35, 35), Image.LANCZOS)
        self.img_flch2 = ImageTk.PhotoImage(self.resize)
        self.label_flch2 = tk.Label(self.frm2, image=self.img_flch2, bg="#F2F7F9")
        self.label_flch2.image = self.img_flch2  # Keep a reference to the image object
        self.label_flch2.place(x=1, y=316)

        # Identity image
        self.image_identite = Image.open("ar/image/identite_ar.png")
        self.resize_identite = self.image_identite.resize((250, 170), Image.LANCZOS)
        self.img_identite = ImageTk.PhotoImage(self.resize_identite)
        self.label_img = tk.Label(self.frm2, image=self.img_identite, bg="#F2F7F9")
        self.label_img.image = self.img_identite  # Keep a reference to the image object
        self.label_img.place(x=55, y=20)

        self.frm2.pack()

        self.frm3 = tk.Frame(self.master, bg="#1679EF", height=30)
        self.date = datetime.now()
        self.label2 = tk.Label(
            self.frm3,
            text=f"{self.date:%d-%m-%Y}  /  {self.date:%I:%M}",
            font=("Arial", 12),
            fg="#F2F7F9",
            bg="#1679EF",
        )
        self.label2.pack(expand=tk.YES)
        self.frm3.pack(fill=tk.X, side=tk.BOTTOM)

    def validate_username(self, username):
        # Check if the username consists only of numbers and is between 6 to 9 digits long
        if username.isdigit() and 6 <= len(username) <= 9:
            return True
        else:
            return False

    def switch_to_page4ar(self):
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Create an instance of LanguageInterface from page2.py
        page4fr = Page4AR(self.master, self, self.cursor, self.conn)

    def return_to_main(self):
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Hide the language interface
        # Show the main interface
        self.main_app.switch_to_main_interface()

    def generate_password(self):
        # Generate a random password of 6 digits
        password = "".join(random.choices(string.digits, k=6))
        return password

    def save_to_database(self):
        entry_text = self.entry.get()
        # Generate a password
        password = self.generate_password()

        # Execute SQL command to insert data into the person table
        self.cursor.execute(
            """INSERT INTO person (username, password) VALUES (?, ?)""",
            (entry_text, password),
        )
        self.conn.commit()

    def save_and_switch(self):
        # Get the entry text
        entry_text = self.entry.get()
        # Validate the username
        if not self.validate_username(entry_text):
            # Display an error message in the interface
            self.error_label.config(
                text="Le nom d'utilisateur doit comporter entre 6 et 9 chiffres"
            )
            return
        # Save data to the database
        self.save_to_database()
        # Switch to page4fr
        self.switch_to_page4ar()

    def switch_to_main_interface(self):
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Hide the language interface
        # Show the main interface
        self.main_app.switch_to_main_interface()


if __name__ == "__main__":
    root = tk.Tk()
    app = Page3AR(root)
    root.mainloop()
