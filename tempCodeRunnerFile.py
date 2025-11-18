 self.title("Insert dan Read Data Nilai")
        self.geometry("600x420")

        frm = tk.Frame(self, bg="#ffffff", padx=12, pady=12)
        frm.pack(padx=16, pady=12, fill="x")

        tk.Label(frm, text="Nama:", bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.ent_name = tk.Entry(frm, width=30)
        self.ent_name.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Biologi :", bg="#ffffff").grid(row=1, column=0, sticky="w")
        self.ent_age = tk.Entry(frm, width=30)
        self.ent_age.grid(row=1, column=1, sticky="w", padx=6, pady=6) 

        tk.Label(frm, text="Fisika :", bg="#ffffff").grid(row=1, column=0, sticky="w")
        self.ent_age = tk.Entry(frm, width=30)
        self.ent_age.grid(row=1, column=1, sticky="w", padx=6, pady=6) 

        tk.Label(frm, text="Inggris :", bg="#ffffff").grid(row=1, column=0, sticky="w")
        self.ent_age = tk.Entry(frm, width=30)
        self.ent_age.grid(row=1, column=1, sticky="w", padx=6, pady=6) 