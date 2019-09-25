import requests
import sys
import time
from datetime import datetime


def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    # Convert the price to a floating point number
    return float(response_json[0]['price_usd'])


def post_ifttt_webhook(event, value):
    # The payload that will be sent to IFTTT service
    data = {'value1': value}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(
        event)  # Inserts our desired event
    # Sends a HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)


def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24.02.2018 15:09'
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        # <b> (bold) tag creates bolded text
        row = '{}: $<b>{}</b>'.format(date, price)
        # 24.02.2018 15:09: $<b>10123.4</b>
        # Use a <br> (break) tag to create a new line return
        rows.append(row)
        # Join the rows delimited by <br> tag: row1<br>row2<br>row3
        '<br>'.join(rows)


def main():
    bitcoin_history = []
    while True:
        print("THRESHOLD set to", BITCOIN_PRICE_THRESHOLD)
        print("Checking bitcoin price..")
        price = get_latest_bitcoin_price()
        date = datetime.now()
        # Send an emergency notification
        bitcoin_history.append({'date': date, 'price': price})
        if price < BITCOIN_PRICE_THRESHOLD:
            print(price, 'dropped')
#            post_ifttt_webhook('bitcoin_price_emergency', price)
#        # Send a ifttt notification when we have 5 items in history
#        if len(bitcoin_history) == 5:
#            post_ifttt_webhook('bitcoin_price_update',
#                               format_bitcoin_history(bitcoin_history))
#            # Reset the history
#            bitcoin_history = []
#            # Sleep for 5 minutes
#            time.sleep(5 * 60)
        else:
            print("still high...")
        time.sleep(5)


if __name__ == '__main__':
    try:
        price = sys.argv[1] if len(sys.argv) > 1 else 0
    finally:
        BITCOIN_PRICE_THRESHOLD = price or 8400
    BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
    # IFTTT_WEBHOOKS_URL = \
    #    'https://maker.ifttt.com/trigger/{}/with/key/{your-IFTTT-key}'
    main()
