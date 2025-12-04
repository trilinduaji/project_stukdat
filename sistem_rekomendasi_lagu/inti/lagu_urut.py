class NodeLagu:
    def __init__(self, lagu):
        self.lagu = lagu
        self.kiri = None
        self.kanan = None

class LaguBST:
    def __init__(self):
        self.akar = None

    def sisip(self, lagu):
        self.akar = self._sisip(self.akar, lagu)

    def _sisip(self, node, lagu):
        if node is None:
            return NodeLagu(lagu)
        key = lagu.judul.lower()
        if key < node.lagu.judul.lower():
            node.kiri = self._sisip(node.kiri, lagu)
        else:
            node.kanan = self._sisip(node.kanan, lagu)
        return node

    def inorder(self):
        out = []
        self._inorder(self.akar, out)
        return out

    def _inorder(self, node, out):
        if not node:
            return
        self._inorder(node.kiri, out)
        out.append(node.lagu)
        self._inorder(node.kanan, out)

    def cari_judul(self, judul):
        t = judul.lower()
        cur = self.akar
        while cur:
            if t == cur.lagu.judul.lower():
                return cur.lagu
            elif t < cur.lagu.judul.lower():
                cur = cur.kiri
            else:
                cur = cur.kanan
        return None
