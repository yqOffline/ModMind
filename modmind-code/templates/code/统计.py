# -*- coding: utf-8 -*-
"""
统计.py —— 统计类模型模板
覆盖：回归分析 / PCA 降维 / KMeans 聚类 / 分类（随机森林）

铁律：
  - 先划分训练/测试集，再做标准化（防数据泄漏）。
  - PCA、聚类、逻辑回归/SVM 必须标准化；树模型（随机森林）可免。
  - 回归看 R² + p 值；分类看 AUC/F1/混淆矩阵，不只准确率。
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (roc_auc_score, confusion_matrix,
                             classification_report)


# ---------- 1. 回归分析（statsmodels，要 p 值）----------
def regression(X, y, feature_names=None):
    """X: 特征矩阵；y: 目标（连续）。打印完整回归结果（R²、系数、p 值）。"""
    import statsmodels.api as sm
    X = np.array(X, float)
    y = np.array(y, float)
    X1 = sm.add_constant(X)  # 加截距
    model = sm.OLS(y, X1).fit()
    print(model.summary(xname=['const'] + (feature_names or
                       [f'x{i}' for i in range(X.shape[1])])))
    return model


# ---------- 2. PCA 降维 ----------
def pca_reduce(X, n_components=None):
    """X: 特征矩阵（会自动标准化）。返回 (降维后数据, 模型)。
    用累计贡献率定 k：explained_variance_ratio_.cumsum()。"""
    X = StandardScaler().fit_transform(np.array(X, float))
    pca = PCA(n_components=n_components)
    X_new = pca.fit_transform(X)
    cum = np.cumsum(pca.explained_variance_ratio_)
    print("各主成分方差贡献率:", pca.explained_variance_ratio_.round(4))
    print("累计贡献率:", cum.round(4))
    return X_new, pca


# ---------- 3. KMeans 聚类（肘部法则定 k）----------
def kmeans_fit(X, k_max=10):
    """X: 特征矩阵（会自动标准化）。返回 (肘部法则的 inertia 列表, 最佳 k 建议)。"""
    Xs = StandardScaler().fit_transform(np.array(X, float))
    inertia = []
    for k in range(1, k_max + 1):
        km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(Xs)
        inertia.append(km.inertia_)
    return inertia, Xs


def kmeans_labels(Xs, k):
    """对已标准化的数据做聚类，返回标签。"""
    return KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(Xs)


# ---------- 4. 分类（随机森林 + AUC + 混淆矩阵 + 交叉验证）----------
def classify(X, y, test_size=0.3, random_state=30):
    """X: 特征；y: 标签（0/1 或类别）。返回训练好的模型与评估结果。
    注意：调用方应保证「先划分、再预处理」的顺序。"""
    X = np.array(X, float)
    y = np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y)
    clf = RandomForestClassifier(n_estimators=100, random_state=random_state)
    clf.fit(X_train, y_train)
    acc = clf.score(X_test, y_test)
    cv = cross_val_score(clf, X, y, cv=5).mean()
    print("测试集准确率:", round(acc, 4))
    print("5 折交叉验证均分:", round(cv, 4))
    print("混淆矩阵:\n", confusion_matrix(y_test, clf.predict(X_test)))
    if len(np.unique(y)) == 2:
        # 二分类给 AUC
        try:
            auc = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])
            print("AUC:", round(auc, 4))
        except ValueError:
            pass
    print(classification_report(y_test, clf.predict(X_test)))
    return clf


# ---------- 自测 ----------
if __name__ == "__main__":
    rng = np.random.default_rng(0)
    X = rng.normal(size=(200, 4))
    y = (X[:, 0] + X[:, 1] > 0).astype(int)  # 二分类
    classify(X, y)
