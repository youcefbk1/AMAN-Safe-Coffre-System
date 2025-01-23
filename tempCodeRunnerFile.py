        # Bande bleue d'en bas
        self.frm3 = tk.Frame(self.master, bg="#1679EF", height=30)
        self.date_label = tk.Label(
            self.frm3,
            text=self.get_current_date_time(),
            font=("Arial", 12),
            fg="#F2F7F9",
            bg="#1679EF",
        )
        self.date_label.pack(expand=tk.YES)
        self.frm3.pack(fill=tk.X, side=tk.BOTTOM)

    def get_current_date_time(self):
        date = datetime.now()
        return f"{date:%d-%m-%Y}  /  {date:%I:%M}"

    def switch_to_language_interface(self):
        self.frm1.pack_forget()
        self.frm2.pack_forget()
        self.frm3.pack_forget()
        # Create an instance of LanguageInterface from page2.py
        LanguageInterface(self.master, self, self.cursor, self.conn)

    def switch_to_main_interface(self):
        # Show the main interface again
        self.frm1.pack(fill=tk.X, side=tk.TOP, pady=15)
        self.frm2.pack()
        self.frm3.pack(fill=tk.X, side=tk.BOTTOM)
