from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import locale
import arabic_reshaper
import bidi.algorithm
import serial
from ar.depotAR.page8ar import Page8AR


class Page7AR:
    def __init__(
        self,
        master,
        main_app,
        cursor,
        conn,
    ):
        self.master = master
        self.main_app = main_app
        self.cursor = cursor
        self.conn = conn
        self.casier_id = None  # Initialize with a default locker ID
        # self.stop_signal_check = False  # Flag to stop the signal check loop
        self.price = self.get_active_user_price()  # Fetch the active user's price
        self.casier_num()  # Call the method to populate self.casier_id

        # Check if the UART connection is already open
        if not hasattr(self, "uart") or not self.uart.is_open:
            self.uart = serial.Serial(
                port="COM3",
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1,
            )

        self.inactivity_timer = None  # Initialize the inactivity timer
        self.setup_gui()
        self.reset_timer()  # Start the inactivity timer
        self.send_data_to_raspberry()  # Send the price to the Raspberry Pi
        self.wait_for_signal()  # Start waiting for the "done" signal

    def casier_num(self):
        """
        Fetches the casier ID for the active user from the 'person' table.
        """
        try:
            # Query to fetch casier ID for the active user
            self.cursor.execute("SELECT casier FROM person WHERE actif = ?", (1,))
            result = self.cursor.fetchone()
            if result:
                self.casier_id = result[0]  # Store the casier_id
                print(f"Fetched Casier ID: {self.casier_id}")
            else:
                print("No active user or casier ID found.")
        except Exception as e:
            print(f"Error fetching casier ID: {e}")

    def wait_for_signal(self):
        """
        Waits for the "done" signal from the Raspberry Pi via UART.
        """
        try:
            # if self.stop_signal_check:
            #     return  # Exit the loop if the flag is set
            if self.uart.is_open:
                # Check for incoming data
                print("uart is open, waiting for signal")
                data = self.uart.readline().decode("utf-8").strip()
                if data == "done":
                    print("Signal received: Payment successful.")
                    self.switch_to_page8ar()
                    self.paid()  # Mark the user as paid in the database
                else:
                    # Retry after 500ms
                    self.master.after(500, self.wait_for_signal)
            else:
                print("UART connection is not openNNNNNN.")
                # self.master.after(500, self.wait_for_signal)
        except Exception as e:
            print(f"Error waiting for signal: {e}")
            self.master.after(500, self.wait_for_signal)

    def paid(self):
        """
        Update the 'paid' column in the 'person' table to mark the user as paid.
        """
        try:
            self.cursor.execute("UPDATE person SET paid = 1 WHERE actif = 1")
            self.conn.commit()
            print("User marked as paid.")
        except Exception as e:
            print(f"Error marking user as paid: {e}")

    def send_data_to_raspberry(self):
        """
        Sends the price and casier_id to the Raspberry Pi via UART.
        """
        try:
            if self.uart.is_open:
                # Combine price and casier_id into a single string
                data_to_send = (
                    f"{self.price}:{self.casier_id}"  # Format: "price:casier_id"
                )
                self.uart.write(data_to_send.encode("utf-8"))
                print(f"Data sent to Raspberry Pi: {data_to_send}")
            else:
                print("UART connection is not open.")
        except Exception as e:
            print(f"Error sending data to Raspberry Pi: {e}")

    def get_active_user_price(self):
        """
        Fetches the price for the active user from the 'person' table.
        """
        try:
            self.cursor.execute("SELECT price FROM person WHERE actif = ?", (1,))
            result = self.cursor.fetchone()
            if result:
                return result[0]  # Return the price
            else:
                print("No active user found.")
                return 0  # Default value if no active user
        except Exception as e:
            print(f"Error fetching price: {e}")
            return 0  # Default value in case of error

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

        # according to the selected self.casier_id color the box below with blue and turn text to white
        if self.casier_id == 1:
            box1.configure(fg_color="#1679EF", text_color="#FFFFFF")
        elif self.casier_id == 2:
            box5.configure(fg_color="#1679EF", text_color="#FFFFFF")
        elif self.casier_id == 3:
            box13.configure(fg_color="#1679EF", text_color="#FFFFFF")

        self.frm_msg = CTkFrame(master=self.frm2, fg_color="#F2F7F9")

        label_msg = CTkLabel(
            master=self.frm_msg,
            text="المبلغ الإجمالي الذي عليك دفعه",
            font=("Arial", 30, "bold"),
            fg_color="#F2F7F9",
            text_color="#095CD3",
        )
        label_msg.grid(row=0, column=0, pady=30)

        # case prix
        reshaped_text = arabic_reshaper.reshape("400 دج")
        text = bidi.algorithm.get_display(reshaped_text)
        # Dynamically set the price for the active user
        label_price = CTkLabel(
            master=self.frm_msg,
            text=f"{self.price}دج ",
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
            text="خروج",
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

    def switch_to_page8ar(self):
        self.reset_timer()  # Reset the timer on interaction
        # Change vers la page suivante
        if hasattr(self, "uart") and self.uart.is_open:
            self.uart.close()
            print("Connexion UART fermée.")

        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        self.master.update_idletasks()  # Ensure GUI refresh before switching
        Page8AR(self.master, self, self.cursor, self.conn)

    def return_to_main(self):
        self.reset_timer()  # Reset the timer on interaction
        """
        Handles the return to the main interface by closing the UART connection,
        deleting unpaid active users, and restarting the main application.
        """
        if hasattr(self, "uart") and self.uart.is_open:
            self.uart.close()
            print("Connexion UART fermée.")
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
        self.frm_box.place_forget()
        self.main_app.switch_to_main_interface()

    def __del__(self):
        if hasattr(self, "uart") and self.uart.is_open:
            self.uart.close()
            print("Connexion UART fermée.")

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
    app = Page7AR(root)
    root.mainloop()
