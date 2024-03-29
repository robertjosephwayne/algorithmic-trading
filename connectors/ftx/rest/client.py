import time
import urllib.parse
import hmac
from requests import Request, Session, Response
import logging

logger = logging.getLogger()


class FtxClient:
    _BASE_URL = 'https://ftx.com/api/'

    def __init__(self, api_key=None, api_secret=None, subaccount_name=None):
        self._session = Session()
        self._api_key = api_key
        self._api_secret = api_secret
        self._subaccount_name = subaccount_name

        logger.info('FTX client successfully initialized')

    def _get(self, path, params=None):
        return self._request('GET', path, params=params)

    def _post(self, path, params=None):
        return self._request('POST', path, json=params)

    def _delete(self, path, params=None):
        return self._request('DELETE', path, json=params)

    def _request(self, method, path, **kwargs):
        request = Request(method, self._BASE_URL + path, **kwargs)
        self._sign_request(request)
        response = self._session.send(request.prepare())
        return self._process_response(response)

    def _sign_request(self, request):
        ts = int(time.time() * 1000)
        prepared = request.prepare()
        signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode(
        )
        if prepared.body:
            signature_payload += prepared.body
        signature = hmac.new(self._api_secret.encode(),
                             signature_payload, 'sha256').hexdigest()
        request.headers['FTX-KEY'] = self._api_key
        request.headers['FTX-SIGN'] = signature
        request.headers['FTX-TS'] = str(ts)
        if self._subaccount_name:
            request.headers['FTX-SUBACCOUNT'] = urllib.parse.quote(
                self._subaccount_name)

    def _process_response(self, response):
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            if not data['success']:
                raise Exception(data['error'])
            return data['result']

    # Account

    def get_account_information(self):
        return self._get('account')

    def request_historical_balances_and_positions_snapshot(self, accounts, end_time):
        endpoint = 'historical_balances/requests'
        payload = {
            'accounts': accounts,
            'endTime': end_time
        }
        return self._post(endpoint, payload)

    def get_historical_balances_and_positions_snapshot(self, request_id, show_avg_price=None):
        endpoint = f'historical_balances/requests/{request_id}'
        params = {
            'showAvgPrice': show_avg_price
        }
        return self._get(endpoint, params)

    def get_all_historical_balances_and_positions_snapshot(self):
        endpoint = 'historical_balances/requests'
        return self._get(endpoint)

    def get_positions(self, show_avg_price):
        endpoint = 'positions'
        params = {
            'showAvgPrice': show_avg_price
        }
        return self._get(endpoint, params)

    def change_account_leverage(self, leverage):
        endpoint = 'account/leverage'
        payload = {
            'leverage': leverage
        }
        return self._post(endpoint, payload)

    # Convert

    def request_quote(self, from_coin, to_coin, size):
        endpoint = 'otc/quotes'
        payload = {
            'fromCoin': from_coin,
            'toCoin': to_coin,
            'size': size
        }
        return self._post(endpoint, payload)

    def get_quote_status(self, quote_id, market=None):
        endpoint = f'otc/quotes/{quote_id}'
        params = {
            'market': market
        }
        return self._get(endpoint, params)

    def accept_quote(self, quote_id):
        endpoint = f'otc/quotes/{quote_id}/accept'
        payload = {
            'quoteId': quote_id
        }
        return self._post(endpoint, payload)

    # Fills

    def get_fills(self, market=None, start_time=None, end_time=None, order=None, order_id=None):
        endpoint = 'fills'
        params = {
            'market': market,
            'start_time': start_time,
            'end_time': end_time,
            'order': order,
            'orderId': order_id
        }
        return self._get(endpoint, params)

    # Funding Payments

    def get_funding_payments(self, start_time=None, end_time=None, future=None):
        endpoint = 'funding_payments'
        params = {
            'start_time': start_time,
            'end_time': end_time,
            'future': future
        }
        return self._get(endpoint, params)

    # Futures

    def list_all_futures(self):
        endpoint = 'futures'
        return self._get(endpoint)

    def get_future(self, future_name):
        endpoint = f'futures/{future_name}'
        return self._get(endpoint)

    def get_future_stats(self, future_name):
        endpoint = f'futures/{future_name}/stats'
        return self._get(endpoint)

    def get_funding_rates(self, start_time=None, end_time=None, future=None):
        endpoint = 'funding_rates'
        params = {
            'start_time': start_time,
            'end_time': end_time,
            'future': future
        }
        return self._get(endpoint, params)

    def get_index_weights(self, index_name):
        endpoint = f'indexes/{index_name}/weights'
        return self._get(endpoint)

    def get_expired_futures(self):
        endpoint = 'expired_futures'
        return self._get(endpoint)

    def get_historical_index(self, market_name, resolution, start_time=None, end_time=None):
        endpoint = f'indexes/{market_name}/candles'
        params = {
            'resolution': resolution,
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_index_constituents(self, underlying):
        endpoint = f'index_constituents/{underlying}'
        return self._get(endpoint)

    # Leveraged Tokens

    def list_leveraged_tokens(self):
        endpoint = 'lt/tokens'
        return self._get(endpoint)

    def get_token_info(self, token_name):
        endpoint = f'lt/{token_name}'
        return self._get(endpoint)

    def get_leveraged_token_balances(self, token, balance):
        endpoint = 'lt/balances'
        params = {
            'token': token,
            'balance': balance
        }
        return self._get(endpoint, params)

    def list_leveraged_token_creation_requests(self):
        endpoint = 'lt/creations'
        return self._get(endpoint)

    def request_leveraged_token_creation(self, token_name):
        endpoint = f'lt/{token_name}/create'
        return self._post(endpoint)

    def list_leveraged_token_redemption_requests(self):
        endpoint = 'lt/redemptions'
        return self._get(endpoint)

    def request_leveraged_token_redemption(self, token_name):
        endpoint = f'lt/{token_name}/redeem'
        return self._post(endpoint)

    def request_etf_rebalance_info(self):
        endpoint = 'etfs/rebalance_info'
        return self._get(endpoint)

    # Markets

    def get_markets(self):
        endpoint = 'markets'
        return self._get(endpoint)

    def get_single_market(self, market_name, depth=None):
        endpoint = f'markets/{market_name}'
        params = {
            'depth': depth
        }
        return self._get(endpoint, params)

    def get_orderbook(self, market_name, depth=None):
        endpoint = f'markets/{market_name}/orderbook'
        params = {
            'depth': depth
        }
        return self._get(endpoint, params)

    def get_trades(self, market_name, start_time=None, end_time=None):
        endpoint = f'markets/{market_name}/trades'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_historical_prices(self, market_name, resolution, start_time=None, end_time=None):
        endpoint = f'markets/{market_name}/candles'
        params = {
            'resolution': resolution,
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    # NFTs

    def list_nfts(self):
        endpoint = 'nft/nfts'
        return self._get(endpoint)

    def get_nft_info(self, nft_id):
        endpoint = f'nft/nft/{nft_id}'
        return self._get(endpoint)

    def get_nft_trades(self, nft_id, start_time=None, end_time=None):
        endpoint = f'nft/{nft_id}/trades'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_all_nft_trades(self, start_time=None, end_time=None):
        endpoint = 'nft/all_trades'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_nft_account_info(self, nft_id):
        endpoint = f'nft/{nft_id}/account_info'
        return self._get(endpoint)

    def get_all_nft_collections(self):
        endpoint = 'nft/collections'
        return self._get(endpoint)

    def get_nft_balances(self):
        endpoint = 'nft/balances'
        return self._get(endpoint)

    def make_nft_offer(self, nft_id, price):
        endpoint = 'nft/balances'
        payload = {
            'nftId': nft_id,
            'price': price
        }
        return self._post(endpoint, payload)

    def buy_nft(self, nft_id, price):
        endpoint = 'nft/buy'
        payload = {
            'nftId': nft_id,
            'price': price
        }
        return self._post(endpoint, payload)

    def create_auction(self, initial_price, reservation_price, duration):
        endpoint = 'nft/auction'
        payload = {
            'initialPrice': initial_price,
            'reservationPrice': reservation_price,
            'duration': duration
        }
        return self._post(endpoint, payload)

    def edit_auction(self, reservation_price):
        endpoint = 'nft/edit_auction'
        payload = {
            'reservationPrice': reservation_price
        }
        return self._post(endpoint, payload)

    def cancel_auction(self, nft_id, reservation_price):
        endpoint = 'nft/cancel_auction'
        payload = {
            'nftId': nft_id,
            'reservationPrice': reservation_price
        }
        return self._post(endpoint, payload)

    def get_bids(self):
        endpoint = 'nft/bids'
        return self._get(endpoint)

    def place_bid(self, nft_id, price):
        endpoint = 'nft/bids'
        payload = {
            'nftId': nft_id,
            'price': price
        }
        return self._post(endpoint, payload)

    def get_nft_deposits(self, start_time=None, end_time=None):
        endpoint = 'nft/deposits'
        params = {
            'start_time	': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_nft_withdrawals(self, start_time=None, end_time=None):
        endpoint = 'nft/withdrawals'
        params = {
            'start_time	': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_nft_fills(self, start_time=None, end_time=None):
        endpoint = 'nft/fills'
        params = {
            'start_time	': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def redeem_nft(self, nft_id, address, notes):
        endpoint = 'nft/redeem'
        payload = {
            'nftId': nft_id,
            'address': address,
            'notes': notes
        }
        return self._post(endpoint, payload)

    def get_nft_gallery(self, gallery_id):
        endpoint = f'nft/gallery/{gallery_id}'
        return self._get(endpoint)

    def get_gallery_settings(self):
        endpoint = 'nft/gallery_settings'
        return self._get(endpoint)

    def edit_gallery_settings(self, public):
        endpoint = 'nft/gallery_settings'
        payload = {
            'public': public
        }
        return self._post(endpoint, payload)

    # Options

    def list_quote_requests(self):
        endpoint = 'options/requests'
        return self._get(endpoint)

    def your_quote_requests(self):
        endpoint = 'options/my_requests'
        return self._get(endpoint)

    def create_quote_request(self, underlying, type, strike, expiry, side, size, limit_price, hide_limit_price, request_expiry=None, counterparty_id=None):
        endpoint = 'options/requests'
        payload = {
            'underlying': underlying,
            'type': type,
            'strike': strike,
            'expiry': expiry,
            'side': side,
            'size': size,
            'limitPrice': limit_price,
            'hideLimitPrice': hide_limit_price,
            'requestExpiry': request_expiry,
            'counterpartyId': counterparty_id
        }
        return self._post(endpoint, payload)

    def cancel_quote_request(self, request_id):
        endpoint = f'options/requests/{request_id}'
        return self._delete(endpoint)

    def get_quotes_for_your_quote_request(self, request_id):
        endpoint = f'options/requests/{request_id}/quotes'
        return self._get(endpoint)

    def create_quote(self, request_id, price):
        endpoint = f'options/requests/{request_id}/quotes'
        payload = {
            'price': price
        }
        return self._post(endpoint, payload)

    def get_my_quotes(self):
        endpoint = 'options/my_quotes'
        return self._get(endpoint)

    def cancel_quote(self, quote_id):
        endpoint = f'options/quotes/{quote_id}'
        return self._delete(endpoint)

    def accept_options_quote(self, quote_id):
        endpoint = f'options/quotes/{quote_id}/accept'
        return self._post(endpoint)

    def get_account_options_info(self):
        endpoint = 'options/account_info'
        return self._get(endpoint)

    def get_options_positions(self):
        endpoint = 'options/positions'
        return self._get(endpoint)

    def get_public_options_trades(self, start_time=None, end_time=None):
        endpoint = 'options/trades'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_options_fills(self, start_time=None, end_time=None):
        endpoint = 'options/fills'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_24h_option_volume(self):
        endpoint = 'stats/24h_options_volume'
        return self._get(endpoint)

    def get_option_historical_volumes(self, ticker, start_time=None, end_time=None):
        endpoint = f'options/historical_volumes/{ticker}'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_option_open_interest(self, ticker):
        endpoint = f'options/open_interest/{ticker}'
        return self._get(endpoint)

    def get_option_historical_open_interest(self, ticker, start_time=None, end_time=None):
        endpoint = f'options/historical_open_interest/{ticker}'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    # Orders

    def get_open_orders(self, market=None):
        endpoint = 'orders'
        params = {
            'market': market
        }
        return self._get(endpoint, params)

    def get_order_history(self, market=None, side=None, order_type=None, start_time=None, end_time=None):
        endpoint = 'orders/history'
        params = {
            'market': market,
            'side': side,
            'orderType': order_type,
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_open_trigger_orders(self, market=None, type=None):
        endpoint = 'conditional_orders'
        params = {
            'market': market,
            'type': type
        }
        return self._get(endpoint, params)

    def get_trigger_order_triggers(self, conditional_order_id):
        endpoint = f'conditional_orders/{conditional_order_id}/triggers'
        return self._get(endpoint)

    def get_trigger_order_history(self, market=None, start_time=None, end_time=None, side=None, type=None, order_type=None):
        endpoint = 'conditional_orders/history'
        params = {
            'market': market,
            'start_time': start_time,
            'end_time': end_time,
            'side': side,
            'type': type,
            'orderType': order_type
        }
        return self._get(endpoint, params)

    def get_twap_orders(self, market):
        endpoint = 'twap_orders'
        params = {
            'market': market
        }
        return self._get(endpoint, params)

    def get_twap_order_executions(self, twap_order_id):
        endpoint = f'twap_orders/{twap_order_id}/executions'
        return self._get(endpoint)

    def place_order(self, market, side, price, type, size, reduce_only=False, ioc=False, post_only=False, client_id=None, reject_on_price_band=False, reject_after_ts=None):
        endpoint = 'orders'
        payload = {
            'market': market,
            'side': side,
            'price': price,
            'type': type,
            'size': size,
            'reduceOnly': reduce_only,
            'ioc': ioc,
            'postOnly': post_only,
            'clientId': client_id,
            'rejectOnPriceBand': reject_on_price_band,
            'rejectAfterTs': reject_after_ts
        }
        return self._post(endpoint, payload)

    def place_trigger_order(self, market, side, size, type, reduce_only=None, retry_until_filled=None):
        endpoint = 'conditional_orders'
        payload = {
            'market': market,
            'side': side,
            'size': size,
            'type': type,
            'reduceOnly': reduce_only,
            'retryUntilFilled': retry_until_filled
        }
        return self._post(endpoint, payload)

    def place_twap_order(self, market, side, size, type, duration_seconds, randomize_size, max_spread=None, max_individual_order_size=None, max_distance_through_book=None, price_bound=None):
        endpoint = 'twap_orders'
        payload = {
            'market': market,
            'side': side,
            'size': size,
            'type': type,
            'durationSeconds': duration_seconds,
            'randomizeSize': randomize_size,
            'maxSpread': max_spread,
            'maxIndividualOrderSize': max_individual_order_size,
            'maxDistanceThroughBook': max_distance_through_book,
            'priceBound': price_bound
        }
        return self._post(endpoint, payload)

    def modify_order(self, order_id, price, size, client_id):
        endpoint = f'orders/{order_id}/modify'
        payload = {
            'price': price,
            'size': size,
            'clientId': client_id
        }
        return self._post(endpoint, payload)

    def modify_order_by_client_id(self, client_order_id, price, size, client_id):
        endpoint = f'orders/by_client_id/{client_order_id}/modify'
        payload = {
            'price': price,
            'size': size,
            'clientId': client_id
        }
        return self._post(endpoint, payload)

    def modify_trigger_order(self, order_id, size, trigger_price, order_price):
        endpoint = f'conditional_orders/{order_id}/modify'
        payload = {
            'size': size,
            'triggerPrice': trigger_price,
            'orderPrice': order_price
        }
        return self._post(endpoint, payload)

    def get_order_status(self, order_id):
        endpoint = f'orders/{order_id}'
        return self._get(endpoint)

    def get_order_status_by_client_id(self, client_order_id):
        endpoint = f'orders/by_client_id/{client_order_id}'
        return self._get(endpoint)

    def cancel_order(self, order_id):
        endpoint = f'orders/{order_id}'
        return self._delete(endpoint)

    def cancel_twap_order(self, twap_order_id):
        endpoint = f'twap_orders/{twap_order_id}'
        return self._delete(endpoint)

    def cancel_order_by_client_id(self, client_order_id):
        endpoint = f'orders/by_client_id/{client_order_id}'
        return self._delete(endpoint)

    def cancel_open_trigger_order(self, id):
        endpoint = f'conditional_orders/{id}'
        return self._delete(endpoint)

    def cancel_all_orders(self, market=None, side=None, conditional_orders_only=None, limit_orders_only=None):
        endpoint = 'orders'
        payload = {
            'market': market,
            'side': side,
            'conditionalOrdersOnly': conditional_orders_only,
            'limitOrdersOnly': limit_orders_only
        }
        return self._delete(endpoint, payload)

    def bulk_cancel_orders(self, order_ids):
        endpoint = 'orders/bulk'
        payload = {
            'orderIds': order_ids
        }
        return self._delete(endpoint, payload)

    def bulk_cancel_orders_by_client_id(self, client_order_ids):
        endpoint = 'bulk_orders_by_client_id'
        payload = {
            'clientOrderIds': client_order_ids
        }
        return self._delete(endpoint, payload)

    # Spot Margin

    def get_lending_history(self, start_time=None, end_time=None):
        endpoint = 'spot_margin/history'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_borrow_rates(self):
        endpoint = 'spot_margin/borrow_rates'
        return self._get(endpoint)

    def get_lending_rates(self):
        endpoint = 'spot_margin/lending_rates'
        return self._get(endpoint)

    def get_daily_borrowed_amounts(self):
        endpoint = 'spot_margin/borrow_summary'
        return self._get(endpoint)

    def get_market_info(self, market):
        endpoint = 'spot_margin/market_info'
        params = {
            'market': market
        }
        return self._get(endpoint, params)

    def get_my_borrow_history(self, start_time=None, end_time=None):
        endpoint = 'spot_margin/borrow_history'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_my_lending_history(self, start_time=None, end_time=None):
        endpoint = 'spot_margin/lending_history'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_lending_offers(self):
        endpoint = 'spot_margin/offers'
        return self._get(endpoint)

    def get_lending_info(self):
        endpoint = 'spot_margin/lending_info'
        return self._get(endpoint)

    def submit_lending_offer(self, coin, size, rate):
        endpoint = 'spot_margin/offers'
        payload = {
            'coin': coin,
            'size': size,
            'rate': rate
        }
        return self._post(endpoint, payload)

    # Staking

    def get_stakes(self):
        endpoint = 'staking/stakes'
        return self._get(endpoint)

    def get_unstake_requests(self):
        endpoint = 'staking/unstake_requests'
        return self._get(endpoint)

    def get_stake_balances(self):
        endpoint = 'staking/balances'
        return self._get(endpoint)

    def unstake_request(self, coin, size):
        endpoint = 'staking/unstake_requests'
        payload = {
            'coin': coin,
            'size': size
        }
        return self._post(endpoint, payload)

    def cancel_unstake_request(self, request_id):
        endpoint = f'staking/unstake_requests/{request_id}'
        return self._delete(endpoint)

    def get_staking_rewards(self, start_time=None, end_time=None):
        endpoint = 'staking/staking_rewards'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def stake_request(self, coin, size):
        endpoint = 'srm_stakes/stakes'
        payload = {
            'coin': coin,
            'size': size
        }
        return self._post(endpoint, payload)

    # Stats

    def get_latency_statistics(self, days=None, subaccount_nickname=None):
        endpoint = 'stats/latency_stats'
        params = {
            'days': days,
            'subaccount_nickname': subaccount_nickname
        }
        return self._get(endpoint, params)

    # Subaccounts

    def get_all_subaccounts(self):
        endpoint = 'subaccounts'
        return self._get(endpoint)

    def create_subaccount(self, nickname):
        endpoint = 'subaccounts'
        payload = {
            'nickname': nickname
        }
        return self._post(endpoint, payload)

    def change_subaccount_name(self, nickname, new_nickname):
        endpoint = 'subaccounts/update_name'
        payload = {
            'nickname': nickname,
            'newNickname': new_nickname
        }
        return self._post(endpoint, payload)

    def delete_subaccount(self, nickname):
        endpoint = 'subaccounts'
        payload = {
            'nickname': nickname
        }
        return self._delete(endpoint, payload)

    def get_subaccount_balances(self, nickname):
        endpoint = f'subaccounts/{nickname}/balances'
        return self._get(endpoint)

    def transfer_between_subaccounts(self, coin, size, source, destination):
        endpoint = 'subaccounts/transfer'
        payload = {
            'coin': coin,
            'size': size,
            'source': source,
            'destination': destination
        }
        return self._post(endpoint, payload)

    # Support Tickets

    def get_all_support_tickets(self):
        endpoint = 'support/tickets'
        return self._get(endpoint)

    def get_support_ticket_messages(self, ticket_id):
        endpoint = f'support/tickets/{ticket_id}/messages'
        return self._get(endpoint)

    def create_support_ticket(self, title, category, message, fiat_deposit_id=None, support_file=None):
        endpoint = 'support/tickets'
        payload = {
            'title': title,
            'category': category,
            'message': message,
            'fiatDepositId': fiat_deposit_id,
            'supportFile': support_file
        }
        return self._post(endpoint, payload)

    def send_support_message(self, ticket_id, message, support_file=None):
        endpoint = f'support/tickets/{ticket_id}/messages'
        payload = {
            'message': message,
            'supportFile': support_file
        }
        return self._post(endpoint, payload)

    def update_support_ticket_status(self, ticket_id, status):
        endpoint = f'support/tickets/{ticket_id}/status'
        payload = {
            'status': status
        }
        return self._post(endpoint, payload)

    def count_total_number_of_unread_support_messages(self):
        endpoint = 'support/tickets/count_unread'
        return self._get(endpoint)

    def mark_support_messages_read(self, ticket_id):
        endpoint = f'support/tickets/{ticket_id}/mark_as_read'
        return self._post(endpoint)

    # Wallet

    def get_coins(self):
        endpoint = 'wallet/coins'
        return self._get(endpoint)

    def get_balances(self):
        endpoint = 'wallet/balances'
        return self._get(endpoint)

    def get_balances_of_all_accounts(self):
        endpoint = 'wallet/all_balances'
        return self._get(endpoint)

    def get_deposit_address(self, coin, method=None):
        endpoint = f'wallet/deposit_address/{coin}'
        params = {
            'method': method
        }
        return self._get(endpoint, params)

    def get_deposit_address_list(self, coin, method=None):
        endpoint = 'wallet/deposit_address/list'
        payload = {
            'coin': coin,
            'method': method
        }
        return self._post(endpoint, payload)

    def get_deposit_history(self, start_time, end_time):
        endpoint = 'wallet/deposits'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_withdrawal_history(self, start_time, end_time):
        endpoint = 'wallet/withdrawals'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def request_withdrawal(self, coin, size, address, tag=None, method=None, password=None, code=None):
        endpoint = 'wallet/withdrawals'
        payload = {
            'coin': coin,
            'size': size,
            'address': address,
            'tag': tag,
            'method': method,
            'password': password,
            'code': code
        }
        return self._post(endpoint, payload)

    def get_airdrops(self, start_time, end_time):
        endpoint = 'wallet/airdrops'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_withdrawal_fees(self, coin, size, address, tag=None, method=None):
        endpoint = 'wallet/withdrawal_fee'
        params = {
            'coin': coin,
            'size': size,
            'address': address,
            'tag': tag,
            'method': method
        }
        return self._get(endpoint, params)

    def get_saved_addresses(self, coin=None):
        endpoint = 'wallet/saved_addresses'
        params = {
            'coin': coin
        }
        return self._get(endpoint, params)

    def create_saved_addresses(self, coin, address, wallet, address_name, is_primetrust, tag=None, whitelist=None, code=None):
        endpoint = 'wallet/saved_addresses'
        payload = {
            'coin': coin,
            'address': address,
            'wallet': wallet,
            'addressName': address_name,
            'isPrimetrust': is_primetrust,
            'tag': tag,
            'whitelist': whitelist,
            'code': code
        }
        return self._post(endpoint, payload)

    def delete_saved_addresses(self, saved_address_id):
        endpoint = f'wallet/saved_addresses/{saved_address_id}'
        return self._delete(endpoint)

    def register_sen_deposit(self, sen_link_id, size):
        endpoint = f'sen/deposits/{sen_link_id}'
        payload = {
            'size': size
        }
        return self._post(endpoint, payload)

    def request_sen_withdrawal(self, sen_link_id, size):
        endpoint = f'sen/withdrawals/{sen_link_id}'
        payload = {
            'size': size
        }
        return self._post(endpoint, payload)

    def register_signet_deposit(self, signet_link_id, size):
        endpoint = f'signet/deposits/{signet_link_id}'
        payload = {
            'size': size
        }
        return self._post(endpoint, payload)

    def request_signet_withdrawal(self, signet_link_id, size):
        endpoint = f'signet/withdrawals/{signet_link_id}'
        payload = {
            'size': size
        }
        return self._post(endpoint, payload)
