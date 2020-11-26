### 機械学習を使ってローン審査予測モデルを作りました！

コード：[google colabで開く](https://colab.research.google.com/drive/1Gg65BXKWWumWzWrbMYexzbhufZLMg8Sm?usp=sharing)<br>
※google colabで開く場合は以下のファイルをgoogleドライブ上「drive/My Drive/av_loan_u6lujuX_CVtuZ9i.csv」「drive/My Drive/av_loan_test_Y3wMUE5_7gLdaTN.csv」にアップロードしてください。
<br>
<br>
モデル用データ：[googleスプレッドシートで開く](https://drive.google.com/file/d/1kz4IezeMC423Me_HS0vvKkB0iBGLmDaC/view?usp=sharing)<br>
スコア用データ：[googleスプレッドシートで開く](https://drive.google.com/file/d/1MaplBuB9FjPrG55HAtY57soa_YPAju5x/view?usp=sharing)<br>


### 概要

以下のような特徴量を用いて、ローン審査に合格すると予測されるデータに対して0を、不合格と予測されるデータに対して1を返すモデルを作ります。

|性別|既婚者か否か|扶養している子供の人数|大学既卒か否か|自営業を営んでいるか否か|申請者の所得(千円)|共同申請者の所得(千円)|ローン残高(千円)|ローンの返済期間(日)|ローンの返済状況(返済可能な場合は1、返済不可能な場合は0)|都内在住か田舎在住か|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
<br>

### データ処理

モデル用データとスコア用データにはそれぞれ欠損値やカテゴリ変数が存在し、また「Dependents_3+」はモデル用データにのみ存在し、Gender_Unknownはスコア用データにのみ存在します。<br>

そこで、まずモデル用データの正解ラベル「Loan_Status」(Y,N)に対して、Yとなったサンプルを0に、Nとなったサンプルを1に変換します。<br>

(例)
|Loan_Status|
|:---|
|Y|   
|N|
|Y|

&nbsp; &nbsp; &nbsp; <img src="https://uploda2.ysklog.net/135c254819b82f68a3113a21fcd44f09.jpg" width="50">

|Loan_Status|
|:---|
|0|   
|1|
|0|

次にモデル用データに対してone-hotエンコーディングを行い、カテゴリ変数を数値化します。<br>

(例)
|Dependents|
|:---|
|0|
|1|
|2|
|3+|

&nbsp; &nbsp; &nbsp; <img src="https://uploda2.ysklog.net/135c254819b82f68a3113a21fcd44f09.jpg" width="50">

|Dependents_0|Dependents_1|Dependents_2|Dependents_3+|
|:---|:---|:---|:---|
|1|0|0|0|
|0|1|0|0|
|0|0|1|0|
|0|0|0|1|

次にモデル用データに対してSimpleImputerクラスを使い、欠損値を平均値で補完します。<br>

(例)
|ApplicantIncome|
|:---|
|3000|
|7000|
|NaN|
|4000|
|5000|

&nbsp; &nbsp; &nbsp; <img src="https://uploda2.ysklog.net/135c254819b82f68a3113a21fcd44f09.jpg" width="50">

|ApplicantIncome|
|:---|
|3000|
|7000|
|4750|
|4000|
|5000|

さらにモデル用データに対してRFEクラスを使い、特徴量因子の重要度を推定しつつ、重要な特徴量だけを10個選択します。<br>

(特徴量26個)
|ApplicantIncome|CoapplicantIncome|LoanAmount|Loan_Amount_Term|Credit_History|Dependents_0|Dependents_1|Dependents_2|Dependents_3+|Dependents_nan|Gender_Female|Gender_Male|Gender_nan|Married_No|Married_Yes|Married_nan|Education_Graduate|Education_NotGraduate|Education_nan|Self_Employed_No|Self_Employed_Yes|Self_Employed_nan|Property_Area_Rural|Property_Area_Semiurban|Property_Area_Urban|Property_Area_nan|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|

&nbsp; &nbsp; &nbsp; <img src="https://uploda2.ysklog.net/135c254819b82f68a3113a21fcd44f09.jpg" width="50">

(特徴量10個)
|ApplicantIncome|CoapplicantIncome|LoanAmount|Loan_Amount_Term|Credit_History|Dependents_0|Married_No|Education_Graduate|Property_Area_Rural|Property_Area_Semiurban|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|

モデル用データのみに登場する変数を復活させ、反対にスコア用データのみに登場する変数を削除します。<br>

