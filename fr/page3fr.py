from tkinter import *
from customtkinter import CTkEntry, CTkButton
from PIL import Image, ImageTk
from datetime import datetime
import locale
import random
import string
from fr.page4fr import Page4FR
import os
import sys


class Page3FR:
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

        self.frm1 = Frame(self.master, bg="#1679EF", height=50)
        self.frm1.pack(fill=X, side=TOP, pady=15)

        old_image_frm1 = Image.open("image/AMAN-BLEU.png")
        resized_frm1 = old_image_frm1.resize((60, 50), Image.LANCZOS)
        self.new_image_frm1 = ImageTk.PhotoImage(resized_frm1)
        self.label1 = Label(
            self.frm1, image=self.new_image_frm1, highlightthickness=0, bd=0
        )
        self.label1.image = self.new_image_frm1
        self.label1.pack(expand=YES)

        # Central part (content)
        self.frm2 = Frame(self.master, bg="#F2F7F9", height=360, width=800)

        label_msg = Label(
            self.frm2,
            text="Veuillez entrer le code\nde votre carte d'identité biométrique",
            font=("Arial", 17, "bold"),
            fg="#095CD3",
            bg="#F2F7F9",
        )
        label_msg.place(x=345, y=20)

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

        self.btn = Button(
            self.frm2,
            text="Inscription",
            font=("Arial", 20),
            bg="#1679EF",
            fg="#F2F7F9",
            width=22,
            bd=0,
            command=self.save_and_switch,
        )
        self.btn.place(x=370, y=200)

        self.btn_srt = Button(
            self.frm2,
            text="Sortie",
            font=("Arial", 15),
            bg="#1679EF",
            fg="#F2F7F9",
            width=7,
            bd=0,
            command=self.return_to_main,
        )
        self.btn_srt.place(x=45, y=320)

        image_flch = Image.open("fleche3.png")
        img_flch = ImageTk.PhotoImage(image_flch)
        label_flch = Label(self.frm2, image=img_flch, bg="#F2F7F9")
        label_flch.image = img_flch  # Keep a reference to the image object
        label_flch.place(x=725, y=194)

        image_flch2 = Image.open("fleche3.png")
        rotated_img = image_flch2.rotate(180)
        resize = rotated_img.resize((35, 35), Image.LANCZOS)
        img_flch2 = ImageTk.PhotoImage(resize)
        label_flch2 = Label(self.frm2, image=img_flch2, bg="#F2F7F9")
        label_flch2.image = img_flch2  # Keep a reference to the image object
        label_flch2.place(x=2, y=319)

        image_identite = Image.open("fr/image/identite_fr.png")
        resize_identite = image_identite.resize((250, 170), Image.LANCZOS)
        img_identite = ImageTk.PhotoImage(resize_identite)
        self.label_img = Label(self.frm2, image=img_identite, bg="#F2F7F9")
        self.label_img.image = img_identite  # Keep a reference to the image object
        self.label_img.place(x=55, y=20)

        self.frm2.pack()

        self.frm3 = Frame(self.master, bg="#1679EF", height=30)
        date = datetime.now()
        label_date = Label(
            self.frm3,
            text=f"{date:%m-%d-%Y}  /  {date:%I:%M}",
            font=("Arial", 12),
            fg="#F2F7F9",
            bg="#1679EF",
        )
        label_date.pack(expand=YES)
        self.frm3.pack(fill=X, side=BOTTOM)

    def validate_username(self, username):
        # Check if the username consists only of numbers and is between 6 to 9 digits long
        if username.isdigit() and 6 <= len(username) <= 9:
            return True
        else:
            return False

    def switch_to_page4fr(self):
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Create an instance of LanguageInterface from page2.py
        Page4FR(self.master, self, self.cursor, self.conn)

    def generate_password(self):
        # Generate a random password of 6 digits
        password = "".join(random.choices(string.digits, k=6))
        return password

    def save_to_database(self):
        entry_text = self.entry.get()
        # Generate a password
        password = self.generate_password()

        # Set all users to inactive first
        self.cursor.execute("UPDATE person SET actif = 0")

        # Insert the new user and set them as active
        self.cursor.execute(
            """
            INSERT INTO person (username, password, actif)
            VALUES (?, ?, ?)
            """,
            (entry_text, password, 1),  # Actif = 1 pour ce nouvel utilisateur
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
        self.switch_to_page4fr()

    # def return_to_main(self):
    #     self.frm1.pack_forget()
    #     self.frm2.pack_forget()
    #     self.frm3.pack_forget()
    #     # Hide the language interface
    #     # Show the main interface
    #     self.main_app.switch_to_main_interface()


    def return_to_main(self):
        """
        Resets the application without closing the window.
        """
        # Destroy all widgets inside the main window
        for widget in self.master.winfo_children():
            widget.destroy()

        # Reimport and reinitialize the main application
        from main import MainApplication  # Import your main application class

        MainApplication(self.master)  # Restart the main interface

    def switch_to_main_interface(self):
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Hide the language interface
        # Show the main interface
        self.main_app.switch_to_main_interface()


if __name__ == "__main__":
    root = Tk()
    app = Page3FR(root)
    root.mainloop()
