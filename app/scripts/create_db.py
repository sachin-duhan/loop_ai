import os
import csv
import gdown
import logging

from dotenv import load_dotenv

from app.constants import raw_data
from app.common.postgres import Postgres
from app.schema.store import Store, BusinessHours, Timezone
from app.common.logger import init_logger
from app.constants import LOG_PATH, PRFETCH_DATA_TO_DB

load_dotenv()
init_logger()

LOGGER = logging.getLogger(__name__)

with Postgres() as db_session:

    def load_data_from_csv(file_key: str, table):
        os.makedirs(LOG_PATH, exist_ok=True)
        file_name = f"{file_key}.csv"
        if not os.path.exists(os.path.join(LOG_PATH, file_name)):
            gsheet_id = raw_data[file_key]
            if not gsheet_id:
                raise RuntimeError(
                    "Could not download google sheet raw data. Update app.constants file"
                )

            gdown.download(
                id=gsheet_id, output=os.path.join(LOG_PATH, file_name), quiet=False
            )
            LOGGER.success(f"Downloaded {file_key}")
            data_exits = False

        if not PRFETCH_DATA_TO_DB:
            return

        data_rows = []
        batch_size = 50000

        LOGGER.info(f"Starting DB upload for {file_key}")
        event_count = 0
        with open(os.path.join(LOG_PATH, file_name), "r") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                event_count += 1
                data = {}
                for index, column in enumerate(table.__table__.columns):
                    data[column.name] = row[index]

                if index % batch_size == 0:
                    db_session.bulk_insert_mappings(table, data_rows)
                    db_session.commit()
                    data_rows = []  # Reset the list for the next batch

            if data_rows:
                db_session.bulk_insert_mappings(table, data_rows)
                db_session.commit()

            LOGGER.success(f"Completed upload for total {event_count} entries.")
            file.close()

    preload_tables = {
        "store_data": Store,
        "business_hours_data": BusinessHours,
        "timezone_data": Timezone,
    }

    for file_name, Schema in preload_tables.items():
        load_data_from_csv(file_name, Schema)
        file_path = os.path.join(LOG_PATH, file_name)
        if os.path.exists(file_path) and PRFETCH_DATA_TO_DB:
            os.remove(file_path)

    LOGGER.success(f"Loaded required data files at {LOG_PATH}")
    db_session.close()
