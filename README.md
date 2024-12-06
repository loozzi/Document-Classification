# Đề tài

Áp dụng map-reduce trong cơ sở dữ liệu MongoDB để giải quyết bài toán phân loại email spam.

## Mục đích

Phân loại email spam dựa trên thuật toán Naive Bayes

## Mô tả

Cài đặt thuật toán Naive Bayes trên bộ dữ liệu email đã được gắn nhãn. Bộ phân loại được xây dựng dựa trên cơ sở dữ liệu MongoDB.

## Dữ liệu

Dữ liệu lấy từ nguồn Kaggle: [jackksoncsie/spam-email-dataset](https://www.kaggle.com/datasets/jackksoncsie/spam-email-dataset)
Bộ dữ liệu: Gồm 5695 email trong đó có 1335 email spam đã được gắn nhãn

## Kiến thức

- Ngôn ngữ: Python 3.x
- Libraries: Pymongo, nltk, Math, os, glob, codecs, re, bson, flask

## Hướng dẫn chạy

- Cấu hình file môi trường `.env` trong thư mục `/src`
  ```
  MONGODB_URI=<mongodb_uri>
  ```
- Chạy `python DocumentClassification.py` để tạo tập dữ liệu train
- Chạy `python app.py` để khởi chạy UI

## Thành viên nhóm

<table>
    <th>
        <td>Họ tên</td>
        <td>Email</td>
    </th>
    <tr>
        <td>1</td>
        <td>Vũ Thành Đạt</td>
        <td><a href="mailto:22022620@vnu.edu.vn">22022620@vnu.edu.vn</a></td>
    </tr>
    <tr>
        <td>2</td>
        <td>Nguyễn Trần Hải Ninh</td>
        <td><a href="mailto:22022526@vnu.edu.vn">22022526@vnu.edu.vn</a></td>
    </tr>
    <tr>
        <td>3</td>
        <td>Nguyễn Quang Thao</td>
        <td><a href="mailto:22022619@vnu.edu.vn">22022619@vnu.edu.vn</a></td>
    </tr>
</table>
