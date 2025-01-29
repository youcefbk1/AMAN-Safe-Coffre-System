from tkinter import *
from tkinter import messagebox  # Pour afficher des messages d'erreur
from customtkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import locale

import paramiko
from fr.retrait.page10fr import Page10FR


class Page9FR:
    def __init__(self, master, main_app, cursor, conn):
        self.master = master
        self.main_app = main_app  # Save the MainApplication instance
        self.cursor = cursor  # Save the cursor
        self.conn = conn  # Save the conn

        # Fetch username automatically from the database
        self.fetch_username()
        self.setup_gui()



    def start_raspberry_script(self):
        """
        Reads the casier value from the 'person' table and starts the corresponding
        Raspberry Pi script remotely using SSH.
        """
        try:
            # Fetch the casier ID from the active user in the database
            self.cursor.execute("SELECT casier FROM person WHERE actif = ?", (1,))
            result = self.cursor.fetchone()

            if not result:
                print("No active user found or casier ID missing.")
                return

            casier_id = result[0]  # Get the casier ID

            # Map casier_id to the corresponding script
            script_mapping = {1: "open_relay1.py", 2: "open_relay2.py", 3: "open_relay3.py"}

            script_name = script_mapping.get(casier_id)

            if not script_name:
                print(f"Invalid casier ID: {casier_id}")
                return

            # SSH connection to Raspberry Pi
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to Raspberry Pi (update IP, username, and password if necessary)
            ssh.connect(hostname="raspberrypi.local", username="aman", password="aman")

            # Kill any previous instance of the script
            ssh.exec_command("pkill -f open_relay.py")
            ssh.exec_command("pkill -f open_relay1.py")
            ssh.exec_command("pkill -f open_relay2.py")
            ssh.exec_command("pkill -f open_relay3.py")

            # Start the corresponding script based on the casier ID
            ssh.exec_command(f"lxterminal -e 'python3 /home/aman/aman/{script_name}'")

            print(f"Started {script_name} successfully on Raspberry Pi.")
            ssh.close()

        except Exception as e:
            print(f"Error starting Raspberry Pi script: {e}")

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

        # Entry fields
        self.entry_username = CTkEntry(
            master=frm_info,
            fg_color="#F2F7F9",
            text_color="black",
            font=("Arial", 20),
            border_color="#1679EF",
            border_width=2.5,
            width=200,
            state="disabled",  # Make this field read-only
        )
        self.entry_username.grid(row=0, column=1, padx=10, pady=15)

        # Pre-fill the username field
        if self.active_username:
            self.entry_username.configure(state="normal")  # Enable entry to insert text
            self.entry_username.insert(0, self.active_username)
            self.entry_username.configure(
                state="disabled"
            )  # Disable again after filling

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

        # Label d'erreur (caché par défaut)
        self.lbl_error = CTkLabel(
            master=frm_info,
            text="",
            font=("Arial", 16, "bold"),
            text_color="red",
            fg_color="#F2F7F9",
        )
        self.lbl_error.grid(row=2, column=1, padx=10, pady=5)

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

    def fetch_username(self):
        """
        Fetches the active username from the database where 'actif = 1'.
        Stores it in a global variable.
        """
        try:
            self.cursor.execute("SELECT username FROM person WHERE actif = 1")
            result = self.cursor.fetchone()

            if result:
                self.active_username = result[0]  # Store in global variable
            else:
                messagebox.showerror("Erreur", "Aucun utilisateur actif trouvé.")
                self.active_username = ""  # Set empty if no active user
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Une erreur s'est produite lors de la récupération du nom d'utilisateur : {e}",
            )
            self.active_username = ""  # Ensure no crash

    def verify_user(self):
        """
        Vérifie les informations de l'utilisateur (nom d'utilisateur et mot de passe).
        """
        username = self.active_username  # Utilise l'username récupéré automatiquement
        password = self.entry_password.get().strip()

        if not password:
            self.lbl_error.configure(text="Veuillez entrer un mot de passe.")  # Affiche un message d'erreur
            return

        try:
            self.cursor.execute(
                "SELECT * FROM person WHERE username = ? AND password = ?",
                (username, password),
            )
            result = self.cursor.fetchone()

            if result:
                self.lbl_error.configure(text="")  # Efface l'erreur s'il y en avait une
                print("Succès", "Connexion réussie.")
                # Start Raspberry Pi script remotely via SSH
                self.start_raspberry_script()
                self.switch_to_page10fr()
                self.delete_user()
            else:
                self.lbl_error.configure(text="Mot de passe incorrect.")  # Affiche l'erreur en rouge sous le champ

        except Exception as e:
            self.lbl_error.configure(text="Erreur lors de la connexion.")  # Gère l'erreur SQL

    def delete_user(self):
        """
        Supprime l'utilisateur actif de la base de données.
        """
        try:
            self.cursor.execute("DELETE FROM person WHERE actif = 1")
            self.conn.commit()
            print("Utilisateur supprimé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la suppression de l'utilisateur : {e}")
            
            
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
    app = Page9FR()
    root.mainloop()
