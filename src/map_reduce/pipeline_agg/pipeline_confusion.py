def make_confusion_value():
    pipe_line_TP = [
        {
            "$match": {
                "classX": 1,
                "predclassX": 1
            }
        },
        {
            "$count": "TruePositive"
        }
    ]
    pipe_line_FP = [
        {
            "$match": {
                "classX": 0,
                "predclassX": 1
            }
        },
        {
            "$count": "FalsePositive"
        }
    ]
    pipe_line_TN = [
        {
            "$match": {
                "classX": 0,
                "predclassX": 0
            }
        },
        {
            "$count": "TrueNegative"
        }
    ]
    pipe_line_FN = [
        {
            "$match": {
                "classX": 1,
                "predclassX": 0
            }
        },
        {
            "$count": "FalseNegative"
        }
    ]
    return pipe_line_TP, pipe_line_FP, pipe_line_TN, pipe_line_FN