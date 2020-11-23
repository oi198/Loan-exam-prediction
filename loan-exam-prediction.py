#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import RFE
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


#--------------------------------------------------------------------------------------------------
df = pd.read_csv('./data/av_loan_u6lujuX_CVtuZ9i.csv', header=0) #モデル用データを取得

#print(df) 取得したモデル用データフレームを表示

X  = df.iloc[:,:-1]            # 最終列以前を特徴量
ID = X.iloc[:,[0]]             # 第0列はIDとしてセット
X  = X.drop('Loan_ID', axis=1) # Loan_IDは特徴ベクトルから削除
y  = df.iloc[:,-1]             # 最終列は正解ラベル
#--------------------------------------------------------------------------------------------------
df_s = pd.read_csv('./data/av_loan_test_Y3wMUE5_7gLdaTN.csv', header=0) #スコア用データを取得

#print(df_s) 取得したスコア用データフレームを表示

ID_s = df_s.iloc[:,[0]]            # 第0列はIDとしてセット
X_s  = df_s.drop('Loan_ID',axis=1) # Loan_IDは特徴ベクトルから削除
#--------------------------------------------------------------------------------------------------

# ローン審査でNOとなったサンプルを1（正例）yesとなったサンプルを0（負例）として変換
class_mapping = {'N':1, 'Y':0}
y = y.map(class_mapping)

# カテゴリ変数をリストで設定
ohe_columns = ['Dependents',
               'Gender',
               'Married',
               'Education',
               'Self_Employed',
               'Property_Area']

X_ohe = pd.get_dummies(X,dummy_na=True, columns=ohe_columns)  #カテゴリ変数を数量化するためにone-hotエンコーディング
X_ohe_s = pd.get_dummies(X_s, dummy_na=True, columns=ohe_columns) #カテゴリ変数を数量化するためにone-hotエンコーディング

#print(X_ohe) one-hotエンコーディング後のデータフレームを表示

imp = SimpleImputer() #連続値の欠損値を平均値で補うためのSimpleImputer
imp.fit(X_ohe) #インピュータインスタンスを学習させる

X_ohe_columns = X_ohe.columns.values #欠損値補完する前にカラムを取得
X_ohe = pd.DataFrame(imp.transform(X_ohe), columns=X_ohe_columns) #欠損値補完

#print(X_ohe) 欠損値補完後のデータフレームを表示

selector = RFE(RandomForestClassifier(n_estimators=100, random_state=1), n_features_to_select=10, step=.05)
# 特徴量因子の重要度を推定する分類器をRandomForestClassifierに設定
# 最終的に残す特徴量を10に設定
# 1回のstepで削除する次元数は5%ずつとした
selector.fit(X_ohe,y) #特徴量セレクターを学習させる

#print(selector.support_) 残された10個の特徴量カラムを取得

# 26次元を10次元を圧縮
X_fin = X_ohe.loc[:, X_ohe_columns[selector.support_]]

#print(X_fin) 圧縮したデータフレームを表示
#--------------------------------------------------------------------------------------------------
cols_model = set(X_ohe.columns.values) #モデル用データのカラムを取得
cols_score = set(X_ohe_s.columns.values) #スコア用データのカラムを取得

diff1 = cols_model - cols_score
#print('モデルのみに存在する項目: %s' % diff1)

diff2 = cols_score - cols_model
#print('スコアのみに存在する項目: %s' % diff2)

#Dependents_3+はスコアリングデータには存在しない。またGender_Unknownはスコアリングデータで新たに登場した。
#そこでモデル用にはあるが、スコア用に存在しない変数は復活させる。さらにスコア用データにあるが、モデル用に存在しない変数は削除する。

df_cols_m = pd.DataFrame(None, columns=X_ohe_columns, dtype=float) #モデル用データのカラムをデータフレーム型で取得

X_ohe_s2 = pd.concat([df_cols_m, X_ohe_s]) #モデル用データのみに登場する変数を復活させる

set_Xm = set(X_ohe.columns.values)
set_Xs = set(X_ohe_s.columns.values)

X_ohe_s3 = X_ohe_s2.drop(list(set_Xs-set_Xm),axis=1) #スコア用データのみに登場する変数を削除
X_ohe_s3.loc[:,list(set_Xm-set_Xs)] = X_ohe_s3.loc[:,list(set_Xm-set_Xs)].fillna(0,axis=1) #復活させたカラムをゼロ埋め

X_ohe_s3 = X_ohe_s3.reindex(X_ohe.columns.values,axis=1) #モデリング時点のone-hotエンコーディング後の並び順に制御
X_ohe_s4 = pd.DataFrame(imp.transform(X_ohe_s3),columns=X_ohe_columns) #スコア用データの欠損値を平均値で補完

X_fin_s = X_ohe_s4.loc[:, X_ohe_columns[selector.support_]] #学習済みのRFEクラスのインスタンスを使って選択された特徴量インデックスを指定
#--------------------------------------------------------------------------------------------------

#display(X_fin) モデル用データを表示
#display(X_fin_s) スコア用データを表示

#--------------------------------------------------------------------------------------------------
# holdout
X_train,X_test,y_train,y_test=train_test_split(X_fin, y, test_size=0.3, random_state=1)

#アルゴリズムをパイプラインで設定
pipelines = {
    'knn':
        Pipeline([('scl',StandardScaler()),
                  ('est',KNeighborsClassifier())]),
    'logistic':
        Pipeline([('scl',StandardScaler()),
                  ('est',LogisticRegression(random_state=1))]),
    'rsvc':
        Pipeline([('scl',StandardScaler()),
                  ('est',SVC(C=1.0, kernel='rbf', class_weight='balanced', random_state=1))]),
    'lsvc':
        Pipeline([('scl',StandardScaler()),
                  ('est',LinearSVC(C=1.0, class_weight='balanced', random_state=1))]),
    'tree':
        Pipeline([('scl',StandardScaler()),
                  ('est',DecisionTreeClassifier(random_state=1))]),
    'rf':
        Pipeline([('scl',StandardScaler()),
                  ('est',RandomForestClassifier(random_state=1))]),
    'gb':
        Pipeline([('scl',StandardScaler()),
                  ('est',GradientBoostingClassifier(random_state=1))]),
    'mlp':
        Pipeline([('scl',StandardScaler()),
                  ('est',MLPClassifier(hidden_layer_sizes=(3,3),
                                       max_iter=1000,
                                       random_state=1))])
}

#各アルゴリズムの精度を取得
scores = {}
for pipe_name, pipeline in pipelines.items():
    pipeline.fit(X_train, y_train) #パイプライン内の各アルゴリズムを訓練データで学習
    scores[(pipe_name,'train')] = accuracy_score(y_train, pipeline.predict(X_train)) #正解ラベルと予測値のaccuracyをscoresに保存
    scores[(pipe_name,'test')] = accuracy_score(y_test, pipeline.predict(X_test)) #正解ラベルと予測値のaccuracyをscoresに保存
    
#pd.Series(scores).unstack() 各アルゴリズムの正解率を表示
#最も精度が高いLogisticRegressionを採用
#--------------------------------------------------------------------------------------------------

#ロジスティック回帰を使ってスコア用データのローン審査を予測する
ans = pd.Series(pipelines['logistic'].predict(X_fin_s))
print(ans)

