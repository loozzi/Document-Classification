def pipeline_count_each_word():
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
    return pipeline_counts_each_word