from tkinter import *
from customtkinter import *
from PIL import Image,ImageTk
from datetime import datetime
import locale

class Page5fr:
  
    def __init__(self, master, main_app, cursor, conn):
        self.master = master
        self.main_app = main_app  # Save the MainApplication instance
        self.cursor = cursor  # Save the cursor
        self.conn = conn  # Save the conn
        self.setup_gui()

    def setup_gui(self):
        # Met la localisation suivant la France permet d'avoir la langue française pour la date
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

        self.master.title("Langue")
        self.master.iconbitmap("image/AMAN-LOGO.ico")
        self.master.geometry("800x480")
        self.master.minsize(800, 480)
        self.master.maxsize(800, 480)
        self.master.config(bg="#F2F7F9")

        self.frm1 = Frame(self.master, bg="#1679EF", height=50)
        self.frm1.pack(fill=X, side=TOP, pady=15)

        self.old_image_frm1 = Image.open("image/AMAN-BLEU.png")
        self.resized_frm1 = self.old_image_frm1.resize((60, 50), Image.LANCZOS)
        self.new_image_frm1 = ImageTk.PhotoImage(self.resized_frm1)
        self.label1 = Label(
            self.frm1, image=self.new_image_frm1, highlightthickness=0, bd=0
        )
        self.label1.image = (
            self.new_image_frm1
        )  # Keep a reference to avoid garbage collection
        self.label1.pack(expand=YES)

        self.image = Image.open("image/fleche3.png")
        self.img = ImageTk.PhotoImage(self.image)

        self.frm2 = Frame(self.master, bg="#F2F7F9", width=800, height=360)

        self.bouton1 = CTkButton(
            master=self.frm2,
            text="Français",
            fg_color="#1679EF",
            text_color="#F2F7F9",
            font=(("Arial"), 28),
            width=170,
            height=50,
            border_width=0,
            corner_radius=4,
            command=self.switch_to_page3fr,  # Call switch_to_page3fr when the button is clicked
        )
        self.bouton1.place(x=565, y=65)
        self.label1 = Label(self.frm2, image=self.img, bg="#F2F7F9")
        self.label1.place(x=735, y=59)

        self.bouton2 = CTkButton(
            master=self.frm2,
            text="العربية",
            fg_color="#1679EF",
            text_color="#F2F7F9",
            font=(("Arial"), 28),
            width=170,
            height=50,
            border_width=0,
            corner_radius=4,
            command=self.switch_to_page3ar,  # Call switch_to_page3ar when the button is clicked
        )
        self.bouton2.place(x=565, y=160)
        self.label2 = Label(self.frm2, image=self.img, bg="#F2F7F9")
        self.label2.place(x=735, y=154)

        self.bouton3 = CTkButton(
            master=self.frm2,
            text="Sortie  خروج ",
            fg_color="#1679EF",
            text_color="#F2F7F9",
            font=(("Arial"), 28),
            width=170,
            height=50,
            border_width=0,
            corner_radius=4,
            command=self.return_to_main,
        )
        self.bouton3.place(x=565, y=260)
        self.label3 = Label(self.frm2, image=self.img, bg="#F2F7F9")
        self.label3.place(x=735, y=254)

        self.label = Label(
            self.frm2,
            text="S'il vous plaît, choisissez votre langue \n\n من فضلك، اختر لغتك ",
            bg="#F2F7F9",
            fg="#095CD3",
            font=("Arial", 21, "bold"),
        )
        self.label.place(x=30, y=80)
        self.frm2.pack()

        self.frm3 = Frame(self.master, bg="#1679EF", height=30)
        date = datetime.now()
        self.label2 = Label(
            self.frm3,
            text=f"{date:%d-%m-%Y}  /  {date:%I:%M}",
            font=("Arial", 12),
            fg="#F2F7F9",
            bg="#1679EF",
        )
        self.label2.pack(expand=YES)
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
    app = Page5fr(root)
    root.mainloop()  
  

  
# #met la localisatin suivant la france      permet davoir la langue française pour la date
# locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')


# root = Tk()
# root.title('AMAN')
# root.iconbitmap('image/AMAN-LOGO.ico')
# root.geometry("800x480")
# root.minsize(800, 480)
# root.maxsize(800, 480)
# root.config(bg='#F2F7F9')

