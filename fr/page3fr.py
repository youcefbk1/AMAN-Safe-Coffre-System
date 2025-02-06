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
        self.inactivity_timer = None  # Initialize the inactivity timer
        self.setup_gui()
        self.reset_timer()  # Start the inactivity timer

    def open_touch_keyboard(self, event=None):
        # Open the touch keyboard on Windows from C:\Program Files\Common Files\microsoft shared\ink\TabTip.exe

        os.system('"C:\\Program Files\\Common Files\\microsoft shared\\ink\\TabTip.exe"')
        print("success keyboard")
        
    

    def setup_gui(self):
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

        self.master.title("AMAN")

        self.master.iconbitmap("image/AMAN-LOGO.ico")
        self.master.geometry("1920x1200")
        self.master.minsize(1920, 1200)
        self.master.maxsize(1920, 1200)
        self.master.config(bg="#F2F7F9")

        self.frm1 = Frame(self.master, bg="#1679EF", height=100)
        self.frm1.pack(fill=X, side=TOP)

        old_image_frm1 = Image.open("image/AMAN-BLEU.png")
        resized_frm1 = old_image_frm1.resize((120, 100), Image.LANCZOS)
        self.new_image_frm1 = ImageTk.PhotoImage(resized_frm1)
        self.label1 = Label(
            self.frm1, image=self.new_image_frm1, highlightthickness=0, bd=0
        )
        self.label1.image = self.new_image_frm1
        self.label1.pack(expand=YES)

        # Central part (content)
        self.frm2 = Frame(self.master, bg="#F2F7F9")

        label_msg = Label(
            self.frm2,
            text="Veuillez entrer le code\nde votre carte d'identité biométrique",
            font=("Arial", 34, "bold"),
            fg="#095CD3",
            bg="#F2F7F9",
        )
        label_msg.place(x=690, y=40)

        # Entry field
        self.entry = CTkEntry(
            master=self.frm2,
            font=("Arial", 46, "bold"),
            fg_color="#F2F7F9",
            border_width=2,
            width=730,
            border_color="#1679EF",
            corner_radius=4,
            text_color="black",
            height=100,
        )
        self.entry.place(x=740, y=180)
        self.entry.bind("<FocusIn>", lambda event: self.open_touch_keyboard())

        self.error_label = Label(
            self.frm2,
            text="",
            font=("Arial", 24),
            fg="red",
            bg="#F2F7F9",
        )
        self.error_label.place(x=740, y=280)

        self.btn = Button(
            self.frm2,
            text="Inscription",
            font=("Arial", 40),
            bg="#1679EF",
            fg="#F2F7F9",
            width=22,
            bd=0,
            command=self.save_and_switch,
        )
        self.btn.place(x=740, y=400)

        self.btn_srt = CTkButton(
            self.frm2,
            text="Sortie",
            font=("Arial", 40),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=200,
            height=60,
            border_width=0,
            corner_radius=3,
            command=self.return_to_main,
        )
        self.btn_srt.place(x=90, y=600)

        image_flch = Image.open("fleche3.png")
        self.resized_flesh = image_flch.resize((100, 100), Image.LANCZOS)
        img_flch = ImageTk.PhotoImage(self.resized_flesh)
        label_flch = Label(self.frm2, image=img_flch, bg="#F2F7F9")
        label_flch.image = img_flch  # Keep a reference to the image object
        label_flch.place(x=1430, y=400)

        image_flch2 = Image.open("fleche3.png")
        rotated_img = image_flch2.rotate(180)
        resize = rotated_img.resize((70, 70), Image.LANCZOS)
        img_flch2 = ImageTk.PhotoImage(resize)
        label_flch2 = Label(self.frm2, image=img_flch2, bg="#F2F7F9")
        label_flch2.image = img_flch2  # Keep a reference to the image object
        label_flch2.place(x=4, y=595)

        image_identite = Image.open("fr/image/identite_fr.png")
        resize_identite = image_identite.resize((500, 340), Image.LANCZOS)
        img_identite = ImageTk.PhotoImage(resize_identite)
        self.label_img = Label(self.frm2, image=img_identite, bg="#F2F7F9")
        self.label_img.image = img_identite  # Keep a reference to the image object
        self.label_img.place(x=110, y=40)

        self.frm2.pack(expand=YES, fill=BOTH)

        self.frm3 = Frame(self.master, bg="#1679EF", height=60)
        date = datetime.now()
        self.label_date = Label(
            self.frm3,
            text=f"{date:%m-%d-%Y}  /  {date:%I:%M}",
            font=("Arial", 24),
            fg="#F2F7F9",
            bg="#1679EF",
        )
        self.label_date.pack(expand=YES)
        self.frm3.pack(fill=X, side=BOTTOM)

    def validate_username(self, username):
        # Check if the username consists only of numbers and is exactly 9 digits long
        if username.isdigit() and len(username) == 9:
            return True
        else:
            return False

    def switch_to_page4fr(self):
        self.reset_timer()  # Reset the timer on interaction
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Create an instance of LanguageInterface from page2.py
        Page4FR(self.master, self, self.cursor, self.conn)

    def generate_password(self):
        # Generate a random password of 6 digits
        password = "".join(random.choices(string.digits, k=4))
        return password

    def save_to_database(self):
        entry_text = self.entry.get()
        # Generate a password
        password = self.generate_password()

        # Check if the username already exists
        # self.cursor.execute("SELECT id FROM person WHERE username = ?", (entry_text,))
        # existing_user = self.cursor.fetchone()

        # Set all users to inactive first
        self.cursor.execute("UPDATE person SET actif = 0")

        # if existing_user:
        #     self.cursor.execute(
        #         "UPDATE person SET actif = ? WHERE id = ?",
        #         (1, existing_user[0]),
        #     )
        #     self.conn.commit()
        # else:
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
                text="Le nom d'utilisateur doit comporter 9 chiffres"
            )
            return
        # Save data to the database
        self.save_to_database()
        # Switch to page4fr
        self.switch_to_page4fr()

    def return_to_main(self):
        self.reset_timer()  # Reset the timer on interaction
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
        self.reset_timer()  # Reset the timer on interaction
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Hide the language interface
        # Show the main interface
        self.main_app.switch_to_main_interface()

    def reset_timer(self):
        print("Resetting timer")
        if self.inactivity_timer is not None:
            self.master.after_cancel(self.inactivity_timer)
            print("Cancelled timer")
        else:
            self.inactivity_timer = self.master.after(
                120000, self.return_to_main
            )  # 1 minute = 120000 ms
            print("Starting timer")


if __name__ == "__main__":
    root = Tk()
    app = Page3FR(root)
    root.mainloop()
