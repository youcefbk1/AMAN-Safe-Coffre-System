from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import locale
import os
import sys

class Page8FR:

    def __init__(self, master, main_app, cursor, conn):
        self.master = master
        self.main_app = main_app
        self.cursor = cursor
        self.conn = conn
        self.casier_id = None  # Initialize with a default locker ID
        self.user_data = self.get_active_user_data()  # Fetch active user data
        self.inactivity_timer = None  # Initialize the inactivity timer
        self.setup_gui()
        self.reset_timer()  # Start the inactivity timer

    def get_active_user_data(self):
        """
        Fetches active user data from the 'person' table.
        """
        try:
            # Query to get the active user data
            self.cursor.execute(
                "SELECT username, password, casier, price FROM person WHERE actif = ?",
                (1,),
            )
            result = self.cursor.fetchone()

            if result:
                username, password, casier_id, price = result
                # Map casier ID to labels
                casier_label = {1: "A", 2: "B", 3: "C"}.get(casier_id, "Unknown")
                return {
                    "username": username,
                    "password": password,
                    "casier": casier_label,
                    "price": price,
                }
            else:
                print("No active user found.")
                return {
                    "username": "N/A",
                    "password": "N/A",
                    "casier": "N/A",
                    "price": "N/A",
                }
        except Exception as e:
            print(f"Error fetching active user data: {e}")
            return {
                "username": "Error",
                "password": "Error",
                "casier": "Error",
                "price": "Error",
            }

    def setup_gui(self):
        # Set French locale for date
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

        # Initialize main window
        self.master.title("AMAN")
        self.master.iconbitmap("image/AMAN-LOGO.ico")
        self.master.geometry("800x480")
        self.master.minsize(800, 480)
        self.master.maxsize(800, 480)
        self.master.config(bg="#F2F7F9")

        # Top blue banner
        self.frm1 = Frame(self.master, bg="#1679EF", height=50)
        self.frm1.pack(fill=X, side=TOP, pady=15)

        # Logo
        old_image_frm1 = Image.open("image/AMAN-BLEU.png")
        resized_frm1 = old_image_frm1.resize((60, 50), Image.LANCZOS)
        self.new_image_frm1 = ImageTk.PhotoImage(resized_frm1)
        self.label1 = Label(
            self.frm1, image=self.new_image_frm1, highlightthickness=0, bd=0
        )
        self.label1.image = self.new_image_frm1
        self.label1.pack(expand=YES)

        # Central content
        self.frm2 = Frame(self.master, bg="#F2F7F9", height=360, width=800)

        # Frame for ticket information
        frm_info = CTkButton(
            master=self.frm2,
            fg_color="#F2F7F9",
            border_width=3,
            border_color="#1679EF",
            corner_radius=4,
            height=200,
            width=350,
            hover=NONE,
            text="",
        )

        # Labels for ticket details
        label_ticket = CTkLabel(
            master=frm_info,
            text="N° Ticket :",
            font=("Arial", 17, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label_ticket.grid(row=0, column=0, sticky="w", padx=40)

        label_nom = CTkLabel(
            master=frm_info,
            text="Nom d'utilisateur :",
            font=("Arial", 17, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label_nom.grid(row=1, column=0, sticky="w", padx=40)

        label_mdp = CTkLabel(
            master=frm_info,
            text="Mot de passe :",
            font=("Arial", 17, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label_mdp.grid(row=2, column=0, sticky="w", padx=40)

        label_coffre = CTkLabel(
            master=frm_info,
            text="N° Coffre :",
            font=("Arial", 17, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label_coffre.grid(row=3, column=0, sticky="w", padx=40)

        label_montant = CTkLabel(
            master=frm_info,
            text="Montant :",
            font=("Arial", 17, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label_montant.grid(row=4, column=0, sticky="w", padx=40)

        # Display values from the active user data
        label_ticket_value = CTkLabel(
            master=frm_info,
            text="1111111111",  # Placeholder for ticket number
            font=("Arial", 17, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label_ticket_value.grid(row=0, column=1, sticky="w")

        label1 = CTkLabel(
            master=frm_info,
            text=self.user_data["username"],  # Username
            font=("Arial", 17, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label1.grid(row=1, column=1, sticky="w")

        label2 = CTkLabel(
            master=frm_info,
            text=self.user_data["password"],  # Password
            font=("Arial", 17, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label2.grid(row=2, column=1, sticky="w")

        label3 = CTkLabel(
            master=frm_info,
            text=self.user_data["casier"],  # Casier (e.g., A, B, C)
            font=("Arial", 17, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label3.grid(row=3, column=1, sticky="w")

        label4 = CTkLabel(
            master=frm_info,
            text=f"{self.user_data['price']} DA",  # Price
            font=("Arial", 17, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label4.grid(row=4, column=1, sticky="w")

        frm_info.place(x=230, y=0)

        lbl_msg = CTkLabel(
            master=self.frm2,
            text="Veuillez fermer la porte",
            font=("Arial", 40, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        lbl_msg.place(x=185, y=230)

        self.frm2.pack()

        btn_srt = CTkButton(
            master=self.frm2,
            text="Terminer",
            font=("Arial", 20),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=100,
            height=30,
            border_width=0,
            corner_radius=3,
            command=self.return_to_main,
        )
        btn_srt.place(x=40, y=320)

        image_flch_srt = Image.open("image/fleche3.png")
        rotated_img = image_flch_srt.rotate(180)
        resize = rotated_img.resize((35, 35), Image.LANCZOS)
        self.img_flch_srt = ImageTk.PhotoImage(resize)
        self.label_flch_srt = Label(self.frm2, image=self.img_flch_srt, bg="#F2F7F9")
        self.label_flch_srt.image = self.img_flch_srt
        self.label_flch_srt.place(x=1, y=316)

        self.frm3 = Frame(self.master, bg="#1679EF", height=30)
        date = datetime.now()
        label2 = Label(
            self.frm3,
            text=f"{date:%d-%m-%Y}  /  {date:%I:%M}",
            font=("Arial", 12),
            fg="#F2F7F9",
            bg="#1679EF",
        )
        label2.pack(expand=YES)

        self.frm3.pack(fill=X, side=BOTTOM)

    def return_to_main(self):

        # Destroy all widgets inside the main window
        for widget in self.master.winfo_children():
            widget.destroy()

        # Reimport and reinitialize the main application
        from main import MainApplication  # Import your main application class

        MainApplication(self.master)  # Restart the main interface

    def reset_timer(self):
        if self.inactivity_timer is not None:
            self.master.after_cancel(self.inactivity_timer)
        self.inactivity_timer = self.master.after(
            60000, self.return_to_main
        )  # 1 minute = 60000 ms


if __name__ == "__main__":
    root = Tk()
    app = Page8FR(root, None, None, None)
    root.mainloop()
