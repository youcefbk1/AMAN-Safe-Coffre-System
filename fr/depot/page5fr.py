from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import locale
from fr.depot.page6fr import Page6FR
import paramiko


class Page5FR:
    def __init__(self, master, main_app, cursor, conn):
        self.master = master
        self.main_app = main_app  # Save the MainApplication instance
        self.cursor = cursor  # Save the cursor
        self.conn = conn  # Save the conn
        # Start Raspberry Pi script remotely via SSH
        self.start_raspberry_script()

        self.setup_gui()

    def start_raspberry_script(self):
        """
        Starts the Raspberry Pi script remotely using SSH.
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to Raspberry Pi (Change IP, username, and password)
            ssh.connect(hostname="raspberrypi.local", username="aman", password="aman")

            # Kill any previous instance of the script
            ssh.exec_command("pkill -f raspberry_script.py")

            # Start the Raspberry Pi script in the background
            ssh.exec_command(
                "lxterminal -e 'python3 /home/aman/aman/raspberry_script.py'"
            )
            print("Raspberry Pi script started successfully.")
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

        self.frm1 = Frame(self.master, bg="#1679EF", height=50)
        self.frm1.pack(fill=X, side=TOP, pady=15)

        # partie redimentionnage et creatin image logo h'en haut(AMAN BLANC)
        old_image_frm1 = Image.open("image/AMAN-BLEU.png")  # importe l'image image
        resized_frm1 = old_image_frm1.resize(
            (60, 50), Image.LANCZOS
        )  # redimentioner l'image
        self.new_image_frm1 = ImageTk.PhotoImage(
            resized_frm1
        )  # image  final    ---------- si tu veux faire des modifs cest cette Var que tu va utiliser

        self.label1 = Label(
            self.frm1, image=self.new_image_frm1, highlightthickness=0, bd=0
        )  # afficher l'image(image rahi f label)
        self.label1.image = self.new_image_frm1
        self.label1.pack(expand=YES)

        self.frm2 = Frame(self.master, bg="#F2F7F9", height=360, width=800)

        lbl_msg = Label(
            self.frm2,
            text="Veuillez sélectionner le volume qui vous convient",
            font=(("Arial", 17, "bold")),
            bg="#F2F7F9",
            fg="#095CD3",
        )
        lbl_msg.place(x=100, y=3)

        # diagramme
        img_diag = Image.open("fr/image/diagramme4.png")
        self.image_diag = ImageTk.PhotoImage(img_diag)
        self.lbl_diag = Label(self.frm2, image=self.image_diag, bg="#F2F7F9", bd=0)
        self.lbl_diag.image = self.image_diag

        self.lbl_diag.place(x=80, y=60)

        btn1 = CTkButton(
            master=self.frm2,
            text="Volume A",
            font=("Arial", 27),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=250,
            height=50,
            border_width=0,
            corner_radius=4,
            command=lambda: self.switch_to_page6fr("A"),
        )
        btn1.place(x=485, y=50)

        btn2 = CTkButton(
            master=self.frm2,
            text="Volume B",
            font=("Arial", 27),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=250,
            height=50,
            border_width=0,
            corner_radius=4,
            command=lambda: self.switch_to_page6fr("B"),
        )
        btn2.place(x=485, y=150)

        btn3 = CTkButton(
            master=self.frm2,
            text="Volume C",
            font=("Arial", 27),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=250,
            height=50,
            border_width=0,
            corner_radius=4,
            command=lambda: self.switch_to_page6fr("C"),
        )
        btn3.place(x=485, y=250)

        # partie fleche

        image_flch1 = Image.open("image/fleche3.png")
        self.img_flch1 = ImageTk.PhotoImage(image_flch1)
        self.label_flch1 = Label(self.frm2, image=self.img_flch1, bg="#F2F7F9")
        self.label_flch1.image = self.img_flch1
        self.label_flch1.place(x=735, y=43)

        image_flch2 = Image.open("image/fleche3.png")
        self.img_flch2 = ImageTk.PhotoImage(image_flch2)
        self.label_flch2 = Label(self.frm2, image=self.img_flch2, bg="#F2F7F9")
        self.label_flch2.image = self.img_flch2
        self.label_flch2.place(x=735, y=243)

        image_flch3 = Image.open("image/fleche3.png")
        self.img_flch3 = ImageTk.PhotoImage(image_flch3)
        self.label_flch3 = Label(self.frm2, image=self.img_flch3, bg="#F2F7F9")
        self.label_flch3.image = self.img_flch3
        self.label_flch3.place(x=735, y=143)

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

        self.frm2.pack()

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

    def switch_to_page6fr(self,volume):
        casier_value = 0
        if volume == "A":
            casier_value = 1
        elif volume == "B":
            casier_value = 2
        elif volume == "C":
            casier_value = 3

        try:
            # Met à jour la table `user` pour définir le casier
            self.cursor.execute("SELECT id FROM person WHERE actif = 1")
            utilisateur_actif = self.cursor.fetchone()
            utilisateur_id = utilisateur_actif[0]
            self.cursor.execute(
                "UPDATE person SET casier = ? WHERE id = ?",
                (casier_value, utilisateur_id),
            )  # Remplacez 1 par l'ID utilisateur actuel
            self.conn.commit()
            print(f"Casier mis à jour à {casier_value} pour l'utilisateur.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour du casier : {e}")

        # Change vers la page suivante
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        Page6FR(self.master, self, self.cursor, self.conn)

    def return_to_main(self):
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
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Hide the language interface
        # Show the main interface
        self.main_app.switch_to_main_interface()


if __name__ == "__main__":
    root = Tk()
    app = Page5FR(root)
    root.mainloop()
