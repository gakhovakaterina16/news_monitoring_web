from datetime import datetime
from model import News

def return_news_to_user(dt_start, dt_finish, latitude, longitude):
    with webapp.app_context():
        news = News.query.filter_by(date_and_time=dt_start).all()
        return news     

if __name__ == "__main__":
    dt_start = datetime.now()
    dt_finish = dt_start
    latitude = 55.835606
    longitude = 37.52639

    result = return_news_to_user(dt_start, dt_finish, latitude, longitude)
    print(result)