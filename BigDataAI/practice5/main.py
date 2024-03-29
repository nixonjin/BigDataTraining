import os
import matplotlib as mpl
mpl.use('TkAgg')
import joblib
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, classification_report, \
    accuracy_score
from yellowbrick import ROCAUC
from yellowbrick.classifier import ClassPredictionError, ClassificationReport, ConfusionMatrix, DiscriminationThreshold
from yellowbrick.model_selection import LearningCurve, CVScores, FeatureImportances, RFECV, ValidationCurve
import numpy as np


if __name__ == '__main__':
    # 显示所有行
    pd.set_option('display.max_rows', None)

    train_data_path = os.path.join('../practice3', 'train_data.csv')
    test_data_path = os.path.join('../practice3', 'test_data.csv')

    # 读取数据
    train_df = pd.read_csv(train_data_path)
    y_train = train_df.get('Survived')
    X_train = train_df.drop('Survived', axis=1)
    # PassengerId 是主键，没有训练意义，舍弃该特征
    # X_train.drop("PassengerId", axis=1, inplace=True)

    test_df = pd.read_csv(test_data_path)
    y_test = test_df.get('Survived')
    X_test = test_df.drop('Survived', axis=1)
    # X_test = X_test.drop('PassengerId', axis=1)
    # PassengerId
    # id_test = test_df[['PassengerId', 'Survived']]
    id_test = test_df[['Survived']]


    model_path = os.path.join('../model', 'rf.pkl')
    model = joblib.load(model_path)
    y_pred = model.predict(X_test)
    id_test['prediction'] = y_pred

    # 查看预测结果
    print(f"预测结果:{id_test}")

    # 评估
    # 准确率
    accuracy_score_value = accuracy_score(y_test, y_pred)
    print(f"准确率:{accuracy_score_value}")

    precision_score_value = precision_score(y_test, y_pred)
    print(f"精确率:{precision_score_value}")

    recall_score_value = recall_score(y_test, y_pred)
    print(f"召回率:{recall_score_value}")

    f1_score_value = f1_score(y_test, y_pred)
    print(f"f1值:{f1_score_value}")

    confusion_matrix_value = confusion_matrix(y_test, y_pred)
    print(f"混淆矩阵:{confusion_matrix_value}")

    report = classification_report(y_test, y_pred)
    print(f"分类报告:{report}")

    # 可视化
    # ROCAUC
    visualizer = ROCAUC(model)
    visualizer.score(X_test, y_test)
    visualizer.show()

    # 分类预测
    visualizer = ClassPredictionError(model)
    visualizer.score(X_test, y_test)
    visualizer.show()

    # 分类报告
    visualizer = ClassificationReport(model)
    visualizer.score(X_test, y_test)
    visualizer.show()

    # 混淆矩阵
    visualizer = ConfusionMatrix(model)
    visualizer.score(X_test, y_test)
    visualizer.show()

    # 阈值选择
    visualizer = DiscriminationThreshold(model)
    visualizer.fit(X_train, y_train)
    visualizer.show()

    # 学习率
    visualizer = LearningCurve(
        model, scoring='f1_weighted'
    )
    visualizer.fit(X_train, y_train)
    visualizer.show()

    # 交叉验证
    visualizer = CVScores(model, cv=5, scoring='f1_weighted')
    visualizer.fit(X_train, y_train)
    visualizer.show()

    # 特征重要性
    visualizer = FeatureImportances(model)
    visualizer.fit(X_train, y_train)
    visualizer.show()

    # 特征递归消减
    visualizer = RFECV(model, cv=5, scoring='f1_weighted')
    visualizer.fit(X_train, y_train)
    visualizer.show()

    # 特征选择
    visualizer = ValidationCurve(
        model, param_name="max_depth",
        param_range=np.arange(1, 11), cv=5, scoring="f1_weighted"
    )
    visualizer.fit(X_train, y_train)
    visualizer.show()
