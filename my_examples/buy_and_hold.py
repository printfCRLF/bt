

if __name__ == "__main__":


    import numpy as np 
    import pandas as pd

    import ffn

    import sys
    import os

    # from bt2 import Backtest, Strategy, run
    # from bt2.algos import RunOnce, Rebalance

    sys.path.append(os.path.abspath("./"))
    print(sys.path)
    # from bt2 import Backtest, Strategy, run
    # from bt2.algos import RunOnce, Rebalance
    import bt2

    # names = ['foo','bar','rf']
    names = ['foo']
    dates = pd.date_range(start='2017-01-01',end='2017-12-31', freq=pd.tseries.offsets.BDay())
    n = len(dates)
    rdf = pd.DataFrame(
        np.zeros((n, len(names))),
        index = dates,
        columns = names
    )

    np.random.seed(1)
    rdf['foo'] = np.random.normal(loc = 0.1/n,scale=0.2/np.sqrt(n),size=n)
    # rdf['bar'] = np.random.normal(loc = 0.04/n,scale=0.05/np.sqrt(n),size=n)
    # rdf['rf'] = np.random.normal(loc=0.02/ n, scale=0.01 / np.sqrt(n), size=n)

    pdf = 100*np.cumprod(1+rdf)

    buy_and_hold = bt2.Strategy("buy_and_hold",
        [
            bt2.algos.RunOnce(),
            bt2.algos.SelectAll(),
            bt2.algos.WeighEqually(),
            bt2.algos.Rebalance()
        ]
    )

    backtest = bt2.Backtest(buy_and_hold, pdf)

    res = bt2.run(backtest)
    print(res.stats)


