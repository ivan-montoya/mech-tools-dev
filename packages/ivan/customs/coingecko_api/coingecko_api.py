import requests
from typing import Any, Dict, Optional, Tuple, List, Callable
import os
import functools


class CoingeckoAPI:
    def __init__(self, api_key: str):
        self.coingecko_api_key = api_key

    # Ping API endpoint definitions

    def check_api_server_status(self) -> str:
        """
        This endpoint allows you to check the API server status.

        Returns:
            str: JSON response containing API server status
        """
        url = "https://api.coingecko.com/api/v3/ping"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    # Simple API endpoint definitions

    def coin_price_by_id(self, query_params: Optional[dict[Any, Any]] = None) -> str:
        base_url = "https://api.coingecko.com/api/v3/simple/price"
        if query_params is not None:
            url = f"{base_url}?" + "&".join(f"{k}={v}" for k, v in query_params.items())
        else:
            url = base_url

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)
        return response.json()

    def coin_price_by_token_address(
        self,
        id: str,
        contract_addresses: str,
        vs_currencies: str,
        include_market_cap: bool = False,
        include_24hr_vol: bool = False,
        include_24hr_change: bool = False,
        include_last_updated_at: bool = False,
        precision: Optional[str] = None,
    ) -> str:
        """
        Get the price of one or more tokens by their contract addresses.

        Args:
            id: The id of the platform (e.g. ethereum)
            contract_addresses: Token's contract address, comma-separated if querying more than 1 token
            vs_currencies: Target currency of tokens, comma-separated if querying more than 1 currency.
                Refers to /simple/supported_vs_currencies
            include_market_cap: Include market cap. Default: False
            include_24hr_vol: Include 24hr volume. Default: False
            include_24hr_change: Include 24hr change. Default: False
            include_last_updated_at: Include last updated price time in UNIX. Default: False
            precision: Decimal place for currency price value

        Returns:
            str: Price information for the requested tokens
        """
        base_url = "https://api.coingecko.com/api/v3/simple/token_price"

        params = {      
            "contract_addresses": contract_addresses,
            "vs_currencies": vs_currencies
        }

        if include_market_cap:
            params["include_market_cap"] = "true"
        if include_24hr_vol:
            params["include_24hr_vol"] = "true"
        if include_24hr_change:
            params["include_24hr_change"] = "true"
        if include_last_updated_at:
            params["include_last_updated_at"] = "true"
        if precision is not None:
            params["precision"] = precision
        
        url = f"{base_url}/{id}?" + "&".join(f"{k}={v}" for k, v in params.items())

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)
        return response.json()


    def supported_currencies_list(self) -> str:
        """
        Get list of supported vs currencies.
        
        Returns a list of all supported vs/comparison currencies available on CoinGecko.
        These are the currencies that can be used in price conversions and comparisons.
        For example: usd, eur, jpy, etc.
        
        Returns:
            str: JSON response containing array of supported currency codes
        """
        url = "https://api.coingecko.com/api/v3/simple/supported_vs_currencies"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    # Coin API endpoint definitions

    def coins_list(self, include_platform: bool = False) -> str:
        """
        Get the list of coins.

        Args:
            include_platform: If True, includes platform and token's contract addresses. Defaults to False.
        """
        base_url = "https://api.coingecko.com/api/v3/coins/list"

        if include_platform:
            url = f"{base_url}?include_platform=true"
        else:
            url = base_url

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()


    def coins_list_with_market_data(
        self,
        vs_currency: str,
        ids: Optional[str] = None,
        category: Optional[str] = None,
        order: str = "market_cap_desc",
        per_page: int = 100,
        page: int = 1,
        sparkline: bool = False,
        price_change_percentage: Optional[str] = None,
        locale: str = "en",
        precision: Optional[str] = None
    ) -> str:
        """
        Get the list of coins with market data.

        Args:
            vs_currency: Target currency for coin prices and market data (from /simple/supported_vs_currencies)
            ids: Comma-separated coin IDs to query (from /coins/list)
            category: Filter coins by category (from /coins/categories/list)
            order: Sort results by field (default: market_cap_desc)
            per_page: Number of results per page, 1-250 (default: 100)
            page: Page number for pagination (default: 1)
            sparkline: Include 7-day sparkline data (default: False)
            price_change_percentage: Comma-separated timeframes for price change data (1h,24h,7d,14d,30d,200d,1y)
            locale: Language/locale for response (default: en)
            precision: Decimal places for currency price values
        
        Returns:
            str: JSON response containing coin market data
        """
        base_url = "https://api.coingecko.com/api/v3/coins/markets"

        params = {
            "vs_currency": vs_currency
        }

        if ids is not None:
            params["ids"] = ids.replace(",", "%2C")
        if category is not None:
            params["category"] = category
        if order is not None:
            params["order"] = order
        if per_page is not None:
            params["per_page"] = per_page
        if page is not None:
            params["page"] = page
        if sparkline:
            params["sparkline"] = "true"
        if price_change_percentage is not None:
            params["price_change_percentage"] = price_change_percentage
        if locale is not None:
            params["locale"] = locale
        if precision is not None:
            params["precision"] = precision

        url = f"{base_url}?" + "&".join(f"{k}={v}" for k, v in params.items())

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()


    def coin_data_by_id(
        self,
        id: str,
        localization: bool = True,
        tickers: bool = True,
        market_data: bool = True,
        community_data: bool = True,
        developer_data: bool = True,
        sparkline: bool = False
    ) -> str:
        """
        Get current data for a coin.

        Args:
            id: The coin id (from /coins/list)
            localization: Include all localized languages in response (default: True)
            tickers: Include tickers data (default: True)
            market_data: Include market data (default: True)
            community_data: Include community data (default: True)
            developer_data: Include developer data (default: True)
            sparkline: Include 7 day sparkline data (default: False)

        Returns:
            str: JSON response containing coin data
        """
        base_url = f"https://api.coingecko.com/api/v3/coins/{id}"

        params = {
            "localization": str(localization).lower(),
            "tickers": str(tickers).lower(),
            "market_data": str(market_data).lower(),
            "community_data": str(community_data).lower(),
            "developer_data": str(developer_data).lower(),
            "sparkline": str(sparkline).lower()
        }

        url = f"{base_url}?" + "&".join(f"{k}={v}" for k, v in params.items())


        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()


    def coin_tickers_by_id(
        self,
        id: str,
        exchange_ids: Optional[str] = None,
        include_exchange_logo: bool = False,
        page: Optional[int] = None,
        order: str = "trust_score_desc",
        depth: bool = False
    ) -> str:
        """
        Get coin tickers (paginated to 100 items).

        Args:
            id: The coin id (from /coins/list)
            exchange_ids: Filter results by exchange ids (from /exchanges/list)
            include_exchange_logo: Include exchange logo in response (default: False)
            page: Page through results
            order: Sort results by field (default: "trust_score_desc")
            depth: Include 2% orderbook depth data - cost to move up/down (default: False)

        Returns:
            str: JSON response containing coin tickers data
        """
        base_url = f"https://api.coingecko.com/api/v3/coins/{id}/tickers"

        params = {}

        if exchange_ids is not None:
            params["exchange_ids"] = exchange_ids
        if include_exchange_logo:
            params["include_exchange_logo"] = "true"
        if page is not None:
            params["page"] = page
        if order is not None:
            params["order"] = order
        if depth:
            params["depth"] = "true"

        url = f"{base_url}?" + "&".join(f"{k}={v}" for k, v in params.items())

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()  

    def coin_historical_data_by_id(
        self,
        id: str,
        date: str,
        localization: bool = True
    ) -> str:
        """
        Get historical data (name, price, market, stats) at a given date for a coin.

        Args:
            id: The coin id (refers to /coins/list)
            date: The date of data snapshot in dd-mm-yyyy format
            localization: Include all localized languages in response (default: True)

        Returns:
            str: JSON response containing historical coin data
        """
        base_url = f"https://api.coingecko.com/api/v3/coins/{id}/history"

        url = f"{base_url}?date={date}&localization={str(localization).lower()}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()  

    def coin_historical_chart_data_by_id(self, path_params: dict[Any, Any], query_params: dict[Any, Any]) -> str:
        base_url = f"https://api.coingecko.com/api/v3/coins/{path_params['id']}/market_chart"

        url = f"{base_url}?vs_currency={query_params['vs_currency']}&days={query_params['days']}"

        if interval is not None:
            url = f"{url}&interval={interval}"
        if precision is not None:
            url = f"{url}&precision={precision}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def coin_historical_chart_data_within_time_range_by_id(
        self,
        id: str,
        vs_currency: str, 
        from_timestamp: int,
        to_timestamp: int,
        precision: Optional[str] = None
    ) -> str:
        """
        Get historical market data including price, market cap, and 24h volume within a specific time range.

        Args:
            id: The coin id (refers to /coins/list)
            vs_currency: The target currency of market data (refers to /simple/supported_vs_currencies)
            from_timestamp: Starting date in UNIX timestamp
            to_timestamp: Ending date in UNIX timestamp
            precision: Decimal place for currency price value

        Returns:
            str: JSON response containing historical market data
        """
        base_url = f"https://api.coingecko.com/api/v3/coins/{id}/market_chart/range"

        url = f"{base_url}?vs_currency={vs_currency}&from={from_timestamp}&to={to_timestamp}"

        if precision is not None:
            url = f"{url}&precision={precision}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }   

        response = requests.get(url, headers=headers)

        return response.json()

    def coin_ohlc_chart_by_id(
        self,
        id: str,
        vs_currency: str,
        days: str,
        precision: Optional[str] = None
    ) -> str:
        """
        Get OHLC (Open/High/Low/Close) data for a coin.

        Args:
            id: The coin id (refers to /coins/list)
            vs_currency: Target currency of price data (refers to /simple/supported_vs_currencies)
            days: Data up to number of days ago
            precision: Decimal place for currency price value

        Returns:
            str: JSON response containing OHLC data
        """
        base_url = f"https://api.coingecko.com/api/v3/coins/{id}/ohlc"

        url = f"{base_url}?vs_currency={vs_currency}&days={days}"

        if precision is not None:
            url = f"{url}&precision={precision}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    # Contract API endpoint definitions

    def coin_data_by_token_address(
        self,
        id: str,
        contract_address: str
    ) -> str:
        """
        Get the data of a coin by its token address.

        Args:
            id: Asset platform id (refers to /asset_platforms)
            contract_address: The contract address of token

        Returns:
            str: JSON response containing coin data
        """
        url = f"https://api.coingecko.com/api/v3/coins/{id}/contract/{contract_address}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def coin_historical_chart_data_by_token_address(
        self,
        id: str,
        contract_address: str,
        vs_currency: str,
        days: str,
        interval: str = None,
        precision: str = None
    ) -> str:
        """
        Get the historical chart data of a coin by its token address.

        Args:
            id: Asset platform id (refers to /asset_platforms)
            contract_address: The contract address of token
            vs_currency: Target currency of market data (refers to /simple/supported_vs_currencies)
            days: Data up to number of days ago (any integer)
            interval: Data interval, leave empty for auto granularity. Possible value: daily
            precision: Decimal place for currency price value

        Returns:
            str: JSON response containing historical chart data
        """
        base_url = f"https://api.coingecko.com/api/v3/coins/{id}/contract/{contract_address}/market_chart"

        url = f"{base_url}?vs_currency={vs_currency}&days={days}"

        if interval is not None:
            url = f"{url}&interval={interval}"
        if precision is not None:
            url = f"{url}&precision={precision}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def coin_historical_chart_data_within_time_range_by_token_address(
        self,
        id: str,
        contract_address: str,
        vs_currency: str,
        from_timestamp: int,
        to_timestamp: int,
        precision: str = None
    ) -> str:
        """
        Get the historical chart data of a coin by its token address within a time range.

        Args:
            id: Asset platform id (refers to /asset_platforms)
            contract_address: The contract address of token
            vs_currency: Target currency of market data (refers to /simple/supported_vs_currencies)
            from_timestamp: Starting date in UNIX timestamp
            to_timestamp: Ending date in UNIX timestamp
            precision: Decimal place for currency price value

        Returns:
            str: JSON response containing historical chart data
        """
        base_url = f"https://api.coingecko.com/api/v3/coins/{id}/contract/{contract_address}/market_chart/range"

        url = f"{base_url}?vs_currency={vs_currency}&from={from_timestamp}&to={to_timestamp}"

        if precision is not None:
            url = f"{url}&precision={precision}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    # Asset Platform API endpoint definitions   

    def asset_platforms_list(
        self,
        filter: str = None
    ) -> str:
        """
        Get the list of asset platforms.

        Args:
            filter: String to filter results by platform name or other attributes

        Returns:
            str: JSON response containing filtered list of asset platforms
        """
        base_url = "https://api.coingecko.com/api/v3/asset_platforms"

        if filter is not None:
            url = f"{base_url}?filter={filter}"
        else:
            url = base_url

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    # Categories API endpoint definitions

    def coins_categories_list(self) -> str:
        """
        Get the list of all cryptocurrency categories.

        Returns:
            str: JSON response containing list of all cryptocurrency categories including
                category name and category ID
        """
        url = "https://api.coingecko.com/api/v3/coins/categories/list"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def coins_categories_list_with_market_data(
        self,
        order: str = "market_cap_desc"
    ) -> str:
        """
        Get the list of coins categories with market data.

        Args:
            order: String to sort results by field, default: market_cap_desc

        Returns:
            str: JSON response containing list of coins categories with market data
        """

        url = "https://api.coingecko.com/api/v3/coins/categories"

        if order is not None:
            url = f"{url}?order={order}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    # Exchanges API endpoint definitions

    def exchanges_list_with_data(
        self,
        per_page: int = 100,
        page: int = 1
    ) -> str:
        """
        Get the list of exchanges with data.

        Args:
            per_page: Total results per page (1-250), default: 100
            page: Page through results, default: 1

        Returns:
            str: JSON response containing list of exchanges with data
        """
        base_url = "https://api.coingecko.com/api/v3/exchanges"

        params = {}

        if per_page is not None:
            params["per_page"] = str(per_page)
        if page is not None:
            params["page"] = str(page)

        url = f"{base_url}?" + "&".join(f"{k}={v}" for k, v in params.items())

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def exchanges_list(
        self,
        status: str = "active"
    ) -> str:
        """
        Get the list of exchanges.

        Args:
            status: Filter by status of exchanges, default: active

        Returns:
            str: JSON response containing list of exchanges
        """
        url = f"https://api.coingecko.com/api/v3/exchanges/list?status={status}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def exchange_data_by_id(
        self,
        id: str
    ) -> str:
        """
        Get the data of an exchange by its ID.

        Args:
            id: Exchange ID (refers to /exchanges/list)

        Returns:
            str: JSON response containing exchange data
        """
        url = f"https://api.coingecko.com/api/v3/exchanges/{id}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def exchange_tickers_by_id(
        self,
        id: str,
        coin_ids: str = None,
        include_exchange_logo: bool = False,
        page: int = None,
        depth: bool = False,
        order: str = "trust_score_desc"
    ) -> str:
        """
        Get the tickers of an exchange by its ID.

        Args:
            id: Exchange ID (refers to /exchanges/list)
            coin_ids: Filter tickers by coin_ids, comma-separated if querying more than 1 coin (refers to /coins/list)
            include_exchange_logo: Include exchange logo, default: false
            page: Page through results
            depth: Include 2% orderbook depth (cost_to_move_up_usd & cost_to_move_down_usd), default: false
            order: Sort order of responses, default: trust_score_desc

        Returns:
            str: JSON response containing exchange tickers
        """
        base_url = f"https://api.coingecko.com/api/v3/exchanges/{id}/tickers"

        params = {}

        if coin_ids is not None:
            params["coin_ids"] = coin_ids.replace(",", "%2C")
        if include_exchange_logo is not None:
            params["include_exchange_logo"] = str(include_exchange_logo).lower()
        if page is not None:
            params["page"] = str(page)
        if depth is not None:
            params["depth"] = str(depth).lower()
        if order is not None:
            params["order"] = order

        url = f"{base_url}?" + "&".join(f"{k}={v}" for k, v in params.items())

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def exchange_volume_chart_by_id(
        self,
        id: str,
        days: str
    ) -> str:
        """
        Get the volume chart of an exchange by its ID.

        Args:
            id: Exchange ID or derivatives exchange ID (refers to /exchanges/list or /derivatives/exchanges/list)
            days: Data up to number of days ago

        Returns:
            str: JSON response containing exchange volume chart data
        """
        url = f"https://api.coingecko.com/api/v3/exchanges/{id}/volume_chart?days={days}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    # Derivatives API endpoint definitions

    def derivatives_tickers_list(self) -> str:
        """
        Get the list of derivatives tickers including open interest, volume, index price, basis, funding rate, etc.

        Returns:
            str: JSON response containing list of derivatives tickers with market data
        """
        url = "https://api.coingecko.com/api/v3/derivatives"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def derivatives_exchanges_list_with_data(
        self,
        order: str = "open_interest_btc_desc",
        per_page: int = None,
        page: int = 1
    ) -> str:
        """
        Get the list of derivatives exchanges with data.

        Args:
            order: Sort order of responses (default: open_interest_btc_desc)
            per_page: Total results per page
            page: Page through results (default: 1)

        Returns:
            str: JSON response containing list of derivatives exchanges with data
        """

        base_url = "https://api.coingecko.com/api/v3/derivatives/exchanges"

        params = {}

        if order is not None:
            params["order"] = order
        if per_page is not None:
            params["per_page"] = str(per_page)
        if page is not None:
            params["page"] = str(page)

        url = f"{base_url}?" + "&".join(f"{k}={v}" for k, v in params.items())

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def derivatives_exchange_data_by_id(
        self,
        id: str,
        include_tickers: str = None
    ) -> str:
        """
        Get the data of a derivatives exchange by its ID.

        Args:
            id: Derivative exchange ID (refers to /derivatives/exchanges/list)
            include_tickers: Include tickers data

        Returns:
            str: JSON response containing derivatives exchange data
        """
        url = f"https://api.coingecko.com/api/v3/derivatives/exchanges/{id}"

        if include_tickers is not None:
            url = f"{url}?include_tickers={include_tickers}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def derivatives_exchanges_list(self) -> str:
        """
        Get the list of all derivatives exchanges.

        Returns:
            str: JSON response containing list of all derivatives exchanges
        """
        url = "https://api.coingecko.com/api/v3/derivatives/exchanges/list"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    # NFT API endpoint definitions

    def nfts_list(
        self,
        order: str = None,
        per_page: int = None,
        page: int = None
    ) -> str:
        """
        Get the list of all NFTs.

        Args:
            order: Sort order of responses
            per_page: Total results per page (1-250)
            page: Page number through results

        Returns:
            str: JSON response containing list of all NFTs
        """
        base_url = "https://api.coingecko.com/api/v3/nfts/list"

        params = {}

        if order is not None:
            params["order"] = order
        if per_page is not None:
            params["per_page"] = str(per_page)
        if page is not None:
            params["page"] = str(page)

        url = f"{base_url}?" + "&".join(f"{k}={v}" for k, v in params.items())

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def nfts_collection_data_by_id(
        self,
        id: str
    ) -> str:
        """
        Get NFT data by its ID.

        Args:
            id: NFTs id (refers to /nfts/list)

        Returns:
            str: JSON response containing NFT data
        """
        url = f"https://api.coingecko.com/api/v3/nfts/{id}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def nfts_collection_data_by_contract_address(
        self,
        asset_platform_id: str,
        contract_address: str
    ) -> str:
        """
        Get NFT data by contract address.

        Args:
            asset_platform_id: Asset platform id (refers to /asset_platforms)
            contract_address: The contract address of token

        Returns:
            str: JSON response containing NFT data
        """
        url = f"https://api.coingecko.com/api/v3/nfts/{asset_platform_id}/contract/{contract_address}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    # Exchange Rates API endpoint definitions

    def btc_to_currency_exchange_rates(self) -> str:
        """
        Get BTC exchange rates with other currencies.

        Returns:
            str: JSON response containing BTC exchange rates with other currencies
        """
        url = "https://api.coingecko.com/api/v3/exchange_rates"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    # Search API endpoint definitions

    def search_queries(
        self,
        query: str
    ) -> str:
        """
        Search for coins, categories and markets listed on CoinGecko.

        Args:
            query: Search query string (required)

        Returns:
            str: JSON response containing search results
        """
        url = f"https://api.coingecko.com/api/v3/search?query={query}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    # Trending API endpoint definitions

    def trending_search_list(self) -> str:
        """
        Get trending search coins, NFTs and categories on CoinGecko in the last 24 hours.

        Returns:
            str: JSON response containing trending search results
        """
        url = "https://api.coingecko.com/api/v3/search/trending"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    # Global API endpoint definitions

    def crypto_global_market_data(self) -> str:
        """
        Get global cryptocurrency market data including:
        - Total number of active cryptocurrencies
        - Total number of markets
        - Total market capitalization
        - 24h trading volume
        - Market cap percentage by coin
        - Market cap change percentage
        - And other key global metrics

        Returns:
            str: JSON response containing global cryptocurrency market data
        """
        url = "https://api.coingecko.com/api/v3/global"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def global_defi_market_data(self) -> str:
        """
        Get global DeFi market data for the top 100 cryptocurrencies, including total DeFi market 
        capitalization, trading volume, and other key metrics for decentralized finance tokens.

        Returns:
            str: JSON response containing global defi market data
        """
        url = "https://api.coingecko.com/api/v3/global/decentralized_finance_defi"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()  

    # Companies API endpoint definitions

    def public_companies_holdings(
        self,
        coin_id: str
    ) -> str:
        """
        This endpoint allows you query public companies' bitcoin or ethereum holdings.

        Args:
            coin_id (str): The coin ID to query holdings for (e.g. 'bitcoin' or 'ethereum')

        Returns:
            str: JSON response containing public companies' holdings data for the specified coin
        """
        url = f"https://api.coingecko.com/api/v3/companies/public_treasury/{coin_id}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.coingecko_api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()


