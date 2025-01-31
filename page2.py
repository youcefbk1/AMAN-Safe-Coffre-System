from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import locale
from fr.page3fr import Page3FR
from ar.page3ar import Page3AR


class LanguageInterface:
    def __init__(self, master, main_app, cursor, conn):
        self.master = master
        self.main_app = main_app  # Save the MainApplication instance
        self.cursor = cursor  # Save the cursor
        self.conn = conn  # Save the conn
        self.inactivity_timer = None  # Initialize the inactivity timer
        self.setup_gui()
        self.reset_timer()  # Start the inactivity timer

    def setup_gui(self):
        # Met la localisation suivant la France permet d'avoir la langue française pour la date
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

        self.master.title("Langue")
        self.master.iconbitmap("image/AMAN-LOGO.ico")
        self.master.geometry("800x480")
        self.master.minsize(800, 480)
        self.master.maxsize(800, 480)
        self.master.config(bg="#F2F7F9")

        self.frm1 = Frame(self.master, bg="#1679EF", height=50)
        self.frm1.pack(fill=X, side=TOP, pady=15)

        self.old_image_frm1 = Image.open("image/AMAN-BLEU.png")
        self.resized_frm1 = self.old_image_frm1.resize((60, 50), Image.LANCZOS)
        self.new_image_frm1 = ImageTk.PhotoImage(self.resized_frm1)
        self.label1 = Label(
            self.frm1, image=self.new_image_frm1, highlightthickness=0, bd=0
        )
        self.label1.image = (
            self.new_image_frm1
        )  # Keep a reference to avoid garbage collection
        self.label1.pack(expand=YES)

        self.image = Image.open("image/fleche3.png")
        self.img = ImageTk.PhotoImage(self.image)

        self.frm2 = Frame(self.master, bg="#F2F7F9", width=800, height=360)

        self.bouton1 = CTkButton(
            master=self.frm2,
            text="Français",
            fg_color="#1679EF",
            text_color="#F2F7F9",
            font=(("Arial"), 28),
            width=170,
            height=50,
            border_width=0,
            corner_radius=4,
            command=self.switch_to_page3fr,  # Call switch_to_page3fr when the button is clicked
        )
        self.bouton1.place(x=565, y=65)
        self.label1 = Label(self.frm2, image=self.img, bg="#F2F7F9")
        self.label1.place(x=735, y=59)

        self.bouton2 = CTkButton(
            master=self.frm2,
            text="العربية",
            fg_color="#1679EF",
            text_color="#F2F7F9",
            font=(("Arial"), 28),
            width=170,
            height=50,
            border_width=0,
            corner_radius=4,
            command=self.switch_to_page3ar,  # Call switch_to_page3ar when the button is clicked
        )
        self.bouton2.place(x=565, y=160)
        self.label2 = Label(self.frm2, image=self.img, bg="#F2F7F9")
        self.label2.place(x=735, y=154)

        self.bouton3 = CTkButton(
            master=self.frm2,
            text="Sortie  خروج ",
            fg_color="#1679EF",
            text_color="#F2F7F9",
            font=(("Arial"), 28),
            width=170,
            height=50,
            border_width=0,
            corner_radius=4,
            command=self.return_to_main,
        )
        self.bouton3.place(x=565, y=260)
        self.label3 = Label(self.frm2, image=self.img, bg="#F2F7F9")
        self.label3.place(x=735, y=254)

        self.label = Label(
            self.frm2,
            text="S'il vous plaît, choisissez votre langue \n\n من فضلك، اختر لغتك ",
            bg="#F2F7F9",
            fg="#095CD3",
            font=("Arial", 21, "bold"),
        )
        self.label.place(x=30, y=80)
        self.frm2.pack()

        self.frm3 = Frame(self.master, bg="#1679EF", height=30)
        date = datetime.now()
        self.label2 = Label(
            self.frm3,
            text=f"{date:%d-%m-%Y}  /  {date:%I:%M}",
            font=("Arial", 12),
            fg="#F2F7F9",
            bg="#1679EF",
        )
        self.label2.pack(expand=YES)
        self.frm3.pack(fill=X, side=BOTTOM)

    def switch_to_page3fr(self):
        self.reset_timer()  # Reset the timer on interaction
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Create an instance of LanguageInterface from page2.py
        Page3FR(self.master, self, self.cursor, self.conn)

    def switch_to_page3ar(self):
        self.reset_timer()  # Reset the timer on interaction
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Create an instance of LanguageInterface from page2.py
        Page3AR(self.master, self, self.cursor, self.conn)

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
                100000, self.return_to_main
            )  # 1 minute = 100000 ms
            print("Starting timer")


if __name__ == "__main__":
    root = Tk()
    app = LanguageInterface(root, None, None, None)
    root.mainloop()
