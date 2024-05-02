import sqlite3

class TextSimilarityAnalyzer:
    def __init__(self, db_name='texts.db'):
        self.db_name = db_name
        self.create_table()

    def clean_text(self, text):
        cleaned_text = ''.join(char for char in text if char.isalnum() or char.isspace())
        return cleaned_text.lower()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS texts
                     (id INTEGER PRIMARY KEY, text TEXT)''')
        conn.commit()
        conn.close()

    def insert_text(self, text):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO texts (text) VALUES (?)", (text,))
        conn.commit()
        conn.close()

    def jaccard_similarity(self, text1, text2):
        words1 = set(self.clean_text(text1))
        words2 = set(self.clean_text(text2))
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        similarity_score = intersection / union if union != 0 else 0  # sıfıra bölme hatası önlemi
        return similarity_score

    def analyze_similarity(self, text1, text2):
        self.insert_text(text1)
        self.insert_text(text2)
        similarity_score = self.jaccard_similarity(text1, text2)
        return similarity_score

if __name__ == "__main__":
    analyzer = TextSimilarityAnalyzer()
    text1 = input("İlk metni gir: ")
    text2 = input("İkinci metni gir: ")
    similarity_score = analyzer.analyze_similarity(text1, text2)
    print("Benzerlik skoru:", similarity_score)
    with open("benzerlik.txt", "w") as file:
        file.write("Benzerlik skoru: {:.2f}".format(similarity_score))
