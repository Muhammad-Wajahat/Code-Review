import os
from datetime import date
from urllib import parse
from sqlalchemy import text
import pandas as pd
import psycopg2
from fastapi import FastAPI, Depends
from sqlalchemy import Column, String, BigInteger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine("postgresql://postgres:{password}@localhost:5432/Reddit".format(password=parse.quote('347809')))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ItemsRedditPost(Base):
    __tablename__ = "Posts"
    Link = Column(String)
    Post = Column(String, primary_key=True)
    Post_Date = Column(String)
    Img = Column(String)
    Detail = Column(String)


Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/ShowPost")
def ShowRedditPost( session: Session = Depends(get_db)):
    try:
        with engine.begin() as conn:
            query = text('''SELECT * FROM public."Posts" ''')
            df = pd.read_sql_query(query, conn)
        return df.to_dict('records')
        session.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        session.rollback()
    session.close()


@app.get("/GetPost")
def GetRedditPost( session: Session = Depends(get_db)):

    os.system('python D:\Shaheer\FYP\RedditAPI\main.py')
    try:
        with engine.begin() as conn:
            query = text('''SELECT * FROM public."Posts" ''')
            df = pd.read_sql_query(query, conn)
        return df.to_dict('records')
        session.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        session.rollback()
    session.close()


# @app.get("/query={keyword}")
# def getRedditKeyword(keyword: str, session: Session = Depends(get_db)):
#     con = engine.connect()
#     key = keyword.replace(' ', '%20')
#     print('-----------------------------------------------------------------------------')
#     print(key)
#     print('-----------------------------------------------------------------------------')
#     df = pd.read_sql(
#         f'''select * from public."Search_Logs" where "text" like '%%{keyword}%%' ''',
#         con)
#
#     con.close()
#     if df.empty:
#         try:
#             os.chdir('E:/finalRedit/Redit/Redit/spiders')
#             os.system(f"scrapy crawl Reddit -a query='{key}'")
#             con = engine.connect()
#             index = df['SearchId'][0]
#             df0 = pd.read_sql(
#                 f'''select * from public."Post" where "SearchId" = {index} ''',
#                 con)
#             session.commit()
#             con.close()
#             if df0.empty:
#                 session.close()
#                 return "False"
#             session.close()
#             return "True"
#         except (Exception, psycopg2.DatabaseError) as error:
#             print("Error: %s" % error)
#             session.rollback()
#
#
#     else:
#         Today = df['Time']
#         print(Today[0])
#         print(type(date.today()))
#         if (Today[0] != (date.today())):
#             try:
#                 os.chdir('E:/finalRedit/Redit/Redit/spiders')
#                 os.system(f"scrapy crawl Reddit -a query='{key}'")
#                 con = engine.connect()
#                 index = df['searchId'][0]
#                 con.execute(
#                     f'''update public."Search_Logs" set "Time"='{date.today()}' where ("text" like '%%{keyword.upper()}%%' OR "text" like '%%{keyword.lower()}%%' OR "text" like '%%{keyword}%%' )''')
#                 session.commit()
#                 df0 = pd.read_sql(
#                     f'''select * from public."Post" where "SearchId" ={index} ''',
#                     con)
#                 session.commit()
#                 con.close()
#                 if df0.empty:
#                     session.close()
#                     return "False"
#                 session.close()
#                 return "True"
#             except (Exception, psycopg2.DatabaseError) as error:
#                 print("Error: %s" % error)
#                 session.rollback()
#
#     session.close()
#     return "True"