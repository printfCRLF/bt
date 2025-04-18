"""
Performance benchmarks
"""
import numpy as np
import pandas as pd
import bt2
import cProfile


def benchmark_1():
    x = np.random.randn(10000, 1000) * 0.01
    idx = pd.date_range("1990-01-01", freq="B", periods=x.shape[0])
    data = np.exp(pd.DataFrame(x, index=idx).cumsum())

    s = bt2.Strategy(
        "s",
        [
            bt2.algos.RunMonthly(),
            bt2.algos.SelectRandomly(len(data.columns) / 2),
            bt2.algos.WeighRandomly(),
            bt2.algos.Rebalance(),
        ],
    )

    t = bt2.Backtest(s, data)
    return bt2.run(t)


def benchmark_2():
    x = np.random.randn(10000, 1000) * 0.01
    idx = pd.date_range("1990-01-01", freq="B", periods=x.shape[0])
    data = np.exp(pd.DataFrame(x, index=idx).cumsum())
    bidoffer = data * 0.01
    coupons = data * 0.0
    s = bt2.FixedIncomeStrategy(
        "s",
        algos=[
            bt2.algos.RunMonthly(),
            bt2.algos.SelectRandomly(len(data.columns) / 2),
            bt2.algos.WeighRandomly(),
            bt2.algos.Rebalance(),
        ],
        children=[bt2.CouponPayingSecurity(c) for c in data],
    )

    t = bt2.Backtest(s, data, additional_data={"bidoffer": bidoffer, "coupons": coupons})
    return bt2.run(t)


def benchmark_3():
    # Similar to benchmark_1, but with trading in only a small subset of assets
    # However, because the "multipier" is used, we can't just pass the string
    # names to the constructor, and so the solution is to use the lazy_add flag.
    # Changing lazy_add to False demonstrates the performance gain.
    # i.e. on Win32, it went from 4.3s with the flag to 10.9s without.

    x = np.random.randn(10000, 1000) * 0.01
    idx = pd.date_range("1990-01-01", freq="B", periods=x.shape[0])
    data = np.exp(pd.DataFrame(x, index=idx).cumsum())
    children = [bt2.Security(name=i, multiplier=10, lazy_add=False) for i in range(1000)]
    s = bt2.Strategy(
        "s",
        [
            bt2.algos.RunMonthly(),
            bt2.algos.SelectThese([0, 1]),
            bt2.algos.WeighRandomly(),
            bt2.algos.Rebalance(),
        ],
        children=children,
    )

    t = bt2.Backtest(s, data)
    return bt2.run(t)


if __name__ == "__main__":
    print("\n\n\n================= Benchmark 1 =======================\n")
    cProfile.run("benchmark_1()", sort="tottime")
    print("\n----------------- Benchmark 1 -----------------------\n\n\n")

    print("\n\n\n================= Benchmark 2 =======================\n")
    cProfile.run("benchmark_2()", sort="tottime")
    print("\n----------------- Benchmark 2 -----------------------\n\n\n")

    print("\n\n\n================= Benchmark 3 =======================\n")
    cProfile.run("benchmark_3()", sort="cumtime")
    print("\n----------------- Benchmark 3 -----------------------\n\n\n")
