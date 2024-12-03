from .pipeline_agg.pipeline_count_each_word import pipeline_count_each_word
from .pipeline_agg.pipeline_total_counts import pipeline_total_counts

def map_reduce(trained=False, db=None):
    if trained:
        print("Mapreduce already done")
        return
    if "TotalCounts" in db.list_collection_names():
        db.TotalCounts.drop()
    if "WordCounts" in db.list_collection_names():
        db.WordCounts.drop()


    # TotalCounts
    dict_temp = list(db.train.aggregate(pipeline_total_counts()))[0]
    vocabulary = dict_temp["V"]
    db.TotalCounts.insert_one(dict_temp)
    print("TotalWords: ", vocabulary)
    print("TotalCounts collection created")

    #WordCounts
    list_dict = list(db.train.aggregate(pipeline_count_each_word()))
    db.WordCounts.insert_many(list_dict)
    print("WordCounts collection created")
    return