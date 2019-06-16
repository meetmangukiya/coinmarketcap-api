# CoinMarketCap-API

## Installation

1. From source
   `python setup.py install`

## Usage

```py
from coinmarketcap_api import CoinMarketCap

# create the client, pass API key as the argument
market = CoinMarketCap('7194abc4-3278-4226-be13-85d995af8af9')
```

### Cryptocurrency

```py
# get ID map of cryptocurrencies on coinmarketcap
idmap = market.crypto.idmap(
    listing_status=market.crypto.ACTIVE,    # can be ACTIVE or INACTIVE
                                            #
    start=3,                                # means page number 3
                                            #
    limit=50,                               # indicates page size, so this will get page 3 of size 50
)

# get ID map of particular cryptocurrencies
idmap = market.crypto.idmap(
    symbol=['BTC', 'BCH', 'ETH', 'ETC'] # pass a list of symbols of cryptocurrencies whose idmap is needed
)

# get info of cryptocurrencies using coinmarketcap IDs
info = market.crypto.info(
    ids=[4, 245, 2341],
)

# get info of cryptocurrencies using slugs
info = market.crypto.info(
    slug=['bitcoin', 'bitcoin-cash'],
)

# get info of cryptocurrencies using symbols
info = market.crypto.info(
    symbol=['BTC', 'BCH', 'ETH'],
)

# list cryptocurrencies on coinmarketcap
currencies = market.crypto.list(
    start=3,                                    # means page number 3
                                                #
    limit=50,                                   # of size 50
                                                #
    convert=['BTC', 'BTH', 'USD'],              # include a quote for conversion to these currencies,
                                                # use `convert_id` argument instead if you want to use
                                                # coinmarketcap IDs instead
                                                #
    sort_by='name',                             # could sort by number of attributes, check source or API docs
                                                #
    sort_dir=market.crypto.ASCENDING,           # market.crypto.ASCENDING or market.crypto.DESCENDING
                                                #
    cryptocurrency_type=market.crypto.TOKENS    # market.crypto.ALL, market.crypto.TOKENS or market.crypto.COINS
)

# get quotes
quotes = market.crypto.quotes(
    symbol=['BTC', 'BCH', 'ETH'],   # cryptocurrencies whose quotes are needed,
                                    # could specify them using coinmarketcap IDs using `ids` argument instead
                                    # and using slugs by using `slug` argument
                                    #
    convert=['BTC', 'USD']          # currencies to which we want the conversion to be in,
                                    # could specify them using coinmarketcap IDs using `convert_id` argument instead
)
```
