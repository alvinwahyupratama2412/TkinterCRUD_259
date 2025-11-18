import sqlite3
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk

def koneksi():
    con = sqlite3.connect("nilai.db")
    return con

def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Nilai (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            Biologi INTEGER,
            Fisika INTEGER,
            Inggris INTEGER,
            prediksi TEXT 
        )
    """)
    con.commit()
    con.close()

def insertnilai(name: str, Biologi: int, Fisika: int, Inggris: int):
    con = koneksi()
    cur = con.cursor()
    hasil = prediksi_jurusan(Biologi, Fisika, Inggris)
    cur.execute("INSERT INTO nilai (name, Biologi, Fisika, Inggris, prediksi) VALUES (?, ?, ?, ?, ?)", (name, Biologi, Fisika, Inggris, hasil))
    con.commit()
    rowid = cur.lastrowid
    con.close()
    return rowid

def readnilai():
    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT id, name, Biologi, Fisika, Inggris, prediksi FROM Nilai ORDER BY id")
    rows = cur.fetchall()
    con.close()
    return rows

def prediksi_jurusan(Biologi, Fisika, Inggris):
    if Biologi >= Fisika and Biologi >= Inggris:
        return "Kedokteran"
    elif Fisika >= Biologi and Fisika >= Inggris:
        return "Teknik"
    else:
        return "Inggris"


create_table()

class Nilai(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Insert dan Read Data Nilai")
        self.geometry("600x420")

        frm = tk.Frame(self, bg="#ffffff", padx=12, pady=12)
        frm.pack(padx=16, pady=12, fill="x")

        tk.Label(frm, text="Nama:", bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.ent_name = tk.Entry(frm, width=30)
        self.ent_name.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Biologi :", bg="#ffffff").grid(row=1, column=0, sticky="w")
        self.ent_Biologi = tk.Entry(frm, width=30)
        self.ent_Biologi.grid(row=1, column=1, sticky="w", padx=6, pady=6) 

        tk.Label(frm, text="Fisika :", bg="#ffffff").grid(row=2, column=0, sticky="w")
        self.ent_Fisika = tk.Entry(frm, width=30)
        self.ent_Fisika.grid(row=2, column=1, sticky="w", padx=6, pady=6) 

        tk.Label(frm, text="Inggris :", bg="#ffffff").grid(row=3, column=0, sticky="w")
        self.ent_Inggris = tk.Entry(frm, width=30)
        self.ent_Inggris.grid(row=3, column=1, sticky="w", padx=6, pady=6) 


        btn_frame = tk.Frame(frm, bg="#ffffff")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(6,0))

        self.btn_add = tk.Button(btn_frame, text="Tambah", width=10, command=self.insertdata)
        self.btn_add.pack(side="left", padx=6)
        self.btn_refresh = tk.Button(btn_frame, text="Refresh", width=10, command=self.read_data)
        self.btn_refresh.pack(side="left", padx=6)


        cols = ("id", "name", "Biologi", "Fisika", "Inggris", "prediksi")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=50, anchor="center")
        self.tree.heading("name", text="Nama")
        self.tree.column("name", width=80)
        self.tree.heading("Biologi", text="Biologi")
        self.tree.column("Biologi", width=80, anchor="center")
        self.tree.heading("Fisika", text="Fisika")
        self.tree.column("Fisika", width=80, anchor="center")
        self.tree.heading("Inggris", text="Inggris")
        self.tree.column("Inggris", width=80, anchor="center")
        self.tree.heading("prediksi", text="predriksi")
        self.tree.column("prediksi", width=80, anchor="center")
        self.tree.pack(padx=16, pady=(0,12), fill="both", expand=True)


        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.read_data()


    def clear_inputs(self):
        self.ent_name.delete(0, tk.END)
        self.ent_Biologi.delete(0, tk.END)
        self.ent_Fisika.delete(0, tk.END)
        self.ent_Inggris.delete(0, tk.END)

    def validate_inputs(self):
        name = self.ent_name.get().strip()
        Biologi = self.ent_Biologi.get().strip()
        Fisika = self.ent_Fisika.get().strip()
        Inggris = self.ent_Inggris.get().strip()

        if not name or not Biologi or not Fisika or not Inggris:
            msg.showerror("Error", "Semua data harus diisi!")
            return None

        try:
            Biologi = int(Biologi)
            Fisika = int(Fisika)
            Inggris = int(Inggris)
        except ValueError:
            msg.showerror("Error", "Nilai harus berupa angka!")
            return None

        return name, Biologi, Fisika, Inggris


    def insertdata(self):
        val = self.validate_inputs()
        if not val:
            return
        name, Biologi, Fisika, Inggris = val
        try:
            new_id = insertnilai(name, Biologi, Fisika, Inggris)
            msg.showinfo("Sukses", f"Data disimpan (id={new_id}).")
            self.read_data()
            self.clear_inputs()
        except Exception as e:
            msg.showerror("DB Error", str(e))  

    
    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        _, name, Biologi, Fisika, Inggris = item["values"]

        self.ent_name.insert(0, name)
        self.ent_Biologi.insert(0, str(Biologi))
        self.ent_Fisika.insert(0, str(Fisika))
        self.ent_Inggris.insert(0, str(Inggris))

    def read_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows = readnilai()
            for r in rows:
                self.tree.insert("", tk.END, values=r)
        except Exception as e:
            msg.showerror("DB Error", str(e))
        
if __name__ == "__main__":
    app = Nilai()
    app.mainloop()

