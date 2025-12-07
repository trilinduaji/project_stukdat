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