# frm1 = Frame(root, bg='#1679EF', height=50)
# frm1.pack(fill=X, side=TOP,pady=15)

# #partie redimentionnage et creatin image logo h'en haut(AMAN BLANC)    
# old_image_frm1 = Image.open('image/AMAN-BLEU.png') # importe l'image image   
# resized_frm1 = old_image_frm1.resize((60, 50), Image.LANCZOS)  # redimentioner l'image    
# new_image_frm1 = ImageTk.PhotoImage(resized_frm1)   # image  final    ---------- si tu veux faire des modifs cest cette Var que tu va utiliser
# label1 = Label(frm1, image=new_image_frm1,highlightthickness=0,bd=0)#afficher l'image(image rahi f label)
# label1.pack(expand=YES)



# frm2 = Frame(root,bg='#F2F7F9',height=360,width=800)

# lbl_msg  = Label(frm2,text="Veuillez sélectionner le volume qui vous convient",font=(('Arial',17,"bold")),bg='#F2F7F9',fg='#095CD3')
# lbl_msg.place(x=100,y=3)

# #diagramme
# img_diag = Image.open('fr/image/diagramme4.png')
# image_diag = ImageTk.PhotoImage(img_diag)
# lbl_diag = Label(frm2,image=image_diag,bg='#F2F7F9',bd=0)
# lbl_diag.place(x =80,y= 60)


# btn1 = CTkButton(master=frm2,
#                  text='Volume A',
#                  font=('Arial',27),
#                  fg_color='#1679EF',
#                  text_color='#F2F7F9',
#                  width=250,
#                  height=50,
#                  border_width=0,
#                  corner_radius=4)
# btn1.place(x=485,y=50)

# btn2 = CTkButton(master=frm2,
#                  text='Volume B',
#                  font=('Arial',27),
#                  fg_color='#1679EF',
#                  text_color='#F2F7F9',
#                  width=250,height=50,
#                  border_width=0,
#                  corner_radius=4)
# btn2.place(x=485,y=150)

# btn3 = CTkButton(master=frm2,
#                  text='Volume C',
#                  font=('Arial',27),
#                  fg_color='#1679EF',
#                  text_color='#F2F7F9',
#                  width=250,
#                  height=50,
#                  border_width=0,
#                  corner_radius=4)
# btn3.place(x=485,y=250)

# #partie fleche

# image_flch1  = Image.open('image/fleche3.png')
# img_flch1 = ImageTk.PhotoImage(image_flch1)
# label_flch1 = Label(frm2,image=img_flch1,bg='#F2F7F9')
# label_flch1.place(x=735,y=43)


# image_flch2  = Image.open('image/fleche3.png')
# img_flch2 = ImageTk.PhotoImage(image_flch2)
# label_flch2 = Label(frm2,image=img_flch2,bg='#F2F7F9')
# label_flch2.place(x=735,y=243)


# image_flch3  = Image.open('image/fleche3.png')
# img_flch3 = ImageTk.PhotoImage(image_flch3)
# label_flch3 = Label(frm2,image=img_flch3,bg='#F2F7F9')
# label_flch3.place(x=735,y=143)






# btn_srt = CTkButton(master=frm2,
#                     text='Sortie',
#                     font=('Arial',20),
#                     fg_color='#1679EF',
#                     text_color='#F2F7F9',
#                     width=100,
#                     height=30,
#                     border_width=0,
#                     corner_radius=3)
# btn_srt.place(x=40,y=320)


# image_flch_srt  = Image.open('image/fleche3.png')
# rotated_img = image_flch_srt.rotate(180)
# resize = rotated_img.resize((35,35),Image.LANCZOS)
# img_flch_srt = ImageTk.PhotoImage(resize)
# label_flch_srt = Label(frm2,image=img_flch_srt,bg='#F2F7F9')
# label_flch_srt.place(x=1,y=316)

# frm2.pack()


# frm3 = Frame(root, bg='#1679EF', height=30)
# date=datetime.now()
# label2 = Label(frm3,text=f"{date:%d-%m-%Y}  /  {date:%I:%M}",font=('Arial',12),fg='#F2F7F9',bg='#1679EF')
# label2.pack(expand=YES)

# frm3.pack(fill=X, side=BOTTOM)

# root.mainloop()