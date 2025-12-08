import os
import tkinter as tk
import tkinter.messagebox as msg

try:
    import customtkinter as ctk
    CTK = True
except Exception:
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
        self.title("Sistem Rekomendasi Lagu - UAP")
        self.geometry("1000x640")

        if CTK:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("green")

        self.mgr = PengelolaLagu()
        self.mgr.muat_dari_db()

        # layout: left = daftar, right = rekomendasi & kontrol
        parent = ctk.CTkFrame(self) if CTK else tk.Frame(self)
        parent.pack(fill="both", expand=True, padx=12, pady=12)

        left = ctk.CTkFrame(parent, width=480) if CTK else tk.Frame(parent, width=480)
        left.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        right = ctk.CTkFrame(parent, width=480) if CTK else tk.Frame(parent, width=480)
        right.pack(side="right", fill="both", expand=True, padx=6, pady=6)

        # LEFT: Daftar lagu (otomatis tampil)
        lbl_left = ctk.CTkLabel(left, text="Daftar Lagu", font=("Arial", 16, "bold")) if CTK else tk.Label(left, text="Daftar Lagu", font=("Arial", 16, "bold"))
        lbl_left.pack(anchor="w", pady=6, padx=6)

        self.txt_daftar = ctk.CTkTextbox(left, width=460, height=520) if CTK else tk.Text(left, width=55, height=32)
        self.txt_daftar.pack(padx=6, pady=6)

        # RIGHT: kontrol rekomendasi, update, tambah, hapus
        lbl_right = ctk.CTkLabel(right, text="Rekomendasi & Kontrol", font=("Arial", 16, "bold")) if CTK else tk.Label(right, text="Rekomendasi & Kontrol", font=("Arial", 16, "bold"))
        lbl_right.pack(anchor="w", pady=6, padx=6)

        # genre combobox
        if CTK:
            ctk.CTkLabel(right, text="Pilih Genre:").pack(anchor="w")
            self.cb_genre = ctk.CTkComboBox(right, values=GENRE_LIST)
            self.cb_genre.pack(padx=6, pady=4)
        else:
            tk.Label(right, text="Pilih Genre:").pack(anchor="w")
            self.cb_genre = tk.ttk.Combobox(right, values=GENRE_LIST)
            self.cb_genre.pack(padx=6, pady=4)

        # hasil rekomendasi area
        self.txt_rekom = ctk.CTkTextbox(right, width=440, height=160) if CTK else tk.Text(right, width=50, height=10)
        self.txt_rekom.pack(padx=6, pady=6)

        # kontrol buttons
        frm_btn = ctk.CTkFrame(right) if CTK else tk.Frame(right)
        frm_btn.pack(fill="x", pady=6, padx=6)

        btn_rekom = ctk.CTkButton(frm_btn, text="Tampilkan Rekomendasi", command=self.tampilkan_rekom) if CTK else tk.Button(frm_btn, text="Tampilkan Rekomendasi", command=self.tampilkan_rekom)
        btn_rekom.pack(fill="x", pady=4)

        btn_tambah = ctk.CTkButton(frm_btn, text="Tambah Lagu (Popup)", command=self.popup_tambah) if CTK else tk.Button(frm_btn, text="Tambah Lagu (Popup)", command=self.popup_tambah)
        btn_tambah.pack(fill="x", pady=4)

        btn_hapus = ctk.CTkButton(frm_btn, text="Hapus Lagu (Popup)", command=self.popup_hapus) if CTK else tk.Button(frm_btn, text="Hapus Lagu (Popup)", command=self.popup_hapus)
        btn_hapus.pack(fill="x", pady=4)

        btn_playlist_add = ctk.CTkButton(
            frm_btn,
            text="Tambah ke Playlist (Popup)",
            command=self.popup_tambah_playlist
        ) if CTK else tk.Button(
            frm_btn,
            text="Tambah ke Playlist (Popup)",
            command=self.popup_tambah_playlist
        )
        btn_playlist_add.pack(fill="x", pady=4)



        # Update area (edit lagu) - langsung di panel kanan
        frm_update = ctk.CTkFrame(right) if CTK else tk.Frame(right)
        frm_update.pack(fill="x", pady=6, padx=6)

        if CTK:
            ctk.CTkLabel(frm_update, text="Update Lagu (masukkan ID lalu edit):").pack(anchor="w")
            self.ent_update_id = ctk.CTkEntry(frm_update, placeholder_text="ID lagu")
            self.ent_update_id.pack(fill="x", pady=4)
            self.ent_update_judul = ctk.CTkEntry(frm_update, placeholder_text="Judul baru (kosong = tidak diubah)")
            self.ent_update_judul.pack(fill="x", pady=4)
            self.ent_update_penyanyi = ctk.CTkEntry(frm_update, placeholder_text="Penyanyi baru (kosong = tidak diubah)")
            self.ent_update_penyanyi.pack(fill="x", pady=4)
            self.ent_update_genre = ctk.CTkEntry(frm_update, placeholder_text="Genre baru (pisah koma) (kosong = tidak diubah)")
            self.ent_update_genre.pack(fill="x", pady=4)
            ctk.CTkButton(frm_update, text="Update", command=self.update_lagu_gui).pack(pady=6)
        else:
            tk.Label(frm_update, text="Update Lagu (masukkan ID lalu edit):").pack(anchor="w")
            self.ent_update_id = tk.Entry(frm_update); self.ent_update_id.pack(fill="x", pady=4)
            self.ent_update_judul = tk.Entry(frm_update); self.ent_update_judul.pack(fill="x", pady=4)
            self.ent_update_penyanyi = tk.Entry(frm_update); self.ent_update_penyanyi.pack(fill="x", pady=4)
            self.ent_update_genre = tk.Entry(frm_update); self.ent_update_genre.pack(fill="x", pady=4)
            tk.Button(frm_update, text="Update", command=self.update_lagu_gui).pack(pady=6)

        # skor quick entry
        frm_skor = ctk.CTkFrame(right) if CTK else tk.Frame(right)
        frm_skor.pack(fill="x", pady=6, padx=6)
        if CTK:
            ctk.CTkLabel(frm_skor, text="Beri Skor (ID & Nilai 1-5):").pack(anchor="w")
            self.ent_skor_id = ctk.CTkEntry(frm_skor, placeholder_text="ID lagu"); self.ent_skor_id.pack(side="left", padx=6)
            self.ent_skor_nilai = ctk.CTkEntry(frm_skor, placeholder_text="1-5", width=60); self.ent_skor_nilai.pack(side="left", padx=6)
            ctk.CTkButton(frm_skor, text="Submit Skor", command=self.submit_skor).pack(side="left", padx=6)
        else:
            tk.Label(frm_skor, text="Beri Skor (ID & Nilai 1-5):").pack(anchor="w")
            self.ent_skor_id = tk.Entry(frm_skor, width=8); self.ent_skor_id.pack(side="left", padx=6)
            self.ent_skor_nilai = tk.Entry(frm_skor, width=5); self.ent_skor_nilai.pack(side="left", padx=6)
            tk.Button(frm_skor, text="Submit Skor", command=self.submit_skor).pack(side="left", padx=6)

        btn_simpan = ctk.CTkButton(frm_btn, text="Simpan ke DB", command=self.simpan) if CTK else tk.Button(frm_btn, text="Simpan ke DB", command=self.simpan)
        btn_simpan.pack(fill="x", pady=4)
        btn_playlist = ctk.CTkButton(frm_btn, text="Lihat Playlist", command=self.show_playlist) if CTK else tk.Button(frm_btn, text="Lihat Playlist", command=self.show_playlist)
        btn_playlist.pack(fill="x", pady=4)

        # refresh daftar segera
        self.refresh_daftar()

    def refresh_daftar(self):
        self.txt_daftar.delete("1.0", "end")
        semua = self.mgr.semua_lagu()
        if not semua:
            self.txt_daftar.insert("end", "Belum ada lagu.")
            return
        for l in semua:
            self.txt_daftar.insert("end", f"{l.ringkasan()}\nGenre: {', '.join(l.genres)}\nSkorList: {l.skor.sebagai_list()}\n{'-'*40}\n")

    def tampilkan_rekom(self):
        genre = self.cb_genre.get()
        self.txt_rekom.delete("1.0", "end")
        if not genre:
            self.txt_rekom.insert("end", "Pilih genre dulu.")
            return
        hasil = self.mgr.rekomendasi_by_genre(genre)
        if not hasil:
            self.txt_rekom.insert("end", f"Tidak ada lagu untuk genre {genre}.")
            return
        for l in hasil:
            self.txt_rekom.insert("end", f"{l.ringkasan()}\nGenre: {', '.join(l.genres)}\nAvg: {l.rata_skor():.1f}\n{'-'*30}\n")

    def popup_tambah(self):
        win = ctk.CTkToplevel(self) if CTK else tk.Toplevel(self)
        win.title("Tambah Lagu")
        win.geometry("420x300")
        try:
            win.focus(); win.grab_set(); win.lift()
        except: pass

        if CTK:
            judul = ctk.CTkEntry(win, placeholder_text="Judul"); judul.pack(pady=8)
            penyanyi = ctk.CTkEntry(win, placeholder_text="Penyanyi"); penyanyi.pack(pady=8)
            combo = ctk.CTkComboBox(win, values=GENRE_LIST); combo.pack(pady=8)
            skor = ctk.CTkEntry(win, placeholder_text="Skor awal (1-5)"); skor.pack(pady=8)
            def simpan():
                g = combo.get()
                init = None
                try:
                    init = int(skor.get())
                except: init = None
                self.mgr.tambah_lagu(judul.get(), penyanyi.get(), g, init)
                self.refresh_daftar(); win.destroy()
            ctk.CTkButton(win, text="Simpan", command=simpan).pack(pady=8)
        else:
            tk.Label(win, text="Judul").pack(); judul = tk.Entry(win); judul.pack()
            tk.Label(win, text="Penyanyi").pack(); penyanyi = tk.Entry(win); penyanyi.pack()
            combo = tk.ttk.Combobox(win, values=GENRE_LIST); combo.pack()
            tk.Label(win, text="Skor awal (1-5)").pack(); skor = tk.Entry(win); skor.pack()
            def simpan2():
                try:
                    init = int(skor.get())
                except:
                    init = None
                self.mgr.tambah_lagu(judul.get(), penyanyi.get(), combo.get(), init)
                self.refresh_daftar(); win.destroy()
            tk.Button(win, text="Simpan", command=simpan2).pack(pady=8)

    def popup_hapus(self):
        win = ctk.CTkToplevel(self) if CTK else tk.Toplevel(self)
        win.title("Hapus Lagu")
        win.geometry("380x180")
        try:
            win.focus(); win.grab_set(); win.lift()
        except: pass

        if CTK:
            ent = ctk.CTkEntry(win, placeholder_text="Masukkan ID atau Judul"); ent.pack(pady=12)
            def hapus():
                key = ent.get().strip()
                try:
                    k = int(key)
                except:
                    k = key
                ok = self.mgr.hapus_lagu(k)
                if ok:
                    msg.showinfo("Sukses", "Lagu terhapus.")
                    self.refresh_daftar(); win.destroy()
                else:
                    msg.showerror("Gagal", "Lagu tidak ditemukan.")
            ctk.CTkButton(win, text="Hapus", command=hapus).pack(pady=6)
        else:
            ent = tk.Entry(win); ent.pack(pady=12)
            def hapus2():
                key = ent.get().strip()
                try:
                    k = int(key)
                except:
                    k = key
                ok = self.mgr.hapus_lagu(k)
                if ok:
                    msg.showinfo("Sukses", "Lagu terhapus.")
                    self.refresh_daftar(); win.destroy()
                else:
                    msg.showerror("Gagal", "Lagu tidak ditemukan.")
            tk.Button(win, text="Hapus", command=hapus2).pack(pady=6)
    
    def submit_skor(self):
        try:
            sid = int(self.ent_skor_id.get())
            nilai = int(self.ent_skor_nilai.get())
        except:
            msg.showerror("Error", "ID dan Skor harus angka.")
            return
        ok = self.mgr.tambah_skor(sid, nilai)
        if ok:
            msg.showinfo("Sukses", "Skor ditambahkan.")
            self.refresh_daftar()
        else:
            msg.showerror("Gagal", "Gagal menambahkan skor.")

    def update_lagu_gui(self):
        # ambil input
        try:
            sid = int(self.ent_update_id.get())
        except:
            msg.showerror("Error", "ID lagu harus angka.")
            return
        judul_baru = self.ent_update_judul.get().strip()
        penyanyi_baru = self.ent_update_penyanyi.get().strip()
        genre_baru_raw = self.ent_update_genre.get().strip()
        genres_list = None
        if genre_baru_raw:
            genres_list = [g.strip() for g in genre_baru_raw.split(",") if g.strip()]
        # jika semua kosong, beri peringatan
        if not (judul_baru or penyanyi_baru or genres_list):
            msg.showwarning("Input Kosong", "Minimal satu field harus diisi untuk update.")
            return
        ok = self.mgr.update_lagu(sid, judul_baru or None, penyanyi_baru or None, genres_list)
        if ok:
            msg.showinfo("Sukses", "Lagu berhasil diupdate.")
            self.refresh_daftar()
            # kosongkan field
            self.ent_update_id.delete(0, "end")
            self.ent_update_judul.delete(0, "end")
            self.ent_update_penyanyi.delete(0, "end")
            self.ent_update_genre.delete(0, "end")
        else:
            msg.showerror("Gagal", "ID lagu tidak ditemukan.")

    def show_playlist(self):
        pl = self.mgr.lihat_playlist()
        if not pl:
            msg.showinfo("Playlist", "Playlist kosong.")
            return
        teks = ""
        for sid in pl:
            l = self.mgr.songs.get(sid)
            if l:
                teks += f"{l.ringkasan()}\n"
        msg.showinfo("Playlist", teks)

    def popup_tambah_playlist(self):
        win = ctk.CTkToplevel(self)
        win.title("Tambah ke Playlist")
        win.geometry("320x180")
        win.resizable(False, False)
        win.grab_set()

        lbl = ctk.CTkLabel(win, text="Masukkan ID Lagu:")
        lbl.pack(pady=(20, 8))

        ent_id = ctk.CTkEntry(win, placeholder_text="ID lagu")
        ent_id.pack(padx=20, pady=4, fill="x")

        def submit():
            sid_str = ent_id.get().strip()
            if not sid_str:
                msg.showerror("Error", "ID tidak boleh kosong.", parent=win)
                return

            try:
                sid = int(sid_str)
            except ValueError:
                msg.showerror("Error", "ID harus berupa angka.", parent=win)
                return

            if self.mgr.tambah_ke_playlist(sid):
                msg.showinfo("Playlist",
                            f"Lagu dengan ID {sid} berhasil ditambahkan ke playlist.",
                            parent=win)
                win.destroy()
            else:
                msg.showerror("Error", "ID lagu tidak ditemukan.", parent=win)

        btn_ok = ctk.CTkButton(win, text="Simpan", command=submit)
        btn_ok.pack(pady=16)


    def simpan(self):
        self.mgr.simpan_ke_db()
        msg.showinfo("Simpan", "Data tersimpan ke database.json")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    app = AplikasiRekomendasiLagu()
    app.mainloop()
