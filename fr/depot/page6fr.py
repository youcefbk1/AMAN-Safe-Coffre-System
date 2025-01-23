from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import locale


class Page6FR:

    def __init__(self, master, main_app, cursor, conn):
        self.master = master
        self.main_app = main_app  # Save the MainApplication instance
        self.cursor = cursor  # Save the cursor
        self.conn = conn  # Save the conn
        self.setup_gui()

    def setup_gui(self):

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

        label_msg = Label(
            self.frm2,
            text="Veuillez sélectionner la durée de stockage souhaitée",
            font=("Arial", 18, "bold"),
            fg="#095CD3",
            bg="#F2F7F9",
        )
        label_msg.place(x=95, y=3)

        # partie bouton
        # bouton droit
        btn1 = CTkButton(
            master=self.frm2,
            text="1 heure / 100 DA",
            font=("Arial", 26),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=260,
            height=45,
            border_width=0,
            corner_radius=4,
        )
        btn1.place(x=475, y=60)

        btn2 = CTkButton(
            master=self.frm2,
            text="2 heures / 200 DA",
            font=("Arial", 26),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=260,
            height=45,
            border_width=0,
            corner_radius=4,
        )
        btn2.place(x=475, y=140)

        btn3 = CTkButton(
            master=self.frm2,
            text="3 heures / 300 DA",
            font=("Arial", 26),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=260,
            height=45,
            border_width=0,
            corner_radius=4,
        )
        btn3.place(x=475, y=220)

        btn4 = CTkButton(
            master=self.frm2,
            text="4 heures / 400 DA",
            font=("Arial", 26),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=260,
            height=45,
            border_width=0,
            corner_radius=4,
        )
        btn4.place(x=475, y=300)

        # bouton gauche

        btn5 = CTkButton(
            master=self.frm2,
            text="12 heure / 1200 DA",
            font=("Arial", 26),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=260,
            height=45,
            border_width=0,
            corner_radius=4,
        )
        btn5.place(x=66, y=60)

        btn6 = CTkButton(
            master=self.frm2,
            text="24 heures / 2400 DA",
            font=("Arial", 26),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=260,
            height=45,
            border_width=0,
            corner_radius=4,
        )
        btn6.place(x=66, y=140)

        btn7 = CTkButton(
            master=self.frm2,
            text="48 heures / 4000 DA",
            font=("Arial", 26),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=260,
            height=45,
            border_width=0,
            corner_radius=4,
        )
        btn7.place(x=66, y=220)

        btn8 = CTkButton(
            master=self.frm2,
            text="Sortie",
            font=("Arial", 26),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=260,
            height=45,
            border_width=0,
            corner_radius=4,
        )
        btn8.place(x=66, y=300)

        # partie flech droite
        image_flch = Image.open("image/fleche10.png")
        img_flch = ImageTk.PhotoImage(image_flch)

        label_flch1 = Label(self.frm2, image=img_flch, bg="#F2F7F9")
        label_flch1.place(x=750, y=63)

        label_flch2 = Label(self.frm2, image=img_flch, bg="#F2F7F9")
        label_flch2.place(x=750, y=144)

        label_flch3 = Label(self.frm2, image=img_flch, bg="#F2F7F9")
        label_flch3.place(x=750, y=224)

        label_flch4 = Label(self.frm2, image=img_flch, bg="#F2F7F9")
        label_flch4.place(x=750, y=305)

        # rotated image
        image_old = Image.open("image/fleche10.png")
        image_rota = image_old.rotate(180)
        image_final = ImageTk.PhotoImage(image_rota)

        # partie fleche gauche
        label_flch5 = Label(self.frm2, image=image_final, bg="#F2F7F9")
        label_flch5.place(x=9, y=63)

        label_flch6 = Label(self.frm2, image=image_final, bg="#F2F7F9")
        label_flch6.place(x=9, y=144)

        label_flch7 = Label(self.frm2, image=image_final, bg="#F2F7F9")
        label_flch7.place(x=9, y=224)

        label_flch8 = Label(self.frm2, image=image_final, bg="#F2F7F9")
        label_flch8.place(x=9, y=305)

        self.frm2.pack()

        # bande bleu BOTTOM
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
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Hide the language interface
        # Show the main interface
        self.main_app.switch_to_main_interface()
        
    def switch_to_main_interface(self):
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Hide the language interface
        # Show the main interface
        self.main_app.switch_to_main_interface()

        
if __name__ == "__main__":
    root = Tk()
    app = Page6FR(root)
    root.mainloop()
