from datetime import datetime
import backtrader as bt
import os.path  # 管理路径
import sys  # 发现脚本名字(in argv[0])
import pandas as pd

# 创建策略类


class GenericCSV_TAG(bt.feeds.GenericCSVData):

    # Add a 'pe' line to the inherited ones from the base class
    lines = ('tag',)

    # openinterest in GenericCSVData has index 7 ... add 1
    # add the parameter to the parameters inherited from the base class
    params = (('tag', 8),)


class SmaCross(bt.Strategy):
    # 定义参数

    def __init__(self):
        # 移动平均线指标
        pass
        # self.move_average = bt.ind.MovingAverageSimple(
        # self.datas[0].close, period=self.params.period)

    def next(self):
        print(self.data.tag[0])
        # print(self.tag[0])
      # 还没有仓位
        # 当日收盘价上穿5日均线，创建买单，买入100股
        if (self.data.tag[0] == 1):
            self.sell(self.broker.get_cash()/self.data.open[0])
        if (self.data.tag[0] == 0):
            self.buy(size=10)


cerebro = bt.Cerebro()


df = '/Users/zed/AI_Lab/DoubleEnsembleML/src/pred.csv'
data = GenericCSV_TAG(dataname=df,
                      datetime=0,  # 日期行所在列
                      open=1,  # 开盘价所在列
                      high=2,  # 最高价所在列
                      low=3,  # 最低价所在列
                      close=4,  # 收盘价价所在列
                      volume=5,  # 成交量所在列
                      # 无未平仓量列.(openinterest是期货交易使用的)
                               openinterest=-1,
                               # 日l期格式
                               dtformat=('%Y-%m-%d'),
                               fromdate=datetime(2014, 3, 8),  # 起始日
                               todate=datetime(2021, 3, 8))

cerebro.adddata(data)  # 将行情数据对象注入引擎
cerebro.addstrategy(SmaCross)  # 将策略注入引擎
cerebro.broker.setcash(10000.0)  # 设置初始资金
cerebro.broker.setcommission(commission=0.00000000003)
cerebro.run()

print('最终市值: %.2f' % cerebro.broker.getvalue())

cerebro.plot(style='bar')
