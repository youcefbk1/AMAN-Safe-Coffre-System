from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import locale


class Page7FR:
    def __init__(self, master, main_app, cursor, conn):
        self.master = master
        self.main_app = main_app
        self.cursor = cursor
        self.conn = conn
        self.casier_id = None  # Initialisez avec un ID de casier par défaut
        self.price = (
            self.get_active_user_price()
        )  # Récupérer le prix de l'utilisateur actif
        self.signal_received = False  # Flag pour le signal
        self.setup_gui()
        self.wait_for_signal()  # Lance la méthode pour attendre un signal

    def wait_for_signal(self):
        """
        Méthode qui attend un signal du monnayeur.
        Si le signal est reçu, bascule vers l'interface suivante.
        """
        # Simulation : Si un signal est reçu (à remplacer par votre logique réelle)
        # Exemple : Lecture d'une valeur GPIO ou un autre mécanisme
        if self.signal_received:
            print("Signal reçu, basculement vers l'interface suivante.")
            self.switch_to_main_interface()
        else:
            # Réessaye après 500 ms (0.5 seconde)
            self.master.after(500, self.wait_for_signal)

    def get_active_user_price(self):
        """
        Récupère le prix pour l'utilisateur actif depuis la table 'person'.
        """
        try:
            self.cursor.execute("SELECT price FROM person WHERE actif = ?", (1,))
            result = self.cursor.fetchone()
            if result:
                return result[0]  # Retourne le prix
            else:
                print("Aucun utilisateur actif trouvé.")
                return 0  # Valeur par défaut si aucun utilisateur actif
        except Exception as e:
            print(f"Erreur lors de la récupération du prix : {e}")
            return 0  # Valeur par défaut en cas d'erreur

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
        self.frm_box = Frame(self.master, bg="#F2F7F9", height=300, width=300)
        self.frm_box.place(x=600, y=100)

        box1 = CTkButton(
            master=self.frm_box,
            text="A",
            text_color="#1679EF",
            fg_color="#F2F7F9",
            height=80,
            width=90,
            corner_radius=4,
            border_width=2,
            border_color="#1679EF",
            hover=None,
        )
        box1.grid(row=0, column=0, padx=0.5, pady=0.5)

        box5 = CTkButton(
            master=self.frm_box,
            text="B",
            text_color="#1679EF",
            fg_color="#F2F7F9",
            height=100,
            width=90,
            corner_radius=4,
            border_width=2,
            border_color="#1679EF",
            hover=None,
        )
        box5.grid(row=1, column=0, padx=0.5, pady=0.5)

        box13 = CTkButton(
            master=self.frm_box,
            text="C",
            text_color="#1679EF",
            fg_color="#F2F7F9",
            height=140,
            width=90,
            corner_radius=4,
            border_width=2,
            border_color="#1679EF",
            hover=None,
        )
        box13.grid(row=2, column=0, padx=0.5, pady=0.5, rowspan=2)

        self.frm_msg = CTkFrame(master=self.frm2, fg_color="#F2F7F9")

        label_msg = CTkLabel(
            master=self.frm_msg,
            text="Votre montant total à régler",
            font=("Arial", 25, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        label_msg.grid(row=0, column=0, pady=30)

        # Dynamically set the price for the active user
        label_price = CTkLabel(
            master=self.frm_msg,
            text=f"{self.price} DA",  # Display the fetched price
            font=("Arial", 40),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            corner_radius=4,
            height=70,
            width=200,
        )
        label_price.grid(row=1, column=0)

        # image fleche
        img_flch = Image.open("fr/image/flech_bas.png")
        self.img_flch_final = ImageTk.PhotoImage(img_flch)

        self.label_flch = CTkLabel(
            master=self.frm2, fg_color="#1679EF", image=self.img_flch_final, text=None
        )
        self.label_flch.place(x=120, y=105)

        self.frm_msg.place(x=220, y=50)
        self.frm2.pack()

        btn_srt = CTkButton(
            master=self.frm2,
            text="Sortie",
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
    app = Page7FR(root)
    root.mainloop()
