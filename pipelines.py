from urllib import parse
import pandas as pd
import psycopg2.errors
from itemadapter import ItemAdapter
from sqlalchemy import create_engine

class ReditPipeline:
    def open_spider(self, spider):
        self.engine = create_engine(
            "postgresql://postgres:{password}@localhost:5432/Reddit".format(password=parse.quote('347809')))
        self.conn = self.engine.connect()
        self.i = 0
    def process_item(self, item, spider):
        if spider.name == 'comm':
                if item is not None:
                    if (self.i < 10):
                        df0 = pd.DataFrame.from_dict([ItemAdapter(item).asdict()])
                        try:
                            df0.to_sql('Communities', self.engine, if_exists='append', index=False)
                        except (Exception, psycopg2.errors.UniqueViolation) as error:
                            self.i = self.i + 1
                            print(self.i)
                    else:
                        spider.close.manually = True

        elif spider.name == 'Reddit':
            if item is not None:
                    df0 = pd.DataFrame.from_dict([ItemAdapter(item).asdict()])
                    try:
                        df0.to_sql('Posts', self.engine, if_exists='append', index=False)
                    except (Exception, psycopg2.errors.UniqueViolation) as error:
                        print(" ")

        else:
            print("Wrong spider")

    def close_spider(self, spider):
        self.conn.close()
