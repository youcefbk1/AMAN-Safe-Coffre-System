from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import locale
from fr.depot.page7fr import Page7FR


class Page6FR:
    def __init__(self, master, main_app, cursor, conn):
        self.master = master
        self.main_app = main_app
        self.cursor = cursor
        self.conn = conn
        self.casier_id = None  # Initialisez avec un ID de casier par défaut
        self.inactivity_timer = None  # Initialize the inactivity timer
        self.setup_gui()
        self.reset_timer()  # Start the inactivity timer

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

        # Boutons pour afficher les prix
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
                text="Sortie" if i == 7 else f"Bouton {i+1}",
                font=("Arial", 26),
                fg_color="#1679EF",
                text_color="#F2F7F9",
                width=260,
                height=45,
                border_width=0,
                corner_radius=4,
                command=(
                    self.return_to_main
                    if i == 7
                    else lambda duration_price=(None, None): self.save_choice(
                        duration_price
                    )
                ),  # Placeholder pour l'instant
            )
            btn.place(x=x, y=y)
            self.btns.append(btn)

        # Ajout des flèches
        # partie flech droite
        image_flch = Image.open("image/fleche10.png")
        self.img_flch = ImageTk.PhotoImage(image_flch)

        self.label_flch1 = Label(self.frm2, image=self.img_flch, bg="#F2F7F9")
        self.label_flch1.place(x=750, y=63)

        self.label_flch2 = Label(self.frm2, image=self.img_flch, bg="#F2F7F9")
        self.label_flch2.place(x=750, y=144)

        self.label_flch3 = Label(self.frm2, image=self.img_flch, bg="#F2F7F9")
        self.label_flch3.place(x=750, y=224)

        self.label_flch4 = Label(self.frm2, image=self.img_flch, bg="#F2F7F9")
        self.label_flch4.place(x=750, y=305)

        # rotated image
        image_old = Image.open("image/fleche10.png")
        image_rota = image_old.rotate(180)
        self.image_final = ImageTk.PhotoImage(image_rota)

        # partie fleche gauche
        self.label_flch5 = Label(self.frm2, image=self.image_final, bg="#F2F7F9")
        self.label_flch5.place(x=9, y=63)

        self.label_flch6 = Label(self.frm2, image=self.image_final, bg="#F2F7F9")
        self.label_flch6.place(x=9, y=144)

        self.label_flch7 = Label(self.frm2, image=self.image_final, bg="#F2F7F9")
        self.label_flch7.place(x=9, y=224)

        self.label_flch8 = Label(self.frm2, image=self.image_final, bg="#F2F7F9")
        self.label_flch8.place(x=9, y=305)

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
            self.cursor.execute("SELECT casier FROM person WHERE actif = ?", (1,))
            casier_id = self.cursor.fetchone()[0]

            # Récupérer les prix depuis la table "casier" pour ce casier
            self.cursor.execute("SELECT * FROM casier WHERE id = ?", (casier_id,))
            casier_data = self.cursor.fetchone()

            if casier_data:
                durations = ["1h", "2h", "3h", "4h", "12h", "24h", "48h"]
                prices = casier_data[2:]  # Ignorer les colonnes ID et Volume
                for i, (duration, price) in enumerate(zip(durations, prices)):
                    # Configurer le texte et la commande des boutons
                    self.btns[i].configure(
                        text=f"{duration} / {price} DA",
                        command=lambda d=duration, p=price: self.save_choice(d, p),
                    )
            else:
                print("Aucun casier trouvé pour cet ID.")
        except Exception as e:
            print(f"Erreur lors du chargement des prix : {e}")

    def save_choice(self, duration, price):
        """
        Enregistre le temps et le prix choisis pour l'utilisateur actif.
        """
        try:
            # Convertir le temps (e.g., "24h") en entier
            time_int = int(duration.replace("h", ""))
            # Mettre à jour la table `person` pour l'utilisateur actif
            self.cursor.execute(
                "UPDATE person SET time = ?, price = ? WHERE actif = ?",
                (time_int, price, 1),
            )
            self.conn.commit()  # Valider les changements
            print(f"Temps {duration} et prix {price} enregistrés avec succès.")
            self.switch_to_page7fr()
        except Exception as e:
            print(f"Erreur lors de l'enregistrement du choix : {e}")

    def switch_to_page7fr(self):
        self.reset_timer()  # Reset the timer on interaction
        # Change vers la page suivante
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        Page7FR(self.master, self, self.cursor, self.conn)

    def return_to_main(self):
        self.reset_timer()  # Reset the timer on interaction
        """
        Checks if there is an active user, deletes the user from the database where paid = 0,
        and resets the application without closing the window.
        """
        try:

            # Delete user where paid = 0
            self.cursor.execute("DELETE FROM person WHERE actif = 1 AND paid = 0")
            self.conn.commit()
            print("Deleted unpaid active user.")
        except Exception as e:
            print(f"Error deleting user: {e}")

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
    app = Page6FR()  # Passer vos objets main_app, cursor et conn ici
    root.mainloop()
