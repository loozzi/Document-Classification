from .pipeline_agg.pipeline_confusion import make_confusion_value
import matplotlib.pyplot as plt

def confusion_matrix(db=None):
    db.Results.drop()
    pipe_line_TP, pipe_line_FP, pipe_line_TN, pipe_line_FN = make_confusion_value()
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

    plt.figure(figsize=(10, 10))
    plt.matshow([[TP, FP], [FN, TN]], fignum=1)
    plt.colorbar()
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.xticks([0, 1], ["Spam", "Not spam"])
    plt.yticks([0, 1], ["Spam", "Not spam"])
    plt.show()

    db.Results.insert_one({"value": dict_result})

    calculated_confusion_matrix = db.Results.find_one()["value"]

    return calculated_confusion_matrix