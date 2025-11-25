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
    cur.execute("INSERT INTO Nilai (name, Biologi, Fisika, Inggris, prediksi) VALUES (?, ?, ?, ?, ?)",
                (name, Biologi, Fisika, Inggris, hasil))
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

def updatenilai(id, name, Biologi, Fisika, Inggris):
    con = koneksi()
    cur = con.cursor()
    hasil = prediksi_jurusan(Biologi, Fisika, Inggris)
    cur.execute("""
        UPDATE Nilai
        SET name = ?, Biologi = ?, Fisika = ?, Inggris = ?, prediksi = ?
        WHERE id = ?
    """, (name, Biologi, Fisika, Inggris, hasil, id))
    con.commit()
    con.close()

def deletenilai(id):
    con = koneksi()
    cur = con.cursor()
    cur.execute("DELETE FROM Nilai WHERE id = ?", (id,))
    con.commit()
    con.close()

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

        frm = tk.Frame(self, bg="#d9d3db", padx=12, pady=12)
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

        # tombol Edit dan Delete
        self.btn_edit = tk.Button(btn_frame, text="Edit", width=10, command=self.open_edit_window)
        self.btn_edit.pack(side="left", padx=6)
        self.btn_delete = tk.Button(btn_frame, text="Hapus", width=10, command=self.delete_selected)
        self.btn_delete.pack(side="left", padx=6)


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
        self.tree.heading("prediksi", text="prediksi")
        self.tree.column("prediksi", width=100, anchor="center")
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
        _, name, Biologi, Fisika, Inggris, prediksi = item["values"]

        # isi ke input utama (untuk memudahkan jika mau update langsung)
        self.clear_inputs()
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

    # helper untuk ambil data yang dipilih di tree
    def get_selected(self):
        sel = self.tree.selection()
        if not sel:
            msg.showwarning("Peringatan", "Pilih data dulu!")
            return None
        return self.tree.item(sel[0])["values"]

    # popup edit window
    def open_edit_window(self):
        sel = self.get_selected()
        if not sel:
            return
        record_id, nama, bio, fis, ing, prediksi = sel

        win = tk.Toplevel(self)
        win.title(f"Edit Data ID {record_id}")
        win.geometry("420x240")
        win.grab_set()

        frm = tk.Frame(win, padx=12, pady=12)
        frm.pack(fill="both", expand=True)

        tk.Label(frm, text="Nama :").grid(row=0, column=0, sticky="w")
        e_name = tk.Entry(frm, width=36)
        e_name.grid(row=0, column=1, pady=6)
        e_name.insert(0, nama)

        tk.Label(frm, text="Biologi :").grid(row=1, column=0, sticky="w")
        e_bio = tk.Entry(frm, width=12)
        e_bio.grid(row=1, column=1, sticky="w", pady=6)
        e_bio.insert(0, bio)

        tk.Label(frm, text="Fisika :").grid(row=2, column=0, sticky="w")
        e_fis = tk.Entry(frm, width=12)
        e_fis.grid(row=2, column=1, sticky="w", pady=6)
        e_fis.insert(0, fis)

        tk.Label(frm, text="Inggris :").grid(row=3, column=0, sticky="w")
        e_ing = tk.Entry(frm, width=12)
        e_ing.grid(row=3, column=1, sticky="w", pady=6)
        e_ing.insert(0, ing)

        def save_changes():
            try:
                name = e_name.get().strip()
                b = int(e_bio.get().strip())
                f = int(e_fis.get().strip())
                i = int(e_ing.get().strip())

                if not name:
                    msg.showerror("Error", "Nama tidak boleh kosong")
                    return

                updatenilai(record_id, name, b, f, i)
                msg.showinfo("Sukses", "Data berhasil diperbarui")
                self.read_data()
                win.destroy()
            except ValueError:
                msg.showerror("Error", "Nilai harus angka!")
            except Exception as e:
                msg.showerror("DB Error", str(e))

        btn_frm = tk.Frame(frm)
        btn_frm.grid(row=4, column=0, columnspan=2, pady=(8,0))

        tk.Button(btn_frm, text="Simpan Perubahan", width=16, command=save_changes).pack(side="left", padx=6)
        tk.Button(btn_frm, text="Batal", width=10, command=win.destroy).pack(side="left", padx=6)

    # delete selected record
    def delete_selected(self):
        sel = self.get_selected()
        if not sel:
            return
        record_id = sel[0]
        if msg.askyesno("Konfirmasi", f"Yakin ingin menghapus data ID {record_id}?"):
            try:
                deletenilai(record_id)
                self.read_data()
                msg.showinfo("Sukses", "Data berhasil dihapus.")
            except Exception as e:
                msg.showerror("DB Error", str(e))


if __name__ == "__main__":
    app = Nilai()
    app.mainloop()
