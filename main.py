from http import client
from website import create_app
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client.LmaoJudge

app = create_app()

if __name__ == '__main__':
    app.run(port='3060', debug=True)
