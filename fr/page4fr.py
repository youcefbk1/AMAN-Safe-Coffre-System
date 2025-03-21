from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import locale
from fr.depot.page5fr import Page5FR
from fr.retrait.page9fr import Page9FR


class Page4FR:
    def __init__(self, master, main_app, cursor, conn):
        self.master = master
        self.main_app = main_app  # Save the MainApplication instance
        self.cursor = cursor  # Save the cursor
        self.conn = conn  # Save the conn
        self.inactivity_timer = None  # Initialize the inactivity timer
        self.setup_gui()
        self.reset_timer()  # Start the inactivity timer

    def setup_gui(self):
        # Set French locale for date
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

        # Initialize main window
        self.master.title("AMAN")
        self.master.iconbitmap("image/AMAN-LOGO.ico")
        self.master.geometry("1920x1200")
        self.master.minsize(1920, 1200)
        self.master.maxsize(1920, 1200)
        self.master.config(bg="#F2F7F9")

        # Top blue bar
        self.frm1 = Frame(self.master, bg="#1679EF", height=100)
        self.frm1.pack(fill=X, side=TOP)

        # AMAN logo in top bar
        old_image_frm1 = Image.open("image/AMAN-BLEU.png")
        resized_frm1 = old_image_frm1.resize((120, 100), Image.LANCZOS)
        self.new_image_frm1 = ImageTk.PhotoImage(resized_frm1)
        self.label1 = Label(
            self.frm1, image=self.new_image_frm1, highlightthickness=0, bd=0
        )
        self.label1.image = self.new_image_frm1
        self.label1.pack(expand=YES)

        # Central part (content)
        self.frm2 = Frame(self.master, bg="#F2F7F9")

        # Message at the top
        label_msg = Label(
            self.frm2,
            text="Merci de bien vouloir choisir parmi\n les options suivantes en sélectionnant votre préférence",
            font=("Arial", 36, "bold"),
            fg="#095CD3",
            bg="#F2F7F9",
        )
        label_msg.place(x=120, y=20)

        # Buttons
        self.btn1 = CTkButton(
            self.frm2,
            text="Dépôt",
            font=("Arial", 54),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=700,
            height=100,
            border_width=0,
            corner_radius=4,
            command=self.switch_to_page5fr,
        )
        self.btn1.place(x=770, y=260)

        self.btn2 = CTkButton(
            master=self.frm2,
            text="Retrait",
            font=("Arial", 54),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=700,
            height=100,
            border_width=0,
            corner_radius=4,
            command=self.switch_to_page9fr,
        )
        self.btn2.place(x=770, y=460)

        # Arrow images
        image_flch = Image.open("image/fleche3.png")

        img_flch = ImageTk.PhotoImage(image_flch.resize((100, 100), Image.LANCZOS))
        label_flch = Label(self.frm2, image=img_flch, bg="#F2F7F9")
        label_flch.image = img_flch  # Keep a reference to the image object
        label_flch.place(x=1450, y=460)

        label_flch2 = Label(self.frm2, image=img_flch, bg="#F2F7F9")
        label_flch2.image = img_flch  # Keep a reference to the image object
        label_flch2.place(x=1450, y=260)

        # Exit button
        self.btn_srt = CTkButton(
            master=self.frm2,
            text="Sortie",
            font=("Arial", 40),
            fg_color="#1679EF",
            text_color="#F2F7F9",
            width=200,
            height=60,
            border_width=0,
            corner_radius=3,
            command=self.return_to_main,
        )
        self.btn_srt.place(x=80, y=640)

        # Arrow image for exit button
        rotated_img = image_flch.rotate(180)
        resize = rotated_img.resize((70, 70), Image.LANCZOS)
        img_flch_srt = ImageTk.PhotoImage(resize)
        label_flch_srt = Label(self.frm2, image=img_flch_srt, bg="#F2F7F9")
        label_flch_srt.image = img_flch_srt  # Keep a reference to the image object
        label_flch_srt.place(x=2, y=632)

        self.frm2.pack(expand=YES, fill=BOTH)

        # Bottom blue bar
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

    def switch_to_page5fr(self):
        self.reset_timer()  # Reset the timer on interaction
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Create an instance of LanguageInterface from page2.py
        Page5FR(self.master, self, self.cursor, self.conn)

    def switch_to_page9fr(self):
        self.reset_timer()  # Reset the timer on interaction
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Create an instance of LanguageInterface from page2.py
        Page9FR(self.master, self, self.cursor, self.conn)

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
        # Hide the language interface
        # Show the main interface
        self.main_app.switch_to_main_interface()

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
    app = Page4FR(root)
    root.mainloop()
