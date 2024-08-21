import schedule
import time
from scraper import scrape_quotes
from database import Database
import logging

logging.basicConfig(filename='logs/auto_update.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def update_database():
    logging.info("Iniciando actualización automática de la base de datos")
    try:
        df = scrape_quotes()
        db = Database()
        db.insert_quotes(df)
        db.close()
        logging.info(f"Actualización completada. Se insertaron {len(df)} nuevas citas.")
    except Exception as e:
        logging.error(f"Error durante la actualización: {str(e)}")

def main():
    # Programar la actualización para que se ejecute cada 24 horas
    schedule.every(24).hours.do(update_database)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()