import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.schema.base import Base

class Postgres:
    def __init__(self, db_name = 'loop_ai', pool_size=10):
        self.db_name = db_name
        self.user = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.port = int(os.getenv('DB_PORT'))
        self.pool_size = int(os.getenv('DB_POOL_SIZE', pool_size))
        self.engine = None
        self.Session = None

    def __enter__(self):
        db_url = f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'
        self.engine = create_engine(db_url, pool_size=self.pool_size)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        return self.Session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.Session:
            self.Session.close_all()


if __name__ == "__main__":
    # Example usage
    with Postgres('mydb') as session:
        # Perform database operations
        result = session.execute("SELECT * FROM my_table")
        rows = result.fetchall()
        for row in rows:
            print(row)
