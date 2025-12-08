# inti/tumpukan_lagu.py
class TumpukanLagu:
    def __init__(self):
        self.stack = []

    def dorong(self, aksi):
        self.stack.append(aksi)

    def ambil(self):
        if self.stack:
            return self.stack.pop()
        return None

    def lihat_terakhir(self):
        return self.stack[-1] if self.stack else None

    def kosong(self):
        return len(self.stack) == 0
