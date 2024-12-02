def map_reduce(trained=False, db=None):
    if trained:
        print("Mapreduce already done")
        return
    if "TotalCounts" in db.list_collection_names():
        db.TotalCounts.drop()
    if "WordCounts" in db.list_collection_names():
        db.WordCounts.drop()


    # TotalCounts
    pipeline_total_counts = [
        {
            "$addFields": {
                "wordCount": { "$size": "$content" }
            }
        },
        {
            "$group": {
                "_id": None,
                "TotalclassX" : { "$sum": {
                    "$cond": [{ "$eq": ["$classX", 1] }, "$wordCount", 0]
                    }
                },
                "TotalclassY" : { "$sum": {
                    "$cond": [{ "$eq": ["$classY", 1] }, "$wordCount", 0]
                    }
                },
                "TotalWords": { "$sum": "$wordCount" }
            }
        },
        {
            "$project": {
                "_id": 0,
                "clX": "$TotalclassX",
                "clY": "$TotalclassY",
                "V": "$TotalWords"
            }
        }
    ]

    dict_temp = list(db.train.aggregate(pipeline_total_counts))[0]
    vocabulary = dict_temp["V"]
    db.TotalCounts.insert_one(dict_temp)
    print("TotalWords: ", vocabulary)
    print("TotalCounts collection created")

    #WordCounts
    pipeline_counts_each_word = [
        {
            "$unwind": "$content" # chia mỗi document thành nhiều document với mỗi document có 1 từ
        },
        {
            "$project": {
                "key": "$content", # key là từ
                "clX": "$classX",
                "clY": "$classY"
            }
        },
        {
            "$group": {
                "_id": "$key",
                "claX": { "$sum": "$clX" },
                "claY": { "$sum": "$clY" }
            }
        },
    ]
    list_dict = list(db.train.aggregate(pipeline_counts_each_word))
    db.WordCounts.insert_many(list_dict)
    print("WordCounts collection created")
    return