def get_song_details(self, song_id):
    song = self.songs.get(song_id)
    if song:
        avg_score = song.scores.calculate_average()
        return (f"ID: {song.id}\nJudul Lagu: {song.title}\nArtis: {song.artist}\n"
                f"Genre: {', '.join(song.genres)}\nAvg Popularity Score: {avg_score:.1f}")
    return "Lagu tidak ditemukan."

def recommend_by_genre(self, genre):
    song_ids = self.graph.get_songs_by_genre(genre)
    recommendations = [self.songs[sid] for sid in song_ids if sid in self.songs]
    recommendations.sort(key=lambda s: s.scores.calculate_average(), reverse=True)
    return [f"{s.title} oleh {s.artist} (Score: {s.scores.calculate_average():.1f})" 
            for s in recommendations]
