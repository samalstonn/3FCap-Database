import pymongo
from data import data
import random
import logins

myclient = pymongo.MongoClient(logins.database)

mydb = myclient["mydatabase"]
mycol = mydb["sample"]


def insert():
    mylist = data
    x = mycol.insert_many(mylist)
    print(x.inserted_ids)


def update():
    """
    Updates existing data in the database
    """
    print("Updating data...")
    baselist = [
        {"name": "Amy"},
        {"name": "Hannah"},
        {"name": "Michael"},
        {"name": "Sandy"},
        {"name": "Betty"},
        {"name": "Richard"},
        {"name": "Susan"},
        {"name": "Vicky"},
        {"name": "Ben"},
        {"name": "William"},
        {"name": "Chuck"},
        {"name": "Viola"},
    ]
    mylist = [
        {"name": "Amy", "address": "Apple st " + str(random.randint(0, 100))},
        {"name": "Hannah", "address": "Mountain " + str(random.randint(0, 100))},
        {"name": "Michael", "address": "Valley " + str(random.randint(0, 100))},
        {"name": "Sandy", "address": "Ocean blvd " + str(random.randint(0, 100))},
        {"name": "Betty", "address": "Green Grass " + str(random.randint(0, 100))},
        {"name": "Richard", "address": "Sky st " + str(random.randint(0, 100))},
        {"name": "Susan", "address": "One way " + str(random.randint(0, 100))},
        {"name": "Vicky", "address": "Yellow Garden " + str(random.randint(0, 100))},
        {"name": "Ben", "address": "Park Lane " + str(random.randint(0, 100))},
        {"name": "William", "address": "Central st " + str(random.randint(0, 100))},
        {"name": "Chuck", "address": "Main Road " + str(random.randint(0, 100))},
        {"name": "Viola", "address": "Sideway " + str(random.randint(0, 100))},
    ]
    for i, v in enumerate(baselist):
        mycol.replace_one(v, mylist[i],upsert=True)
    print(mycol)


def find():
    myquery = {"symbolDescription": "MMM"}

    mydoc = mycol.find_one(myquery)
    for x in mydoc:
        print(x)


def run():
    while True:
        res = input("1:insert, 2:find, 3:update\n")
        if res == 1:
            insert()
        elif res == 2:
            find()
        elif res == 3:
            print("here")
            update()


if __name__ == "__main__":
    update()
