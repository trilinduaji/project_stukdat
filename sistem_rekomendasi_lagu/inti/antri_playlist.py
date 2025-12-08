from collections import deque

class AntriPlaylist:
    def __init__(self):
        self.q = deque()

    def tambah(self, song_id):
        self.q.append(song_id)

    def ambil(self):
        if self.q:
            return self.q.popleft()
        return None

    def lihat(self):
        return list(self.q)

    def kosong(self):
        return len(self.q) == 0
