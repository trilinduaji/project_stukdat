class NodeSkor:
    def __init__(self, skor):
        self.skor = skor
        self.berikut = None

class DaftarSkor:
    def __init__(self):
        self.kepala = None

    def tambah(self, skor):
        node = NodeSkor(skor)
        if not self.kepala:
            self.kepala = node
            return
        cur = self.kepala
        while cur.berikut:
            cur = cur.berikut
        cur.berikut = node
    def hitung_rata(self):
        cur = self.kepala
        total = 0
        n = 0
        while cur:
            total += cur.skor
            n += 1
            cur = cur.berikut
        return (total / n) if n else 0.0

        def sebagai_list(self):
            out = []
            cur = self.kepala
            while cur:
                out.append(cur.skor)
                cur = cur.berikut
            return out
    
        def isi_dari_list(self, lst):
            self.kepala = None
            for s in lst:
                try:
                    self.tambah(int(s))
                except:
                    pass
    
