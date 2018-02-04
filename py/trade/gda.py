import gdax
import sys

key = sys.argv[1]
sec = sys.argv[2]
psw = sys.argv[3]


def transactions():
    order = auth_client.sell(price='190.00', size='1', product_id='LTC-USD')
    print(order)

    order = auth_client.sell(price='0.019', size='5', product_id='LTC-BTC')
    print(order)

    order = auth_client.buy(price='9000', size='0.2', product_id='BTC-USD')
    print(order)

    order = auth_client.buy(price='155', size='10', product_id='LTC-USD')
    print(order)

    order = auth_client.sell(price='300.00', size='1', product_id='LTC-USD')
    print(order)


auth_client = gdax.AuthenticatedClient(key, sec, psw)

accounts = auth_client.get_accounts()

for a in accounts:
    print(a['id'], a['currency'], a['balance'], a['available'])

orders = auth_client.get_orders()
for order in orders:
    for elem in order:
        print(elem['id'])
        print(elem)
