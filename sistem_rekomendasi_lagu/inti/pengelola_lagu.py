def update_song_details(self, song_id, new_title, new_artist):
    song = self.songs.get(song_id)
    if song:
        song.title = new_title
        song.artist = new_artist
        return True
    return False

def delete_song(self, song_id):
    if song_id in self.songs:
        song = self.songs.pop(song_id)
        self.graph.remove_song_from_genres(song_id, song.genres)
        return True
    return False

#yang atas salah code kak maap
import os
from .lagu import Lagu
from .genre import GenreGraf
from .lagu_urut import LaguBST
from .antri_playlist import AntriPlaylist
from utilitas.pemuat_dat import Loader
from utilitas.genre_list import GENRE_LIST

class PengelolaLagu:
    def __init__(self):
        self.songs = {}
        self.graf = GenreGraf()
        self.bst = LaguBST()
        self.playlist = AntriPlaylist()
        self.next_id = 1001
        self.path_db = os.path.join("data", "database.json")

    def muat_dari_db(self):
        data = Loader.muat(self.path_db)
        self.next_id = data.get("next_id", self.next_id)
        for s in data.get("lagu", []):
            l = Lagu(s["id"], s["judul"], s["penyanyi"], s.get("genre", []))
            l.skor.isi_dari_list(s.get("skor", []))
            self.songs[l.id_lagu] = l
            self.graf.tambah_lagu_ke_genres(l.id_lagu, l.genres)
            self.bst.sisip(l)

    def simpan_ke_db(self):
        data = {"next_id": self.next_id, "lagu": []}
        for l in sorted(self.songs.values(), key=lambda x: x.id_lagu):
            data["lagu"].append(l.to_dict())
        Loader.simpan(self.path_db, data)

    def tambah_lagu(self, judul, penyanyi, genres, initial_skor=None):
        if isinstance(genres, str):
            genres_list = [genres]
        else:
            genres_list = list(genres or [])
        sid = self.next_id
        lagu = Lagu(sid, judul, penyanyi, genres_list)
        if initial_skor is not None:
            if isinstance(initial_skor, (list, tuple)):
                for v in initial_skor:
                    try:
                        lagu.skor.tambah(int(v))
                    except:
                        pass
            else:
                try:
                    lagu.skor.tambah(int(initial_skor))
                except:
                    pass
        self.songs[sid] = lagu
        self.graf.tambah_lagu_ke_genres(sid, lagu.genres)
        self.bst.sisip(lagu)
        self.next_id += 1
        return lagu

    def hapus_lagu(self, identifier):
        if isinstance(identifier, int):
            sid = identifier
        else:
            sid = None
            for k, v in self.songs.items():
                if v.judul.lower() == str(identifier).strip().lower():
                    sid = k
                    break
        if sid is None or sid not in self.songs:
            return False
        lagu = self.songs.pop(sid)
        self.graf.hapus_lagu_dari_genres(sid, lagu.genres)
        return True

    def update_lagu(self, song_id, judul_baru=None, penyanyi_baru=None, genres_baru=None):
        """
        Perbarui metadata lagu. genres_baru dapat berupa string (single genre)
        atau list. Kembalikan True jika berhasil.
        """
        l = self.songs.get(song_id)
        if not l:
            return False  
        if genres_baru is not None:
            if isinstance(genres_baru, str):
                new_genres = [genres_baru]
            else:
                new_genres = list(genres_baru)
            self.graf.hapus_lagu_dari_genres(song_id, l.genres)
            l.genres = [g.strip().capitalize() for g in new_genres]
            self.graf.tambah_lagu_ke_genres(song_id, l.genres)

        if judul_baru:
            l.judul = judul_baru
            self.bst.sisip(l)
        if penyanyi_baru:
            l.penyanyi = penyanyi_baru
        return True

    def tambah_skor(self, song_id, nilai):
        l = self.songs.get(song_id)
        if not l:
            return False
        try:
            n = int(nilai)
        except:
            return False
        if 1 <= n <= 5:
            l.skor.tambah(n)
            return True
        return False

    def rekomendasi_by_genre(self, genre):
        ids = self.graf.ambil_lagu_berdasarkan_genre(genre)
        rek = [self.songs[i] for i in ids if i in self.songs]
        rek.sort(key=lambda x: x.rata_skor(), reverse=True)
        return rek

    def tambah_ke_playlist(self, song_id):
        if song_id in self.songs:
            self.playlist.tambah(song_id)
            return True
        return False

    def mainkan_selanjutnya(self):
        sid = self.playlist.ambil()
        return sid

    def lihat_playlist(self):
        return self.playlist.lihat()

    def semua_lagu(self):
        return [self.songs[k] for k in sorted(self.songs.keys())]
