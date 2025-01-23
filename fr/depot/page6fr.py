from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import locale


class Page6FR:
    def __init__(self, master, main_app, cursor, conn):
        self.master = master
        self.main_app = main_app
        self.cursor = cursor
        self.conn = conn
        self.casier_id = None  # Initialisez avec un ID de casier par défaut
        self.setup_gui()

    def setup_gui(self):
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
        self.master.title("AMAN")
        self.master.iconbitmap("image/AMAN-LOGO.ico")
        self.master.geometry("800x480")
        self.master.config(bg="#F2F7F9")

        # Bandeau bleu en haut
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

        # Partie centrale
        self.frm2 = Frame(self.master, bg="#F2F7F9", height=360, width=800)
        label_msg = Label(
            self.frm2,
            text="Veuillez sélectionner la durée de stockage souhaitée",
            font=("Arial", 18, "bold"),
            fg="#095CD3",
            bg="#F2F7F9",
        )
        label_msg.place(x=95, y=3)

        # Boutons pour afficher les prix (placeholders pour l'instant)
        self.btns = []
        for i, (x, y) in enumerate(
            [
                (475, 60),
                (475, 140),
                (475, 220),
                (475, 300),
                (66, 60),
                (66, 140),
                (66, 220),
                (66, 300),
            ]
        ):
            btn = CTkButton(
                master=self.frm2,
                text = "Sortie" if i == 7 else f"Bouton {i+1}",
                font=("Arial", 26),
                fg_color="#1679EF",
                text_color="#F2F7F9",
                width=260,
                height=45,
                border_width=0,
                corner_radius=4,
                command=(
                    self.return_to_main if i == 7 else None
                ),  # Par exemple, "Sortie" pour le dernier bouton
            )
            btn.place(x=x, y=y)
            self.btns.append(btn)

        # Ajout des flèches
        # partie flech droite
        image_flch = Image.open("image/fleche10.png")
        self.img_flch = ImageTk.PhotoImage(image_flch)

        self.label_flch1 = Label(self.frm2, image=self.img_flch, bg="#F2F7F9")
        self.label_flch1.place(x=750, y=63)

        label_flch2 = Label(self.frm2, image=self.img_flch, bg="#F2F7F9")
        label_flch2.place(x=750, y=144)

        label_flch3 = Label(self.frm2, image=self.img_flch, bg="#F2F7F9")
        label_flch3.place(x=750, y=224)

        label_flch4 = Label(self.frm2, image=self.img_flch, bg="#F2F7F9")
        label_flch4.place(x=750, y=305)

        # rotated image
        image_old = Image.open("image/fleche10.png")
        image_rota = image_old.rotate(180)
        self.image_final = ImageTk.PhotoImage(image_rota)

        # partie fleche gauche
        label_flch5 = Label(self.frm2, image=self.image_final, bg="#F2F7F9")
        label_flch5.place(x=9, y=63)

        label_flch6 = Label(self.frm2, image=self.image_final, bg="#F2F7F9")
        label_flch6.place(x=9, y=144)

        label_flch7 = Label(self.frm2, image=self.image_final, bg="#F2F7F9")
        label_flch7.place(x=9, y=224)

        label_flch8 = Label(self.frm2, image=self.image_final, bg="#F2F7F9")
        label_flch8.place(x=9, y=305)


        # Charger les prix basés sur le casier
        self.load_prices()

        self.frm2.pack()

        # Bandeau bleu en bas
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

    def load_prices(self):
        try:
            # Obtenir l'ID du casier pour l'utilisateur actif
            self.cursor.execute(
                "SELECT casier FROM person WHERE actif = ?", (1,)
            )  # Remplacez 1 par l'ID actuel
            casier_id = self.cursor.fetchone()[0]

            # Récupérer les prix depuis la table "casier" pour ce casier
            self.cursor.execute("SELECT * FROM casier WHERE id = ?", (casier_id,))
            casier_data = self.cursor.fetchone()

            if casier_data:
                durations = ["1h", "2h", "3h", "4h", "12h", "24h", "48h"]
                prices = casier_data[2:]  # Ignorer les colonnes ID et Volume
                for i, (duration, price) in enumerate(zip(durations, prices)):
                    self.btns[i].configure(text=f"{duration} / {price} DA")
            else:
                print("Aucun casier trouvé pour cet ID.")
        except Exception as e:
            print(f"Erreur lors du chargement des prix : {e}")

    def return_to_main(self):
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        self.main_app.switch_to_main_interface()


if __name__ == "__main__":
    root = Tk()
    app = Page6FR(
        root, None, None, None
    )  # Passer vos objets main_app, cursor et conn ici
    root.mainloop()
