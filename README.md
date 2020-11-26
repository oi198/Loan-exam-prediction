### 機械学習を使ってローン審査予測モデルを作りました！

コード：[google colabで開く](https://colab.research.google.com/drive/1Gg65BXKWWumWzWrbMYexzbhufZLMg8Sm?usp=sharing)<br>
<br>
※google colabで開く場合は以下のファイルをgoogleドライブ上「drive/My Drive/av_loan_u6lujuX_CVtuZ9i.csv」「drive/My Drive/av_loan_test_Y3wMUE5_7gLdaTN.csv」にアップロードしてください
<br>
モデル用データ：[googleスプレッドシートで開く](https://drive.google.com/file/d/1kz4IezeMC423Me_HS0vvKkB0iBGLmDaC/view?usp=sharing)<br>
スコア用データ：[googleスプレッドシートで開く](https://drive.google.com/file/d/1MaplBuB9FjPrG55HAtY57soa_YPAju5x/view?usp=sharing)<br>


### 概要

以下のような特徴量を用いて、ローン審査に合格すると予測されるデータに対して0を、不合格と予測されるデータに対して1を返すモデルを作ります

|性別|既婚者か否か|扶養している子供の人数|大学既卒か否か|自営業を営んでいるか否か|申請者の所得(千円)|共同申請者の所得(千円)|ローン残高(千円)|ローンの返済期間(日)|ローンの返済状況(返済可能な場合は1、返済不可能な場合は0)|都内在住か田舎在住か|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|

<br>

