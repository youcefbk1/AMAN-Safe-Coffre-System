from tkinter import *
from customtkinter import *
from PIL import Image,ImageTk
from datetime import datetime
import locale

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
        self.frm1 = Frame(self.master, bg='#1679EF', height=50)
        self.frm1.pack(fill=X, side=TOP, pady=15)

        # logo
        old_image_frm1 = Image.open('image/AMAN-BLEU.png')
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
            text="veuillez remplir les informations suivantes",
            font=("Arial", 28, "bold"),
            text_color="#095CD3",
            fg_color="#F2F7F9",
        )
        lbl_msg.place(x = 115 , y=30)

        frm_info = CTkFrame(master=self.frm2, fg_color="#F2F7F9")
        lbl1 = CTkLabel(master=frm_info,text="Nom d'utilisateur",font=('Arial',20,"bold"),fg_color='#F2F7F9',text_color='#1679EF')
        lbl1.grid(row=0,column=0,padx=10,pady=15,sticky='w')

        lbl2 = CTkLabel(master=frm_info,text="Mot de passe",font=('Arial',20,"bold"),fg_color='#F2F7F9',text_color='#1679EF')
        lbl2.grid(row=1,column=0,padx=10,pady=15,sticky='w')

        entry1 = CTkEntry(master=frm_info,fg_color='#F2F7F9',text_color='black',font=('Arial',20),border_color='#1679EF',border_width=2.5,width=200)
        entry1.grid(row=0,column=1,padx=10,pady=15)

        entry2 = CTkEntry(master=frm_info,fg_color='#F2F7F9',text_color='black',font=('Arial',20),border_color='#1679EF',border_width=2.5,width=200)
        entry2.grid(row=1,column=1,padx=10,pady=15)

        frm_info.place(x=385,y=100)

        frm_btn = CTkFrame(master=self.frm2, fg_color="#F2F7F9")
        bouton = CTkButton(master=frm_btn,text='Confimer',font=('Arial',25),text_color='#F2F7F9',fg_color='#1679EF',height=45,width=200,corner_radius=4)
        bouton.grid(row=0,column=0,padx=10)

        img_flch = Image.open('image/fleche10.png')
        flch_img = ImageTk.PhotoImage(img_flch)
        lbl_flch = CTkLabel(master=frm_btn,fg_color='#F2F7F9',image=flch_img,text="")
        lbl_flch.grid(row=0,column=1)

        frm_btn.place(x=533,y=280)

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
            command= self.return_to_main,
        )
        btn_srt.place(x=40,y=320)

        image_flch_srt  = Image.open('image/fleche3.png')
        rotated_img = image_flch_srt.rotate(180)
        resize = rotated_img.resize((35,35),Image.LANCZOS)
        self.img_flch_srt = ImageTk.PhotoImage(resize)
        self.label_flch_srt = Label(self.frm2, image=self.img_flch_srt, bg="#F2F7F9")
        self.label_flch_srt.image = self.img_flch_srt
        self.label_flch_srt.place(x=1, y=316)

        self.frm3 = Frame(self.master, bg="#1679EF", height=30)
        date=datetime.now()
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
        # Hide the language interface
        # Show the main interface
        self.main_app.switch_to_main_interface()

    def switch_to_main_interface(self):
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Hide the language interface
        # Show the main interface
        self.main_app.switch_to_main_interface()



if __name__ == "__main__":
    root = Tk()
    app = Page9FR(root)
    root.mainloop()
