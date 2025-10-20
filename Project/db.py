import sqlite3

class DB:
	def __init__(self):
		self.conn = sqlite3.connect('scores.db')
		self.cur = self.conn.cursor()
		self.cur.execute('''
			CREATE TABLE IF NOT EXISTS "Scores" (
				"id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
				"Name" TEXT NOT NULL,
				"Score" INTEGER NOT NULL
			)
		''')

    def insert_score(self, player_name: str, score: int) -> None:
        self.cur.execute('INSERT INTO "Scores" (Name, Score) VALUES (?, ?)', (player_name, score))
		self.conn.commit()

    def get_top_scores(self, limit: int):
        return self.cur.execute('SELECT Name, Score FROM Scores ORDER BY Score DESC LIMIT ?', (limit,)).fetchall()

    def is_high_score(self, score: int) -> bool:
        lowest_score = self.cur.execute('SELECT Score FROM Scores ORDER BY Score ASC LIMIT 5').fetchone()
        if lowest_score is None or score > lowest_score[0]:
			self.conn.commit()
			return True
        elif score == lowest_score[0]:
			return False
		return False

	def printDB(self):
		print(self.cur.execute("SELECT * FROM Scores").fetchall())
		self.conn.commit()