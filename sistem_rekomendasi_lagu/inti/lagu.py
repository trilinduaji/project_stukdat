from .skor import DaftarSkor

class Lagu:
    def __init__(self, id_lagu, judul, penyanyi, genres=None):
        self.id_lagu = id_lagu
        self.judul = judul
        self.penyanyi = penyanyi
        self.genres = [g.strip().capitalize() for g in (genres or [])]
        self.skor = DaftarSkor()

    def rata_skor(self):
        return self.skor.hitung_rata()

    def ringkasan(self):
        return f"[{self.id_lagu}] {self.judul} - {self.penyanyi} (Avg: {self.rata_skor():.1f})"

    def to_dict(self):
        return {
            "id": self.id_lagu,
            "judul": self.judul,
            "penyanyi": self.penyanyi,
            "genre": self.genres,
            "skor": self.skor.sebagai_list()
        }

    def __str__(self):
        return self.ringkasan()
