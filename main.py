from Reddit.Reddit.spiders.Posts import Redditspider
from Reddit.Reddit.spiders.reddit import Redcomm
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process
from urllib import parse
from sqlalchemy import create_engine
import pandas as pd
import concurrent.futures
from sqlalchemy import text
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy import cmdline
def crawler(name):
    try:
        process = CrawlerProcess(settings={'ITEM_PIPELINES' : {'Reddit.Reddit.pipelines.ReditPipeline': 300}})
        process.crawl(Redditspider, query=name)
        process.start()

    except Exception as e:
        print(f"Error crawling community {name}: {e}")



if __name__ == "__main__":
    t1 = time.perf_counter()
    # process = CrawlerProcess(settings={'ITEM_PIPELINES' : {'Reddit.Reddit.pipelines.ReditPipeline': 300}})
    # process.crawl(Redcomm,query='Depression')
    # process.start()
    engine = create_engine("postgresql://postgres:{password}@localhost:5432/Reddit".format(password=parse.quote('347809')))
    with engine.begin() as conn:
        query = text('''SELECT * FROM public."Communities" ''')
        df = pd.read_sql_query(query, conn)
    community = ['r/2Asia4u','r/Anxiety','r/AnxietyDepression','r/AskReddit','r/bakchodi','r/bipolar','r/chutyapa']
    community1=['r/depression','r/depression_help','r/depression_memes','r/depression_partners','r/DepressionBuddies','r/Depressiondens','r/DepressionForGrownups','r/depressionhacks']
    community2=['r/DepressionIsNotAJoke','r/depressionmeals','r/depressionmemes','r/DepressionNests','r/depressionregimens','r/exmuslim','r/ExplorePakistan','r/FreeCompliments']
    community3 = ['r/getting_over_it', 'r/india', 'r/indianews', 'r/IndiaSpeaks', 'r/leaves', 'r/MadeOfStyrofoam', 'r/MilitaryPorn', 'r/news']
    community4 = ['r/NoFap', 'r/offmychest', 'r/PakiBeauties', 'r/pakistan', 'r/pakistanconfessions', 'r/pakistangirls', 'r/PakistanHistoryPorn', 'r/pakistani']
    community5 = ['r/pakistanigirlsforBBC', 'r/pakistanimemes', 'r/PakistaniMilitary', 'r/pakistaniscandals', 'r/PakistaniStarFeet', 'r/PakistaniTech', 'r/PakistanMilitaryPorn', 'r/PakistanRapeWatch']
    community6 = ['r/pics', 'r/rationalpakistan', 'r/SuicideWatch', 'r/TrollXChromosomes', 'r/Turkey', 'r/worldnews']
    Comm=[community,community1,community2,community3,community4,community5,community6]

    print(community)
    for com in Comm:
     with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(crawler,com)

    # print(len(community))
    # for i in range(0,len(community),5):
    #     print(i)
    # p1 = Process(target=crawler, args=(community[i],))
    # p2 = Process(target=crawler, args=(community[i+1],))
    # p3 = Process(target=crawler, args=(community[i+2],))
    # p4 = Process(target=crawler, args=(community[i+3],))
    # p5 = Process(target=crawler, args=(community[i+4],))
    # p1.start()
    # p2.start()
    # p3.start()
    # p4.start()
    # p5.start()
    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')




