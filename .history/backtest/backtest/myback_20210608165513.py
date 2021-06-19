from datetime import datetime
import backtrader as bt
import os.path  # 管理路径
import sys  # 发现脚本名字(in argv[0])
import pandas as pd


class MLStrategy(bt.Strategy):
    params = dict(
    )

    def __init__(self):
        # 跟踪股票open, close价和predicted值
        self.data_predicted = self.datas[0].predicted  # 这就是机器学习算法的预测值
        self.data_open = self.datas[0].open
        self.data_close = self.datas[0].close

        # 跟踪未决订单/buy price/buy commission
        self.order = None
        self.price = None
        self.comm = None
    # logging function

    def log(self, txt):
        '''Logging function'''
        dt = self.datas[0].datetime.date(0).isoformat()
        print(f'{dt}, {txt}')

    # def notify_order(self, order):
    #     if order.status in [order.Submitted, order.Accepted]:
    #         # order already submitted/accepted - no action required
    #         return
    #     # report executed order
    #     if order.status in [order.Completed]:
    #         if order.isbuy():
    #             # self.log(f'BUY EXECUTED - -- Price: {order.executed.price: .2f},
    #             #          Cost: {order.executed.value: .2f}, Commission: {order.executed.comm: .2f}')
    #             self.price = order.executed.price
    #             self.comm = order.executed.comm
    #         else:
    #             # self.log(f'SELL EXECUTED - -- Price: {order.executed.price: .2f},
    #             #          Cost: {order.executed.value: .2f}, Commission: {order.executed.comm: .2f}')
    #             # 报告失败订单
    #     elif order.status in [order.Canceled, order.Margin,
    #                           order.Rejected]:
    #         self.log('Order Failed')
    #     # 现在没有未决订单了
    #     self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(
            f'OPERATION RESULT --- Gross: {trade.pnl:.2f}, Net: {trade.pnlcomm:.2f}')

    def next(self):
        # 如果有未决订单，则无动作，不再生成新订单
        # if self.order:
        #     return

        if not self.position:
            # 如果预测明天会涨，就买
            if (self.data_predicted > 0.5) & (self.data_predicted[-1] > 0.5) :
                # 全仓买入 ('all-in') self.broker.getcash() / self.datas[0].open
                size = int(3)
                # buy order
                # self.log(f'BUY CREATED - -- Size: {size}, Cash: {self.broker.getcash(): .2f},
                #          Open: {self.data_open[0]}, Close: {self.data_close[0]}')
                self.order = self.buy(size=size)
        else:
            # 如果预测明天会跌，就卖
            if (self.data_predicted < 0.5) & (self.data_predicted[-1] < 0.5):
                # sell order
                self.log(f'SELL CREATED --- Size: {self.position.size}')
                self.order = self.sell(size=self.position.size)


class GenericCSV_TAG(bt.feeds.GenericCSVData):

    # Add a 'pe' line to the inherited ones from the base class
    lines = ('predicted',)
    # openinterest in GenericCSVData has index 7 ... add 1
    # add the parameter to the parameters inherited from the base class
    params = (('predicted', 9),)


df = '/Users/zed/AI_Lab/DoubleEnsembleML/src/pred.csv'
data = GenericCSV_TAG(dataname=df,
                      datetime=0,  # 日期行所在列
                      open=5,  # 开盘价所在列
                      high=1,  # 最高价所在列
                      low=2,  # 最低价所在列
                      close=3,  # 收盘价价所在列
                      volume=4,  # 成交量所在列
                      predicted=21,
                      # 无未平仓量列.(openinterest是期货交易使用的)
                               openinterest=-1,
                               # 日l期格式
                               dtformat=('%Y-%m-%d'),
                               fromdate=datetime(2014, 3, 8),  # 起始日
                               todate=datetime(2021, 3, 8))
cerebro = bt.Cerebro()
cerebro.adddata(data)  # 将行情数据对象注入引擎
cerebro.addstrategy(MLStrategy)  # 将策略注入引擎
cerebro.broker.setcash(10000.0)  # 设置初始资金
cerebro.broker.setcommission(commission=0.003)
cerebro.run()

print('最终市值: %.2f' % cerebro.broker.getvalue())

# cerebro.plot(style='bar')

fig = cerebro.plot(style='candlestick')
show = fig[0][0]
show.set_size_inches(20, 10)  # 调整大小
show.savefig("backtest_double_lgr.png", width=16, height=9, dpi=300)
