import datetime
import gdax


def trade1(arr, budget):
    start_budget = budget
    shares = 0
    diff = 0.05
    start_idx = len(arr)-1
    # pick up the average value of this day as the start value.
    start_value = (arr[start_idx][1] + arr[start_idx][2]) / 2
    point_buy = start_value * (1 - diff)
    point_sel = None

    for i in range(len(arr)-2, -1, -1):
        elem = arr[i]
        ts, low, high, open, close, volume = elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]
        ts_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        # print(ts_str, low, high, volume)

        if point_buy is not None:
            if low <= point_buy:
                point_sel = point_buy * (1 + diff)
                shares = budget / point_sel
                print('{} buy at {}, shoot for sell at {}'.format(ts_str, point_buy, point_sel))
                budget = 0
                point_buy = None

        if point_sel is not None:
            if high >= point_sel:
                print('{} sold at {}'.format(ts_str, point_sel))
                budget = shares * point_sel
                shares = 0
                point_buy = (low + high) / 2 * (1 - diff)
                point_sel = None

    if shares > 0:
        print('${} ==> {} shares = ${}'.format(start_budget, shares, close * shares))
    else:
        print('${} ==> ${}'.format(start_budget, budget))



# main
public_client = gdax.PublicClient()
arr = public_client.get_product_historic_rates('BTC-USD', granularity=3600)
res = trade1(arr, 100.0)
