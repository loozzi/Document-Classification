# DocumentClassification
Implementation of Multinomial Naive Bayes for document classification: MongoDB + MapReduce

System Specification:
Python 2.7

Python Libraries: NLTK, Pymongo


1. to create a collection with preprocessed files, comment  lines 69 and 87 

  d['content'] = create_content(file) 
  and uncomment lines 70 and 88.

2. specify the full path to folders with train docs and test docs for functions
   create_train_collection() and create_test_collection()

3. specify the full path to map/reduce .js files for functions
	map_reduce() and confusion_matrix()
