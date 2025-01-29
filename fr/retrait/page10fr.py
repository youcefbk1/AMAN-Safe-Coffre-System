from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import locale


class Page10FR:
    def __init__(self, master, main_app, cursor, conn):
        self.master = master
        self.main_app = main_app  # Save the MainApplication instance
        self.cursor = cursor  # Save the cursor
        self.conn = conn  # Save the conn
        self.setup_gui()

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

        # bande bleu  TOP
        self.frm1 = Frame(self.master, bg="#1679EF", height=50)
        self.frm1.pack(fill=X, side=TOP, pady=15)

        # logo
        old_image_frm1 = Image.open("image/AMAN-BLEU.png")
        resized_frm1 = old_image_frm1.resize((60, 50), Image.LANCZOS)
        self.new_image_frm1 = ImageTk.PhotoImage(resized_frm1)
        self.label1 = Label(
            self.frm1, image=self.new_image_frm1, highlightthickness=0, bd=0
        )
        self.label1.image = self.new_image_frm1
        self.label1.pack(expand=YES)
        # Partie central (contenu)

        self.frm2 = Frame(self.master, bg="#F2F7F9", height=360, width=800)

        self.frm2.pack()

        lbl_msg = CTkLabel(
            master=self.frm2,
            text="veuillez retirer vos bagages\n et fermer la porte\n Merci.",
            font=("Arial", 40, "bold"),
            text_color="#095CD3",
            fg_color="#F2F7F9",
        )
        lbl_msg.pack(expand=YES, pady=70)

        bouton = CTkButton(
            master=self.frm2,
            text="Confimer",
            font=("Arial", 30),
            text_color="#F2F7F9",
            fg_color="#1679EF",
            height=60,
            width=200,
            corner_radius=4,
            command=self.return_to_main,
        )
        bouton.pack(expand=YES, pady=10)

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
        if hasattr(self, "uart") and self.uart.is_open:
            self.uart.close()
            print("Connexion UART fermée.")
        """
        Resets the application without closing the window.
        """
        # Destroy all widgets inside the main window
        for widget in self.master.winfo_children():
            widget.destroy()

        # Reimport and reinitialize the main application
        from main import MainApplication  # Import your main application class

        MainApplication(self.master)  # Restart the main interface


if __name__ == "__main__":
    root = Tk()
    app = Page10FR()
    root.mainloop()
