import math

def caculate_probability(single_document, denominator_x, denominator_y, db):
    probability_class_x = 0.0
    probability_class_y = 0.0
    sum_x = 0.0 # xác suất của spam
    sum_y = 0.0 # xác suất không spam
    for word in single_document["content"]:
        # Lấy dữ liệu từ collection WordCounts
        dict_two = db.WordCounts.find_one({"_id": word})
        if dict_two is not None:
            word_class_x = dict_two["claX"]  # Số lần xuất hiện của từ trong classX
            word_class_y = dict_two["claY"]  # Số lần xuất hiện của từ trong classY
        else:
            word_class_x = 0.0
            word_class_y = 0.0

        # Tính toán xác suất log với add-one smoothing
        sum_x += math.log10((word_class_x + 1.0) / denominator_x)
        sum_y += math.log10((word_class_y + 1.0) / denominator_y)

    # Thêm xác suất lớp vào tổng
    x = sum_x + probability_class_x
    y = sum_y + probability_class_y

    # Dự đoán lớp dựa trên xác suất lớn hơn
    if x > y:
        return 1, 0
    return 0, 1

def naive_bayes_classifier(show=False, db=None, db1=None):
    vocabulary = db.TotalCounts.find_one()["V"]
    class_x = db.TotalCounts.find_one()["clX"]
    class_y = db.TotalCounts.find_one()["clY"]
    denominator_x = class_x + vocabulary  # Dùng cho add-one smoothing
    denominator_y = class_y + vocabulary  # Dùng cho add-one smoothing
    if show:
        check_count = 0
        print("Mapreduce already done")
        print("Naive Bayes Classifier for mini test started")
        test_docs = db.test.find({}).limit(10)
        db1.test.drop()
        db1.test.insert_many(test_docs)
        test_docs = db1.test.find()
        for doc in test_docs:
            predclassX, predclassY = caculate_probability(doc,
                                                          denominator_x,
                                                          denominator_y, db)
            # Update dự đoán vào MongoDB
            try:
                db1.test.update_one(
                    {"_id": doc["_id"]},  # Sử dụng _id để xác định tài liệu
                    {"$set": {"predclassX": predclassX,
                              "predclassY": predclassY,
                              "processed": True}},
                )
            except Exception as e:
                print(f"Error updating document")

            # Log tiến trình
            print(f"Processed document mini test {check_count}with predclassX: {predclassX} and predclassY: {predclassY}")
            check_count += 1
        print("Naive Bayes Classifier for mini test done")
    else:
        # Batch size để xử lý lô nhỏ, xử lý những document chưa được xử lý
        test_docs = db.test.find({"processed": {"$ne": True}}).batch_size(10)
        if(len(list(test_docs)) == 0):
            print("All documents have been processed")
            return
        
        check_count = 0

        # Dự đoán tất cả các document trong test set là classX (spam) hoặc classY (không spam)
        '''Dùng context manager để quản lý con trỏ, con trỏ sẽ tự động đóng khi dùng with như này,
        tránh lỗi timeout của cursor nếu dùng toàn bộ dữ liệu mà không thông qua batch_size'''
        with test_docs as cursor:  
            for doc in cursor:
                predclassX, predclassY = caculate_probability(doc,
                                                              denominator_x,
                                                              denominator_y, db)
                # Update dự đoán vào MongoDB
                try:
                    db.test.update_one(
                        {"_id": doc["_id"]},  # Sử dụng _id để xác định document
                        {"$set": {"predclassX": predclassX,
                                  "predclassY": predclassY,
                                  "processed": True}},
                    )
                except Exception as e:
                    print(f"Error updating document")

                # Log tiến trình
                print(f"Processed document {check_count}")
                check_count += 1

        print("Naive Bayes Classifier done")