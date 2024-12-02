# Định nghĩa hàm confusion_matrix() để tính toán confusion matrix và các thông số Precision, Recall, F1-score
def confusion_matrix(db=None):
    db.Results.drop()
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
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    try:
        TP = list(db.test.aggregate(pipe_line_TP))[0]["TruePositive"]
    except:
        TP = 0
    try:
        FP = list(db.test.aggregate(pipe_line_FP))[0]["FalsePositive"]
    except:
        FP = 0
    try:
        TN = list(db.test.aggregate(pipe_line_TN))[0]["TrueNegative"]
    except:
        TN = 0
    try:
        FN = list(db.test.aggregate(pipe_line_FN))[0]["FalseNegative"]
    except:
        FN = 0
    
    # Tính toán  F1-score, Precision, Recall

    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1_score = 2 * precision * recall / (precision + recall)

    dict_result = {
        "TP": TP,
        "FP": FP,
        "TN": TN,
        "FN": FN,
        "Precision": precision,
        "Recall": recall,
        "F1-score": f1_score
    }

    db.Results.insert_one({"value": dict_result})

    calculated_confusion_matrix = db.Results.find_one()["value"]

    return calculated_confusion_matrix