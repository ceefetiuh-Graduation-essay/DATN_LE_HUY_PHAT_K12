#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from model.naive_bayes_model import NaiveBayesModel
from model.svm_model import SVMModel

class TextClassificationPredict(object):

    def __init__(self):
        #  train data
        train_data = []
        train_data.append({"feature": u"Hôm nay trời đẹp không ?", "target": "hoi_thoi_tiet"})
        train_data.append({"feature": u"Hôm nay thời tiết thế nào ?", "target": "hoi_thoi_tiet"})
        train_data.append({"feature": u"Hôm nay mưa không ?", "target": "hoi_thoi_tiet"})
        train_data.append({"feature": u"Chào em gái", "target": "chao_hoi"})
        train_data.append({"feature": u"Chào bạn", "target": "chao_hoi"})
        train_data.append({"feature": u"Hello bạn", "target": "chao_hoi"})
        train_data.append({"feature": u"Hi bot", "target": "chao_hoi"})
        train_data.append({"feature": u"Hi em", "target": "chao_hoi"})
        train_data.append({"feature": u"Bật", "target": "bat_den"})
        train_data.append({"feature": u"Bật đèn lên", "target": "bat_den"})
        train_data.append({"feature": u"Bật đèn đi", "target": "bat_den"})
        train_data.append({"feature": u"On", "target": "bat_den"})
        train_data.append({"feature": u"Turn on", "target": "bat_den"})
        train_data.append({"feature": u"Tối quá", "target": "bat_den"})
        train_data.append({"feature": u"Sao tối thế này", "target": "bat_den"})
        train_data.append({"feature": u"Tắt", "target": "tat_den"})
        train_data.append({"feature": u"Tắt đèn", "target": "tat_den"})
        train_data.append({"feature": u"Tắt đèn đi", "target": "tat_den"})
        train_data.append({"feature": u"Turn off", "target": "tat_den"})
        train_data.append({"feature": u"Off", "target": "tat_den"})
        train_data.append({"feature": u"Chói mắt quá", "target": "tat_den"})

        global df_train
        df_train = pd.DataFrame(train_data)

    def classification(self, text):
        #  test data
        self.text = text
        test_data = []
        test_data.append({"feature": f"{self.text}"})
        df_test = pd.DataFrame(test_data)

        # init model naive bayes
        model = SVMModel()

        clf = model.clf.fit(df_train["feature"], df_train.target)

        predicted = clf.predict(df_test["feature"])

        # Print predicted result
        #print (predicted)
        return predicted
        #print (clf.predict_proba(df_test["feature"]))

if __name__ == '__main__':
    tcp = TextClassificationPredict() # khởi tạo object
    data = tcp.classification(str(input("Nhập text: ")))
    print(type(data))
    print(str(data[0]))