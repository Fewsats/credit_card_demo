## Automatic Credit Card purchases with Fewsats SDK


```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  CLI for interacting with L402 services

Options:
  --help  Show this message and exit.

Commands:
  check-payment  Check payment status (placeholder)
  check-weather  Check weather for a location
  create-user    Create a new user
```


Create a new user (Weather API)

```
$ python main.py create-user                                
New UserID: c675d44c-2448-450f-afa8-5090f43f189c
```

Check the weather for a given location and purchase 
```
# With credits
$ python main.py check-weather --user-id=c675d44c-2448-450f-afa8-5090f43f189c [--location="vancouver"]
{'temperature': 6.7, 'condition': 'Light rain', 'location': 'San Francisco, United States of America', 'humidity': 82, 'wind_kph': 23.8, 'feels_like': 2.8, 'last_updated': '2025-03-14 08:45'}

# Without credits
$ python main.py check-weather --user-id=c675d44c-2448-450f-afa8-5090f43f189c 
No credits left and no API key provided
```

Purchase credits if needed

```
# Purchase credits automatically ($5.00 using CC)
python main.py check-weather --user-id=c675d44c-2448-450f-afa8-5090f43f189c --location=vancouver --api-ke
y=$FEWSATS_API_KEY
{'id': 429, 'created_at': '2025-03-14T16:00:37.307Z', 'status': 'pending', 'payment_method': 'credit_card'}
```

Check the payment status
```
$ python main.py check-payment --payment-id=429 --api-key=FEWSATS_API_KEY
{'id': 429, 'created_at': '2025-03-14T16:00:37.307Z', 'status': 'pending', 'payment_request_url': 'https://api.fewsats.com/v0/l402/payment-request', 'payment_context_token': '9b08d1e9-cca8-409e-ac16-2076c0c98af3', 'invoice': '', 'preimage': '', 'amount': 500, 'currency': 'usd', 'payment_method': 'credit_card', 'title': '1000 credit package', 'description': 'Add 1000 credits to your account.', 'type': 'one-off', 'is_test': False}
```

Credit cart payments can take multiple minutes to precess. We recomend polling every 30 seconds/1 minute

