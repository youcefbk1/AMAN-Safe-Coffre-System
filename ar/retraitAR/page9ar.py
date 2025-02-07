from tkinter import *
from customtkinter import *
from tkinter import messagebox  # Pour afficher des messages d'erreur
from PIL import Image, ImageTk
from datetime import datetime
import locale
import paramiko
from ar.retraitAR.page10ar import Page10AR


class Page9AR:
    def __init__(self, master, main_app, cursor, conn):
        self.master = master
        self.main_app = main_app  # Save the MainApplication instance
        self.cursor = cursor  # Save the cursor
        self.conn = conn  # Save the conn

        # Fetch username automatically from the database
        self.fetch_username()
        self.inactivity_timer = None  # Initialize the inactivity timer
        self.setup_gui()
        self.reset_timer()  # Start the inactivity timer

    def setup_gui(self):
        # Set locale for French date format
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

        self.master.title("AMAN")
        self.master.iconbitmap("image/AMAN-LOGO.ico")
        self.master.geometry("1920x1200")
        self.master.minsize(1920, 1200)
        self.master.maxsize(1920, 1200)
        self.master.config(bg="#F2F7F9")

        # Top blue bar
        self.frm1 = Frame(self.master, bg="#1679EF", height=100)
        self.frm1.pack(fill=X, side=TOP)

        # AMAN logo
        old_image_frm1 = Image.open("image/AMAN-BLEU.png")
        resized_frm1 = old_image_frm1.resize((120, 100), Image.LANCZOS)
        new_image_frm1 = ImageTk.PhotoImage(resized_frm1)
        self.label1 = Label(self.frm1, image=new_image_frm1, highlightthickness=0, bd=0)
        self.label1.image = new_image_frm1
        self.label1.pack(expand=YES)

        # Partie central (contenu)
        self.frm2 = Frame(self.master, bg="#F2F7F9")

        lbl_msg = CTkLabel(
            master=self.frm2,
            text="يرجى ملء المعلومات التالية",
            font=("Arial", 60, "bold"),
            text_color="#095CD3",
            fg_color="#F2F7F9",
        )
        lbl_msg.place(x=840, y=60)

        frm_info = CTkFrame(master=self.frm2, fg_color="#F2F7F9")
        lbl1 = CTkLabel(
            master=frm_info,
            text="إسم المستخدم",
            font=("Arial", 44, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        lbl1.grid(row=0, column=1, padx=20, pady=30, sticky="e")

        lbl2 = CTkLabel(
            master=frm_info,
            text="كلمة السر",
            font=("Arial", 44, "bold"),
            fg_color="#F2F7F9",
            text_color="#1679EF",
        )
        lbl2.grid(row=1, column=1, padx=20, pady=30, sticky="e")

        # Entry fields
        self.entry_username = CTkEntry(
            master=frm_info,
            fg_color="#F2F7F9",
            text_color="black",
            font=("Arial", 40),
            border_color="#1679EF",
            border_width=5,
            width=400,
            state="disabled",  # Make this field read-only
        )
        self.entry_username.grid(row=0, column=0, padx=20, pady=30)

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
            font=("Arial", 40),
            border_color="#1679EF",
            border_width=5,
            width=400,
            show="*",
        )
        self.entry_password.grid(row=1, column=0, padx=20, pady=30)

        # Label d'erreur (caché par défaut)
        self.lbl_error = CTkLabel(
            master=frm_info,
            text="",
            font=("Arial", 32, "bold"),
            text_color="red",
            fg_color="#F2F7F9",
        )
        self.lbl_error.grid(row=2, column=0, padx=20, pady=10)

        frm_info.place(x=860, y=200)

        frm_btn = CTkFrame(master=self.frm2, fg_color="#F2F7F9")
        bouton = CTkButton(
            master=frm_btn,
            text="دخول",
            font=("Arial", 50),
            text_color="#F2F7F9",
            fg_color="#1679EF",
            height=90,
            width=400,
            corner_radius=4,
            command=self.verify_user,  # Appelle la méthode de vérification
        )
        bouton.grid(row=0, column=0, padx=20)

        img_flch = Image.open("image/fleche10.png")
        flch_img = ImageTk.PhotoImage(img_flch.resize((50, 50), Image.LANCZOS))
        lbl_flch = CTkLabel(master=frm_btn, fg_color="#F2F7F9", image=flch_img, text="")
        lbl_flch.grid(row=0, column=1)

        frm_btn.place(x=1026, y=510)

        self.frm2.pack(expand=YES, fill=BOTH)

        btn_srt = CTkButton(
            master=self.frm2,
            text="خروج",
            font=("Arial", 40),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=200,
            height=60,
            border_width=0,
            corner_radius=3,
            command=self.return_to_main,
        )
        btn_srt.place(x=80, y=600)

        image_flch_srt = Image.open("image/fleche3.png")
        rotated_img = image_flch_srt.rotate(180)
        resize = rotated_img.resize((70, 70), Image.LANCZOS)
        self.img_flch_srt = ImageTk.PhotoImage(resize)
        self.label_flch_srt = Label(self.frm2, image=self.img_flch_srt, bg="#F2F7F9")
        self.label_flch_srt.image = self.img_flch_srt
        self.label_flch_srt.place(x=2, y=592)

        self.frm3 = Frame(self.master, bg="#1679EF", height=60)
        date = datetime.now()
        label2 = Label(
            self.frm3,
            text=f"{date:%d-%m-%Y}  /  {date:%I:%M}",
            font=("Arial", 24),
            fg="#F2F7F9",
            bg="#1679EF",
        )
        label2.pack(expand=YES)

        self.frm3.pack(fill=X, side=BOTTOM)

    def start_raspberry_script(self, username, password):
        """
        Reads the casier value from the 'person' table and starts the corresponding
        Raspberry Pi script remotely using SSH.
        """
        try:
            # Fetch the casier ID from the user in the database
            self.cursor.execute(
                "SELECT casier FROM person WHERE username = ? AND password = ?",
                (username, password),
            )
            result = self.cursor.fetchone()

            if not result:
                print("No active user found or casier ID missing.")
                return

            casier_id = result[0]  # Get the casier ID

            # Map casier_id to the corresponding script
            script_mapping = {
                1: "open_relay1.py",
                2: "open_relay2.py",
                3: "open_relay3.py",
            }

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
            self.lbl_error.configure(
                text="Veuillez entrer un mot de passe."
            )  # Affiche un message d'erreur
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
                self.start_raspberry_script(username, password)
                self.switch_to_page10ar()
                self.delete_user()
            else:
                self.lbl_error.configure(
                    text=".كلمة السر غير صحيحة"
                )  # Affiche l'erreur en rouge sous le champ

        except Exception as e:
            self.lbl_error.configure(
                text="Erreur lors de la connexion."
            )  # Gère l'erreur SQL

    def delete_user(self):
        """
        Supprime l'utilisateur actif de la base de données.
        """
        try:
            self.cursor.execute("DELETE FROM person WHERE actif = 1")
            # Delete also from person where username = username and password = password
            self.cursor.execute(
                "DELETE FROM person WHERE username = ? AND password = ?",
                (self.active_username, self.entry_password.get().strip()),
            )
            self.conn.commit()
            print("Utilisateur supprimé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la suppression de l'utilisateur : {e}")

    def switch_to_page10ar(self):
        self.reset_timer()  # Reset the timer on interaction
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Create an instance of LanguageInterface from page2.py
        Page10AR(self.master, self, self.cursor, self.conn)

    def switch_to_main_interface(self):
        self.reset_timer()  # Reset the timer on interaction
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        self.main_app.switch_to_main_interface()  # Changez cette ligne selon votre logique

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

    def reset_timer(self):
        print("Resetting timer")
        if self.inactivity_timer is not None:
            self.master.after_cancel(self.inactivity_timer)
            print("Cancelled timer")
        else:
            self.inactivity_timer = self.master.after(
                120000, self.return_to_main
            )  # 1 minute = 120000 ms
            print("Starting timer")


if __name__ == "__main__":
    root = Tk()
    app = Page9AR(root)
    root.mainloop()
