import logging
from scraper import scrape_quotes
from database import Database
import auto_update


logging.basicConfig(filename='logs/scraper.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def main():
    logging.info("Iniciando el proceso de scraping")
    df = scrape_quotes()
    logging.info(f"Se obtuvieron {len(df)} frases")

    db = Database()
    db.insert_quotes(df)
    logging.info("Frases almacenadas en la base de datos")
    db.close()

if __name__ == "__main__":
    main()