from urllib.parse import urljoin

import requests


class CoinMarketCapError(Exception):
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code


class CoinMarketCap:
    def __init__(self, api_key, sandbox=False):
        self._api_key = api_key
        self._session = requests.Session()
        self._session.headers.update({'X-CMC_PRO_API_KEY': self._api_key})
        self._credit_count = None
        self._base_url = 'https://pro-api.coinmarketcap.com' if not sandbox else 'https://sandbox-api.coinmarketcap.com'

        self.crypto = CoinMarketCapCryptocurrency(self)

    @property
    def credit_count(self):
        return self._credit_count

    def _request(self, method, endpoint, *args, **kwargs):
        url = urljoin(self._base_url, endpoint)

        if method == 'get':
            res = self._session.get(url, *args, **kwargs)
        elif method == 'post':
            res = self._session.post(url, *args, **kwargs)

        status = res.json()['status']

        self._credit_count = status['credit_count']

        if status['error_code'] != 0:
            raise CoinMarketCapError(status['error_message'],
                    status['error_code'])

        return res.json()

    def _get(self, endpoint, *args, **kwargs):
        return self._request('get', endpoint, *args, **kwargs)

    def _post(self, endpoint, *args, **kwargs):
        return self._request('post', endpoint, *args, **kwargs)


class CoinMarketCapCryptocurrency:
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    ASCENDING = 'asc'
    DESCENDING = 'desc'

    ALL = 'all'
    TOKENS = 'tokens'
    COINS = 'coins'

    def __init__(self, client):
        self._client = client

    def _list_to_comma_separated(self, ls):
        return ','.join(map(lambda x: str(x), ls)) if isinstance(ls, list) else str(ls)

    def idmap(self, listing_status=ACTIVE, start=1, limit=None, symbol=None):
        """
        Get ID map of cryptocurrencies.

        :param listing_status:
            Either of ``CoinMarketCapCryptocurrency.ACTIVE`` or
            ``CoinMarketCapCryptocurrency.INACTIVE``
        :param start:
            1-based index indicating the page number.
        :param limit:
            Number of results, used alongside ``start`` to implement paginated
            results.
        :param symbol:
            A single symbol or list of symbols to get the ID map of.
        """

        params = {
            'listing_status': listing_status,
            'start': start,
            'limit': limit,
            'symbol': self._list_to_comma_separated(symbol),
        }

        return self._client._get('/v1/cryptocurrency/map', params=params)

    def info(self, ids=None, slug=None, symbol=None):
        """
        Get info of cryptocurrencies.

        :param ids:
            Single id or a list of ids to get the info of. This is the
            CoinMarketCap ID for that particular cryptocurrency.
        :param slug:
            Single slug or a list of slugs of cryptocurrencies.
        :param symbol:
            Single symbol or a list of symbols of cryptocurrencies to get info
            of.
        """

        if ids is None and slug is None and symbol is None:
            raise CoinMarketCapError('Either of id, slug or symbol should be provided')

        params = {
            'id': ','.join(ids) if isinstance(ids, list) else ids,
            'slug': ','.join(slug) if isinstance(slug, list) else slug,
            'symbol': self._list_to_comma_separated(symbol),
        }

        return self._client._get('/v1/cryptocurrency/info', params=params)

    def list(self, start=1, limit=None, convert=None, convert_id=None,
            sort_by='market_cap', sort_dir=ASCENDING, cryptocurrency_type=ALL):
        """
        List cryptocurrencies.

        :param start:
            1-based index indicating page number.
        :param limit:
            Number of results, used alongside start to implement pagination.
        :param convert:
            List of symbols of currencies to get the quote of currencies in.
        :param convert_id:
            List of ids of cryptocurrencies to get the quote of currencies in.
        :param sort_by:
            Field to sort the results by. Either of ['name', 'symbol',
                'date_added', 'market_cap', 'market_cap_strict', 'price',
                'circulating_supply', 'total_supply', 'max_supply',
                'num_market_pairs', 'volume_24h', 'percent_change_1h',
                'percent_change_24h', 'percent_change_7d']
        :param sort_dir:
            Either of ``CoinMarketCapCryptocurrency.ASCENDING`` or
            ``CoinMarketCapCryptocurrency.DESCENDING``
        :param cryptocurrency_type:
            Either of ``CoinMarketCapCryptocurrency.ALL``,
            ``CoinMarketCapCryptocurrency.TOKENS`` or
            ``CoinMarketCapCryptocurrency.COINS``
        """

        params = {
            'start': start,
            'limit': limit,
            'convert': self._list_to_comma_separated(convert),
            'convert_id': self._list_to_comma_separated(convert_id),
            'sort': sort_by,
            'sort_dir': sort_dir,
            'cryptocurrency_type': cryptocurrency_type,
        }

        return self._client._get('/v1/cryptocurrency/listings/latest',
                params=params)

    def quotes(self, ids=None, slug=None, symbol=None, convert=None,
            convert_id=None):
        if ids is None and slug is None and symbol is None:
            raise CoinMarketCapError('Either of the ids, slug or symbol should be provided')
        if convert is None and convert_id is None:
            raise CoinMarketCapError('Either of the convert or convert_id has to be provided')

        params = {
            'id': self._list_to_comma_separated(ids),
            'slug': self._list_to_comma_separated(slug),
            'symbol': self._list_to_comma_separated(symbol),
            'convert': self._list_to_comma_separated(convert),
            'convert_id': self._list_to_comma_separated(convert_id),
        }

        return self._client._get('/v1/cryptocurrency/quotes/latest',
                params=params)
