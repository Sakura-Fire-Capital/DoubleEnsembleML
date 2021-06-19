# AM218-Spring Group 1 Project

## Data
### Raw Data
数据集中包含从Quandl上调用的几个加密货币的价格信息，在实际项目中只使用了Bitcoin的数据
### Preprocessing of Data
在./Data/data_factor 目录下的数据为经过预处理的数据。在./report/preprocessing.ipynb文件中，是项目最终的预处理过程，产生的./report/mybtc.csv是最终用到的数据。

## Model
### Logistic Regression

目录.\LR\lr.ipynb下

### Decision Tree & Random Forest

.\rf\.

### DoubleEnsemble
模型实现在.\src\final_mdoel.py


最终模型的预测在
.\src\doubleensemble.ipynb

## Backtest

回测文件为.\backtest\myback.py



