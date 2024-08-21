import sys
import os
from flask import Flask, render_template, request, jsonify
import logging
import pandas as pd

# Añade el directorio 'src' al path de Python para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database

app = Flask(__name__)

# Configuración de logging
logging.basicConfig(filename='logs/frontend.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

@app.route('/')
def index():
    try:
        logging.info("Iniciando el proceso de recuperación de datos")
        db = Database()
        quotes = db.get_all_quotes()
        db.close()
        logging.info(f"Se recuperaron {len(quotes)} frases")
        return render_template('index.html', quotes=quotes.to_dict('records'))
    except Exception as e:
        logging.error(f"Error al recuperar datos: {str(e)}")
        return "Error al cargar los datos", 500

@app.route('/search')
def search():
    try:
        tags = request.args.get('query', '').split(',')
        author = request.args.get('author', '')
        db = Database()
        quotes = db.get_all_quotes()
        
        if tags and tags[0]:
            quotes = quotes[quotes['tags'].apply(lambda x: any(tag.strip().lower() in x.lower() for tag in tags))]
        
        if author:
            quotes = quotes[quotes['author'].str.lower() == author.lower()]
        
        db.close()
        return render_template('quotes.html', quotes=quotes.to_dict('records'))
    except Exception as e:
        logging.error(f"Error en la búsqueda: {str(e)}")
        return "Error en la búsqueda", 500

@app.route('/get_filters')
def get_filters():
    try:
        db = Database()
        all_quotes = db.get_all_quotes()
        logging.info(f"Columns in all_quotes: {all_quotes.columns}")
        logging.info(f"Sample of tags: {all_quotes['tags'].head()}")
        logging.info(f"Sample of authors: {all_quotes['author'].head()}")
        
        # Manejo de tags
        tags = set()
        if 'tags' in all_quotes.columns:
            for tag_str in all_quotes['tags'].dropna():
                if isinstance(tag_str, str):
                    tags.update(tag.strip() for tag in tag_str.split(','))
        
        # Manejo de autores
        authors = set()
        if 'author' in all_quotes.columns:
            authors = set(author for author in all_quotes['author'].dropna() if isinstance(author, str))
        
        db.close()
        return jsonify({'tags': sorted(list(tags)), 'authors': sorted(list(authors))})
    except Exception as e:
        logging.error(f"Error en get_filters: {str(e)}")
        return jsonify({'tags': [], 'authors': []}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)