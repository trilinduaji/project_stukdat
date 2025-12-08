import os
import tkinter as tk
import tkinter.messagebox as msg

# Try import customtkinter
try:
    import customtkinter as ctk
    CTK = True
except:
    CTK = False
    import tkinter.ttk as ttk

    class FakeCTK:
        CTk = tk.Tk
        CTkFrame = tk.Frame
        CTkButton = tk.Button
        CTkLabel = tk.Label
        CTkEntry = tk.Entry
        CTkComboBox = ttk.Combobox
        CTkToplevel = tk.Toplevel
        CTkTextbox = tk.Text
    ctk = FakeCTK()

from inti.pengelola_lagu import PengelolaLagu
from utilitas.genre_list import GENRE_LIST


class AplikasiRekomendasiLagu(ctk.CTk if CTK else tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Rekomendasi Lagu")
        self.geometry("1000x640")

        if CTK:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("green")

        self.mgr = PengelolaLagu()
        self.mgr.muat_dari_db()

        parent = ctk.CTkFrame(self) if CTK else tk.Frame(self)
        parent.pack(fill="both", expand=True, padx=12, pady=12)

        left = ctk.CTkFrame(parent, width=480) if CTK else tk.Frame(parent, width=480)
        left.pack(side="left", fill="both", expand=True, padx=6)

        right = ctk.CTkFrame(parent, width=480) if CTK else tk.Frame(parent, width=480)
        right.pack(side="right", fill="both", expand=True, padx=6)

        ctk.CTkLabel(left, text="Daftar Lagu", font=("Arial", 16, "bold")).pack(anchor="w")
        self.txt_daftar = ctk.CTkTextbox(left, width=460, height=540)
        self.txt_daftar.pack(pady=6)

        ctk.CTkLabel(right, text="Rekomendasi & Kontrol", font=("Arial", 16, "bold")).pack(anchor="w")

        self.cb_genre = ctk.CTkComboBox(right, values=GENRE_LIST)
        self.cb_genre.pack(pady=4)

        self.txt_rekom = ctk.CTkTextbox(right, width=440, height=140)
        self.txt_rekom.pack(pady=6)

        frm_btn = ctk.CTkFrame(right)
        frm_btn.pack(fill="x", pady=6)

        ctk.CTkButton(frm_btn, text="Tampilkan Rekomendasi", command=self.tampilkan_rekom).pack(fill="x", pady=3)
        ctk.CTkButton(frm_btn, text="Tambah Lagu", command=self.popup_tambah).pack(fill="x", pady=3)
        ctk.CTkButton(frm_btn, text="Hapus Lagu", command=self.popup_hapus).pack(fill="x", pady=3)
        ctk.CTkButton(frm_btn, text="Update Lagu", command=self.popup_update).pack(fill="x", pady=3)
        ctk.CTkButton(frm_btn, text="Tambah ke Playlist", command=self.popup_tambah_playlist).pack(fill="x", pady=3)
        ctk.CTkButton(frm_btn, text="Lihat Playlist", command=self.show_playlist).pack(fill="x", pady=3)
        ctk.CTkButton(frm_btn, text="Simpan ke DB", command=self.simpan).pack(fill="x", pady=3)

        self.refresh_daftar()

    # ===================== LOGIKA =====================

    def refresh_daftar(self):
        self.txt_daftar.delete("1.0", "end")
        semua = self.mgr.semua_lagu()
        if not semua:
            self.txt_daftar.insert("end", "Belum ada lagu.")
            return
        for l in semua:
            self.txt_daftar.insert(
                "end",
                f"{l.ringkasan()}\nGenre: {', '.join(l.genres)}\nSkor: {l.skor.sebagai_list()}\n{'-'*40}\n"
            )

    def tampilkan_rekom(self):
        genre = self.cb_genre.get()
        self.txt_rekom.delete("1.0", "end")
        hasil = self.mgr.rekomendasi_by_genre(genre)
        if not hasil:
            self.txt_rekom.insert("end", "Tidak ada rekomendasi.")
            return
        for l in hasil:
            self.txt_rekom.insert("end", f"{l.ringkasan()} | Avg: {l.rata_skor():.1f}\n")

    # ===================== POPUP TAMBAH =====================

    def popup_tambah(self):
        win = ctk.CTkToplevel(self)
        win.title("Tambah Lagu")
        win.geometry("420x320")
        win.grab_set()

        judul = ctk.CTkEntry(win, placeholder_text="Judul"); judul.pack(pady=8)
        penyanyi = ctk.CTkEntry(win, placeholder_text="Penyanyi"); penyanyi.pack(pady=8)
        genre = ctk.CTkComboBox(win, values=GENRE_LIST); genre.pack(pady=8)
        skor = ctk.CTkEntry(win, placeholder_text="Skor awal (1-5)"); skor.pack(pady=8)

        def simpan():
            try:
                init = int(skor.get())
            except:
                init = None
            self.mgr.tambah_lagu(judul.get(), penyanyi.get(), genre.get(), init)
            self.refresh_daftar()
            win.destroy()

        ctk.CTkButton(win, text="Simpan", command=simpan).pack(pady=10)

    # ===================== POPUP HAPUS =====================

    def popup_hapus(self):
        win = ctk.CTkToplevel(self)
        win.title("Hapus Lagu")
        win.geometry("320x180")
        win.grab_set()

        ent = ctk.CTkEntry(win, placeholder_text="Masukkan ID Lagu")
        ent.pack(pady=20)

        def hapus():
            try:
                sid = int(ent.get())
            except:
                msg.showerror("Error", "ID harus angka")
                return

            if self.mgr.hapus_lagu(sid):
                msg.showinfo("Sukses", "Lagu terhapus")
                self.refresh_daftar()
                win.destroy()
            else:
                msg.showerror("Gagal", "ID tidak ditemukan")

        ctk.CTkButton(win, text="Hapus", command=hapus).pack(pady=10)

    # ===================== POPUP UPDATE  =====================

    def popup_update(self):
        win = ctk.CTkToplevel(self)
        win.title("Update Lagu")
        win.geometry("420x320")
        win.grab_set()

        ent_id = ctk.CTkEntry(win, placeholder_text="ID Lagu")
        ent_id.pack(pady=6)

        ent_judul = ctk.CTkEntry(win, placeholder_text="Judul Baru (opsional)")
        ent_judul.pack(pady=6)

        ent_penyanyi = ctk.CTkEntry(win, placeholder_text="Penyanyi Baru (opsional)")
        ent_penyanyi.pack(pady=6)

        ent_genre = ctk.CTkEntry(win, placeholder_text="Genre Baru (pisah koma)")
        ent_genre.pack(pady=6)

        def submit():
            try:
                sid = int(ent_id.get())
            except:
                msg.showerror("Error", "ID harus angka")
                return

            judul = ent_judul.get().strip()
            penyanyi = ent_penyanyi.get().strip()
            genre_raw = ent_genre.get().strip()

            genres = None
            if genre_raw:
                genres = [g.strip() for g in genre_raw.split(",")]

            if not (judul or penyanyi or genres):
                msg.showwarning("Warning", "Minimal 1 field diisi")
                return

            if self.mgr.update_lagu(sid, judul or None, penyanyi or None, genres):
                msg.showinfo("Sukses", "Lagu berhasil diupdate")
                self.refresh_daftar()
                win.destroy()
            else:
                msg.showerror("Gagal", "ID lagu tidak ditemukan")

        ctk.CTkButton(win, text="Update", command=submit).pack(pady=14)

    # ===================== PLAYLIST =====================

    def popup_tambah_playlist(self):
        win = ctk.CTkToplevel(self)
        win.title("Tambah ke Playlist")
        win.geometry("300x180")
        win.grab_set()

        ent = ctk.CTkEntry(win, placeholder_text="Masukkan ID Lagu")
        ent.pack(pady=20)

        def tambah():
            try:
                sid = int(ent.get())
            except:
                msg.showerror("Error", "ID harus angka")
                return

            if self.mgr.tambah_ke_playlist(sid):
                msg.showinfo("Sukses", "Ditambahkan ke playlist")
                win.destroy()
            else:
                msg.showerror("Gagal", "ID tidak ditemukan")

        ctk.CTkButton(win, text="Tambah", command=tambah).pack(pady=10)

    def show_playlist(self):
        pl = self.mgr.lihat_playlist()
        if not pl:
            msg.showinfo("Playlist", "Playlist kosong")
            return

        teks = ""
        for sid in pl:
            l = self.mgr.songs.get(sid)
            if l:
                teks += f"{l.ringkasan()}\n"

        msg.showinfo("Playlist", teks)

    def simpan(self):
        self.mgr.simpan_ke_db()
        msg.showinfo("Simpan", "Data berhasil disimpan")


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    app = AplikasiRekomendasiLagu()
    app.mainloop()
