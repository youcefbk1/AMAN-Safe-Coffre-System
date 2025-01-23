import tkinter as tk
from customtkinter import *
from PIL import ImageTk, Image
from datetime import datetime
import locale
import sqlite3
from page2 import LanguageInterface
from fr.page3fr import Page3FR


class MainApplication:

    def __init__(self, master):
        self.master = master
        self.setup_gui()

    def setup_gui(self):
        # Met la localisation suivant la France permet d'avoir la langue française pour la date
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

        # Partie initialisation de la fenêtre
        self.master.title("AMAN")
        self.master.iconbitmap("image/AMAN-LOGO.ico")
        self.master.geometry("800x480")
        self.master.minsize(800, 480)
        self.master.maxsize(800, 480)
        self.master.config(bg="#F2F7F9")

        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect("db.sqlite")
        self.cursor = self.conn.cursor()

        # Call methods to create tables and insert data
        self.create_person_table()

    def create_person_table(self):
        # Create the person table if it does not exist
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS person (
                        id INTEGER PRIMARY KEY,
                        username INTEGER,
                        password INTEGER,
                        casier INTEGER,
                        actif BOOLEAN DEFAULT 0,
                        price INTEGER,
                        time INTEGER,
                        FOREIGN KEY (casier) REFERENCES casier(id)
                    )"""
        )

        self.conn.commit()

        # Bande bleue d'en haut avec logo AMAN
        self.frm1 = tk.Frame(self.master, bg="#1679EF", height=50)
        self.frm1.pack(fill=tk.X, side=tk.TOP, pady=15)

        self.old_image_frm1 = Image.open("image/AMAN-BLEU.png")
        self.resized_frm1 = self.old_image_frm1.resize((60, 50), Image.LANCZOS)
        self.new_image_frm1 = ImageTk.PhotoImage(self.resized_frm1)
        self.label1 = tk.Label(
            self.frm1, image=self.new_image_frm1, highlightthickness=0, bd=0
        )
        self.label1.image = (
            self.new_image_frm1
        )  # Keep a reference to avoid garbage collection
        self.label1.pack(expand=tk.YES)

        # Frame2 c'est la partie centrale de la fenêtre
        self.frm2 = tk.Frame(self.master, bg="#F2F7F9")

        self.old_image_frm2 = Image.open("image/AMAN-WHITE.jpg")
        self.resize_frm2 = self.old_image_frm2.resize((240, 140), Image.LANCZOS)
        self.new_image_frm2 = ImageTk.PhotoImage(self.resize_frm2)
        self.label = tk.Label(
            self.frm2,
            bg="#1679EF",
            image=self.new_image_frm2,
            bd=0,
            highlightthickness=0,
        )
        self.label.image = (
            self.new_image_frm2
        )  # Keep a reference to avoid garbage collection
        self.label.pack(pady=40)

        self.button = CTkButton(
            master=self.frm2,
            text="Start      ابدا ",
            font=(("Arial"), 28),
            width=250,
            height=60,
            fg_color="#1679EF",
            text_color="#F2F7F9",
            border_width=0,
            corner_radius=4,
            command=self.switch_to_language_interface,
        )  # Appelle la fonction show_page2 lorsque le bouton est cliqué
        self.button.pack()
        self.frm2.pack()

        # Bande bleue d'en bas
        self.frm3 = tk.Frame(self.master, bg="#1679EF", height=30)
        self.date_label = tk.Label(
            self.frm3,
            text=self.get_current_date_time(),
            font=("Arial", 12),
            fg="#F2F7F9",
            bg="#1679EF",
        )
        self.date_label.pack(expand=tk.YES)
        self.frm3.pack(fill=tk.X, side=tk.BOTTOM)

    def get_current_date_time(self):
        date = datetime.now()
        return f"{date:%d-%m-%Y}  /  {date:%I:%M}"

    def switch_to_language_interface(self):
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Create an instance of LanguageInterface from page2.py
        LanguageInterface(self.master, self, self.cursor, self.conn)

    def switch_to_main_interface(self):
        # Show the main interface again
        self.frm1.pack(fill=tk.X, side=tk.TOP, pady=15)
        self.frm2.pack()
        self.frm3.pack(fill=tk.X, side=tk.BOTTOM)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

