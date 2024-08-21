import mysql.connector
from sqlalchemy import create_engine
import pandas as pd



class Database:
    def __init__(self, host='localhost', user='root', password='', database='scraping_web'):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()
        self.engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                text TEXT,
                author VARCHAR(255),
                about TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INT AUTO_INCREMENT PRIMARY KEY,
                quote_id INT,
                tag VARCHAR(255),
                FOREIGN KEY (quote_id) REFERENCES quotes (id)
            )
        ''')
        self.conn.commit()

    def insert_quotes(self, df):
        # Insertar citas
        df[['text', 'author', 'about']].to_sql('quotes', con=self.engine, if_exists='append', index=False)
        
        # Obtener los IDs de las citas insertadas
        self.cursor.execute("SELECT id FROM quotes ORDER BY id DESC LIMIT %s", (len(df),))
        quote_ids = [row[0] for row in self.cursor.fetchall()][::-1]  # Reverse to match DataFrame order
        
        # Insertar tags
        tags_data = []
        for quote_id, tags in zip(quote_ids, df['tags']):
            for tag in tags:
                tags_data.append({'quote_id': quote_id, 'tag': tag})
        
        pd.DataFrame(tags_data).to_sql('tags', con=self.engine, if_exists='append', index=False)

    def close(self):
        self.conn.close()

    def get_all_quotes(self):
        query = '''
        SELECT q.id, q.text, q.author, q.about, GROUP_CONCAT(t.tag) as tags
        FROM quotes q
        LEFT JOIN tags t ON q.id = t.quote_id
        GROUP BY q.id
        '''
        return pd.read_sql(query, self.engine)

    def get_quote_by_id(self, quote_id):
        query = '''
        SELECT q.id, q.text, q.author, q.about, GROUP_CONCAT(t.tag) as tags
        FROM quotes q
        LEFT JOIN tags t ON q.id = t.quote_id
        WHERE q.id = %s
        GROUP BY q.id
        '''
        return pd.read_sql(query, self.engine, params=[quote_id])

    def get_quotes_by_author(self, author):
        query = '''
        SELECT q.id, q.text, q.author, q.about, GROUP_CONCAT(t.tag) as tags
        FROM quotes q
        LEFT JOIN tags t ON q.id = t.quote_id
        WHERE q.author = %s
        GROUP BY q.id
        '''
        return pd.read_sql(query, self.engine, params=[author])

    def get_quotes_by_tag(self, tag):
        query = '''
        SELECT q.id, q.text, q.author, q.about, GROUP_CONCAT(t.tag) as tags
        FROM quotes q
        JOIN tags t ON q.id = t.quote_id
        WHERE t.tag = %s
        GROUP BY q.id
        '''
        return pd.read_sql(query, self.engine, params=[tag])