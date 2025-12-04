class GenreGraf:
    def __init__(self):
        self.map = {}

    def tambah_lagu_ke_genres(self, song_id, genres):
        for g in genres:
            key = g.strip().capitalize()
            if key not in self.map:
                self.map[key] = []
            if song_id not in self.map[key]:
                self.map[key].append(song_id)

    def ambil_lagu_berdasarkan_genre(self, genre):
        key = genre.strip().capitalize()
        return list(self.map.get(key, []))

    def hapus_lagu_dari_genres(self, song_id, genres):
        for g in genres:
            key = g.strip().capitalize()
            if key in self.map and song_id in self.map[key]:
                self.map[key].remove(song_id)

    def semua_genres(self):
        return sorted(list(self.map.keys()))

