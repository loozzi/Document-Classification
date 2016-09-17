# Document Classification#
Multinomial Naive Bayes classifier for document classification.

## Purpose ##
The project I did for my Information Retrieval course. This project is solely for sharing my implementation, not for further development.

## Description ##
The implementation of Naive Bayes classifier for classification of 120 blog files. The classifier is implemented on top of NoSQL database MongoDB. The MapReduce model is used for text categorization task. The algorithm returns a confusion matrix as an output.

## Data ##
The original data collection consisted of 120 files. The `fortnow` files correspond to posts from the Computational Complexity blog by Prof Lance Fortnow. The `random` files come from blogs chosen “at random” by a human. The dataset was split in two parts:  

* `data/train` : fortnow1 - fortnow30, random1 - random30
* `data/test` : fortnow31 - fortnow60, random31 - random60.

## Stack ##
* Language : Python 2.7
* Libraries : Pymongo, nltk, Math, os, glob, codecs, re, bson

## How to run ##
* Start the server (`mongod`) on your machine by running the following command in terminal : `mongod -dbpath <path>`
* Start the client (`mongo`) by running the following command in terminal : `mongo`
* Run `DocumentClassification.py`

## Notes ##
* To create a collection with preprocessed files, in functions `create_train_collection` and `create_test_collection` :
comment the line `my_dict['content'] = create_content(file)`;
uncomment the line `my_dict['content'] = create_preprocessed_content(file)`.
* For a full description of data pre-processing, formulas and results check my report in the `docs` folder.

