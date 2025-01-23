from tkinter import *
from tkinter import messagebox  # Pour afficher des messages d'erreur
from customtkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import locale
from fr.retrait.page10fr import Page10FR


class Page9FR:
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

        lbl_msg = CTkLabel(
            master=self.frm2,
            text="Veuillez remplir les informations suivantes",
            font=("Arial", 28, "bold"),
            text_color="#095CD3",
            fg_color="#F2F7F9",
        )
        lbl_msg.place(x=115, y=30)

        frm_info = CTkFrame(master=self.frm2, fg_color="#F2F7F9")
        lbl1 = CTkLabel(
            master=frm_info,
            text="Nom d'utilisateur",
            font=("Arial", 20, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        lbl1.grid(row=0, column=0, padx=10, pady=15, sticky="w")

        lbl2 = CTkLabel(
            master=frm_info,
            text="Mot de passe",
            font=("Arial", 20, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        lbl2.grid(row=1, column=0, padx=10, pady=15, sticky="w")

        self.entry_username = CTkEntry(
            master=frm_info,
            fg_color="#F2F7F9",
            text_color="black",
            font=("Arial", 20),
            border_color="#1679EF",
            border_width=2.5,
            width=200,
        )
        self.entry_username.grid(row=0, column=1, padx=10, pady=15)

        self.entry_password = CTkEntry(
            master=frm_info,
            fg_color="#F2F7F9",
            text_color="black",
            font=("Arial", 20),
            border_color="#1679EF",
            border_width=2.5,
            width=200,
            show="*",
        )
        self.entry_password.grid(row=1, column=1, padx=10, pady=15)

        frm_info.place(x=385, y=100)

        frm_btn = CTkFrame(master=self.frm2, fg_color="#F2F7F9")
        bouton = CTkButton(
            master=frm_btn,
            text="Confirmer",
            font=("Arial", 25),
            text_color="#F2F7F9",
            fg_color="#1679EF",
            height=45,
            width=200,
            corner_radius=4,
            command=self.verify_user,  # Appelle la méthode de vérification
        )
        bouton.grid(row=0, column=0, padx=10)

        img_flch = Image.open("image/fleche10.png")
        flch_img = ImageTk.PhotoImage(img_flch)
        lbl_flch = CTkLabel(master=frm_btn, fg_color="#F2F7F9", image=flch_img, text="")
        lbl_flch.grid(row=0, column=1)

        frm_btn.place(x=533, y=280)

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

    def verify_user(self):
        """
        Vérifie les informations de l'utilisateur (nom d'utilisateur et mot de passe).
        """
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        try:
            # Requête SQL pour vérifier si l'utilisateur existe
            self.cursor.execute(
                "SELECT * FROM person WHERE username = ? AND password = ?",
                (username, password),
            )
            result = self.cursor.fetchone()

            if result:
                # Si l'utilisateur est trouvé, passer à l'interface suivante
                print("Succès", "Connexion réussie.")
                self.switch_to_page10fr()
            else:
                # Sinon, afficher une erreur
                print("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

        except Exception as e:
            print("Erreur", f"Une erreur s'est produite : {e}")

    def switch_to_page10fr(self):
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Create an instance of LanguageInterface from page2.py
        Page10FR(self.master, self, self.cursor, self.conn)

    def switch_to_main_interface(self):
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        self.main_app.switch_to_main_interface()  # Changez cette ligne selon votre logique

    def return_to_main(self):
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        self.main_app.switch_to_main_interface()


if __name__ == "__main__":
    root = Tk()
    app = Page9FR()
    root.mainloop()
