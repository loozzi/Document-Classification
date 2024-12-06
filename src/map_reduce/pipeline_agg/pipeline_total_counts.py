def pipeline_total_counts():
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
    return pipeline_total_counts