def error_response(msg: str) -> Tuple[str, None, None, None]:
    """
    Creates a formatted error response tuple.
    
    Args:
        msg: The error message to include
        
    Returns:
        A tuple containing the error message and three None values for prompt, transaction and cost
    """
    return msg, None, None, None


# Command Handlers

    
def handle_check_api_server_status(coingecko_api):
    return coingecko_api.check_api_server_status()

def handle_coin_price_by_id(coingecko_api, **kwargs):
    query_params = kwargs.get("query_params", None)
    return coingecko_api.coin_price_by_id(query_params)

def handle_coin_price_by_token_address(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    contract_addresses = kwargs.get("contract_addresses", None)
    vs_currencies = kwargs.get("vs_currencies", None)
    include_market_cap = kwargs.get("include_market_cap", False)
    include_24hr_vol = kwargs.get("include_24hr_vol", False)
    include_24hr_change = kwargs.get("include_24hr_change", False)
    include_last_updated_at = kwargs.get("include_last_updated_at", False)
    precision = kwargs.get("precision", None)
    return coingecko_api.coin_price_by_token_address(id, contract_addresses, vs_currencies, include_market_cap, include_24hr_vol, include_24hr_change, include_last_updated_at, precision)

def handle_supported_currencies_list(coingecko_api):
    return coingecko_api.supported_currencies_list()

def handle_coins_list(coingecko_api, **kwargs):
    include_platform = kwargs.get("include_platform", False)
    return coingecko_api.coins_list(include_platform)

def handle_coins_list_with_market_data(coingecko_api, **kwargs):
    vs_currency = kwargs.get("vs_currency", None)
    ids = kwargs.get("ids", None)
    category = kwargs.get("category", None)
    order = kwargs.get("order", "market_cap_desc")
    per_page = kwargs.get("per_page", 100)
    page = kwargs.get("page", 1)
    sparkline = kwargs.get("sparkline", False)
    price_change_percentage = kwargs.get("price_change_percentage", None)
    locale = kwargs.get("locale", "en")
    precision = kwargs.get("precision", None)
    return coingecko_api.coins_list_with_market_data(vs_currency, ids, category, order, per_page, page, sparkline, price_change_percentage, locale, precision)

def handle_coin_data_by_id(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    localization = kwargs.get("localization", True)
    tickers = kwargs.get("tickers", True)
    market_data = kwargs.get("market_data", True)
    community_data = kwargs.get("community_data", True)
    developer_data = kwargs.get("developer_data", True)
    sparkline = kwargs.get("sparkline", False)
    return coingecko_api.coin_data_by_id(id, localization, tickers, market_data, community_data, developer_data, sparkline)

def handle_coin_tickers_by_id(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    exchange_ids = kwargs.get("exchange_ids", None)
    include_exchange_logo = kwargs.get("include_exchange_logo", False)
    page = kwargs.get("page", None)
    order = kwargs.get("order", "trust_score_desc")
    depth = kwargs.get("depth", False)
    return coingecko_api.coin_tickers_by_id(id, exchange_ids, include_exchange_logo, page, order, depth)

def handle_coin_historical_data_by_id(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    date = kwargs.get("date", None)
    localization = kwargs.get("localization", True)
    return coingecko_api.coin_historical_data_by_id(id, date, localization)

def handle_coin_historical_chart_data_by_id(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    vs_currency = kwargs.get("vs_currency", None)
    days = kwargs.get("days", None)
    interval = kwargs.get("interval", None)
    precision = kwargs.get("precision", None)
    return coingecko_api.coin_historical_chart_data_by_id(id, vs_currency, days, interval, precision)

def handle_coin_historical_chart_data_within_time_range_by_id(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    vs_currency = kwargs.get("vs_currency", None)
    from_timestamp = kwargs.get("from_timestamp", None)
    to_timestamp = kwargs.get("to_timestamp", None)
    precision = kwargs.get("precision", None)
    return coingecko_api.coin_historical_chart_data_within_time_range_by_id(id, vs_currency, from_timestamp, to_timestamp, precision)

def handle_coin_ohlc_chart_by_id(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    vs_currency = kwargs.get("vs_currency", None)
    days = kwargs.get("days", None)
    precision = kwargs.get("precision", None)
    return coingecko_api.coin_ohlc_chart_by_id(id, vs_currency, days, precision)

def handle_coin_data_by_token_address(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    contract_address = kwargs.get("contract_address", None)
    return coingecko_api.coin_data_by_token_address(id, contract_address)

def handle_coin_historical_chart_data_by_token_address(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    contract_address = kwargs.get("contract_address", None)
    vs_currency = kwargs.get("vs_currency", None)
    days = kwargs.get("days", None)
    interval = kwargs.get("interval", None)
    precision = kwargs.get("precision", None)
    return coingecko_api.coin_historical_chart_data_by_token_address(id, contract_address, vs_currency, days, interval, precision)

def handle_coin_historical_chart_data_within_time_range_by_token_address(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    contract_address = kwargs.get("contract_address", None)
    vs_currency = kwargs.get("vs_currency", None)
    from_timestamp = kwargs.get("from_timestamp", None)
    to_timestamp = kwargs.get("to_timestamp", None)
    precision = kwargs.get("precision", None)
    return coingecko_api.coin_historical_chart_data_within_time_range_by_token_address(id, contract_address, vs_currency, from_timestamp, to_timestamp, precision)

def handle_asset_platforms_list(coingecko_api, **kwargs):
    filter = kwargs.get("filter", None)
    return coingecko_api.asset_platforms_list(filter)

def handle_coins_categories_list(coingecko_api):
    return coingecko_api.coins_categories_list()

def handle_exchanges_list_with_data(coingecko_api, **kwargs):
    per_page = kwargs.get("per_page", 100)
    page = kwargs.get("page", 1)
    return coingecko_api.exchanges_list_with_data(per_page, page)

def handle_exchanges_list(coingecko_api, **kwargs):
    status = kwargs.get("status", "active")
    return coingecko_api.exchanges_list(status)

def handle_exchange_data_by_id(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    return coingecko_api.exchange_data_by_id(id)

def handle_exchange_tickers_by_id(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    coin_ids = kwargs.get("coin_ids", None)
    include_exchange_logo = kwargs.get("include_exchange_logo", False)
    page = kwargs.get("page", None)
    depth = kwargs.get("depth", False)
    order = kwargs.get("order", "trust_score_desc")
    return coingecko_api.exchange_tickers_by_id(id, coin_ids, include_exchange_logo, page, depth, order)

def handle_exchange_volume_chart_by_id(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    days = kwargs.get("days", None)
    return coingecko_api.exchange_volume_chart_by_id(id, days)

def handle_derivatives_tickers_list(coingecko_api):
    return coingecko_api.derivatives_tickers_list()

def handle_derivatives_exchanges_list_with_data(coingecko_api, **kwargs):
    order = kwargs.get("order", "open_interest_btc_desc")
    per_page = kwargs.get("per_page", None)
    page = kwargs.get("page", None)
    return coingecko_api.derivatives_exchanges_list_with_data(order, per_page, page)

def handle_derivatives_exchange_data_by_id(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    include_tickers = kwargs.get("include_tickers", None)
    return coingecko_api.derivatives_exchange_data_by_id(id, include_tickers)

def handle_derivatives_exchanges_list(coingecko_api):
    return coingecko_api.derivatives_exchanges_list()

def handle_nfts_list(coingecko_api, **kwargs):
    order = kwargs.get("order", None)
    per_page = kwargs.get("per_page", None)
    page = kwargs.get("page", None)
    return coingecko_api.nfts_list(order, per_page, page)

def handle_nfts_collection_data_by_id(coingecko_api, **kwargs):
    id = kwargs.get("id", None)
    return coingecko_api.nfts_collection_data_by_id(id)

def handle_nfts_collection_data_by_contract_address(coingecko_api, **kwargs):
    asset_platform_id = kwargs.get("asset_platform_id", None)
    contract_address = kwargs.get("contract_address", None)
    return coingecko_api.nfts_collection_data_by_contract_address(asset_platform_id, contract_address)

def handle_btc_to_currency_exchange_rates(coingecko_api):
    return coingecko_api.btc_to_currency_exchange_rates()

def handle_search_queries(coingecko_api, **kwargs):
    query = kwargs.get("query", None)
    return coingecko_api.search_queries(query)

def handle_trending_search_list(coingecko_api):
    return coingecko_api.trending_search_list()

def handle_crypto_global_market_data(coingecko_api):
    return coingecko_api.crypto_global_market_data()

def handle_global_defi_market_data(coingecko_api):
    return coingecko_api.global_defi_market_data()

def handle_public_companies_holdings(coingecko_api, **kwargs):
    coin_id = kwargs.get("coin_id", None)
    return coingecko_api.public_companies_holdings(coin_id)


coingecko_commands = {
    "Check API server status": handle_check_api_server_status,
    "Coin Price by IDs and Symbols": handle_coin_price_by_id,
    "Coin Price by Token Addresses": handle_coin_price_by_token_address,
    "Supported Currencies List": handle_supported_currencies_list,
    "Coins List (ID Map)": handle_coins_list,
    "Coins List with Market Data": handle_coins_list_with_market_data,
    "Coin Data by ID": handle_coin_data_by_id,
    "Coin Tickers by ID": handle_coin_tickers_by_id,
    "Coin Historical Data by ID": handle_coin_historical_data_by_id,
    "Coin Historical Chart Data by ID": handle_coin_historical_chart_data_by_id,
    "Coin Historical Chart Data within Time Range by ID": handle_coin_historical_chart_data_within_time_range_by_id,
    "Coin OHLC Chart by ID": handle_coin_ohlc_chart_by_id,
    "Coin Data by Token Address": handle_coin_data_by_token_address,
    "Coin Historical Chart Data by Token Address": handle_coin_historical_chart_data_by_token_address,
    "Coin Historical Chart Data within Time Range by Token Address": handle_coin_historical_chart_data_within_time_range_by_token_address,
    "Asset Platforms List (ID Map)": handle_asset_platforms_list,
    "Coins Categories List (ID Map)": handle_coins_categories_list,
    "Exchanges List with data": handle_exchanges_list_with_data,
    "Exchanges List (ID Map)": handle_exchanges_list,
    "Exchange Data by ID": handle_exchange_data_by_id,
    "Exchange Tickers by ID": handle_exchange_tickers_by_id,
    "Exchange Volume Chart by ID": handle_exchange_volume_chart_by_id,
    "Derivatives Tickers List": handle_derivatives_tickers_list,
    "Derivatives Exchanges List with Data": handle_derivatives_exchanges_list_with_data,
    "Derivatives Exchange Data by ID": handle_derivatives_exchange_data_by_id,
    "Derivatives Exchanges List (ID Map)": handle_derivatives_exchanges_list,
    "NFTs List (ID Map)": handle_nfts_list,
    "NFTs Collection Data by ID": handle_nfts_collection_data_by_id,
    "NFTs Collection Data by Contract Address": handle_nfts_collection_data_by_contract_address,
    "BTC-to-Currency Exchange Rates": handle_btc_to_currency_exchange_rates,
    "Search Queries": handle_search_queries,
    "Trending Search List": handle_trending_search_list,
    "Crypto Global Market Data": handle_crypto_global_market_data,
    "Global De-Fi Market Data": handle_global_defi_market_data,
    "Public Companies Holdings": handle_public_companies_holdings
}


MechResponse = Tuple[str, Optional[str], Optional[Dict[str, Any]], Any, Any]


def with_key_rotation(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> MechResponse:
        api_keys = kwargs["api_keys"]
        retries_left: Dict[str, int] = api_keys.max_retries()

        def execute() -> MechResponse:
            """Retry the function with a new key."""
            try:
                result = func(*args, **kwargs)
                return result + (api_keys,)
            except Exception as e:
                service = e.__class__.__name__.lower()
                if (
                    hasattr(e, "status_code") and e.status_code == 429
                ):  # If rate limit exceeded
                    if retries_left.get(service, 0) <= 0:
                        raise e
                    retries_left[service] -= 1
                    api_keys.rotate(service)
                    return execute()

                return str(e), "", None, None, api_keys

        mech_response = execute()
        return mech_response

    return wrapper


@with_key_rotation
def run(**kwargs) -> Tuple[Optional[str], Optional[Dict[str, Any]], Any, Any]:
    """
    Main entry point for executing Coinbase Commerce API operations.

    Args:
        **kwargs: Keyword arguments including:
            - tool: Name of the tool/operation to execute
            - api_key: Coinbase Commerce API key
            - Additional arguments specific to each tool

    Returns:
        A tuple containing:
        - Response string from the API
        - Optional prompt sent to the model
        - Optional transaction generated by the tool
        - Optional cost calculation object
    """
    api_keys = kwargs["api_keys"]
    coingecko_api_key = api_keys.get("coingecko", None)
    # Check that the tool has been specified
    command_name = kwargs.get("prompt", None)

    coingecko_api = CoingeckoAPI(coingecko_api_key)

    if command_name is None:
        return error_response("No command has been specified.")
    
    try:
        if command_name.lower() in coingecko_commands.keys().lower():
            response = coingecko_commands[command_name](coingecko_api, **kwargs)
        else:
            response = "Command not found. Please check the command name in prompt and try again."

        # Response, prompt, transaction, cost
        return str(response), None, None, None
    except Exception as e:
        return f"An error occurred: {str(e)}", None, None, None