import settings
import psycopg2

con = psycopg2.connect(
    database=settings.DB_NAME,
    user=settings.DB_USERNAME,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT
)
cur = con.cursor()

query = "SELECT src FROM news_locations"
cur.execute(query)
res = cur.fetchall()
links = []
for l in res:
    links.append(l[0])


print(links)

con.commit()
con.close()