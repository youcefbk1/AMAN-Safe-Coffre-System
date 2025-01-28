from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import locale


class Page8FR:

    def __init__(self, master, main_app, cursor, conn):
        self.master = master
        self.main_app = main_app
        self.cursor = cursor
        self.conn = conn
        self.casier_id = None  # Initialisez avec un ID de casier par défaut
        # self.price = (
        #     self.get_active_user_price()
        # )  # Récupérer le prix de l'utilisateur actif

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

        # la partie à remplire(que tu peux modifier)
        label_date = CTkLabel(
            master=frm_info,
            text="1111111111",
            font=("Arial", 17, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label_date.grid(row=0, column=1, sticky="w")

        label1 = CTkLabel(
            master=frm_info,
            text="user name",
            font=("Arial", 17, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label1.grid(row=1, column=1, sticky="w")

        label2 = CTkLabel(
            master=frm_info,
            text="password",
            font=("Arial", 17, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label2.grid(row=2, column=1, sticky="w")

        label3 = CTkLabel(
            master=frm_info,
            text="nb box",
            font=("Arial", 17, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label3.grid(row=3, column=1, sticky="w")

        label4 = CTkLabel(
            master=frm_info,
            text="price",
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
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        self.frm_box.place_forget()
        self.main_app.switch_to_main_interface()

    def switch_to_main_interface(self):
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        self.frm_box.place_forget()
        self.main_app.switch_to_main_interface()


if __name__ == "__main__":
    root = Tk()
    app = Page8FR(root)
    root.mainloop()
