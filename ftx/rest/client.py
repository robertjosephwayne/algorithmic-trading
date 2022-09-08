import time
import urllib.parse
import hmac
from requests import Request, Session, Response

class FtxClient:
    _BASE_URL = 'https://ftx.com/api/'

    def __init__(self, api_key = None, api_secret = None, subaccount_name = None):
        self._session = Session()
        self._api_key = api_key
        self._api_secret = api_secret
        self._subaccount_name = subaccount_name
    
    def _get(self, path, params = None):
        return self._request('GET', path, params=params)
    
    def _post(self, path, params = None):
        return self._request('POST', path, json=params)
    
    def _delete(self, path, params = None):
        return self._request('DELETE', path, json=params)
    
    def _request(self, method, path, **kwargs):
        request = Request(method, self._BASE_URL + path, **kwargs)
        self._sign_request(request)
        response = self._session.send(request.prepare())
        return self._process_response(response)
    
    def _sign_request(self, request):
        ts = int(time.time() * 1000)
        prepared = request.prepare()
        signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
        if prepared.body:
            signature_payload += prepared.body
        signature = hmac.new(self._api_secret.encode(), signature_payload, 'sha256').hexdigest()
        request.headers['FTX-KEY'] = self._api_key
        request.headers['FTX-SIGN'] = signature
        request.headers['FTX-TS'] = str(ts)
        if self._subaccount_name:
            request.headers['FTX-SUBACCOUNT'] = urllib.parse.quote(self._subaccount_name)

    def _process_response(self, response):
        try:
            data = response.json()
            print(data)
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

    def get_historical_balances_and_positions_snapshot(self, request_id, show_avg_price = None):
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

    def get_quote_status(self, quote_id, market = None):
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

    def get_fills(self, market = None, start_time = None, end_time = None, order = None, order_id = None):
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

    def get_funding_payments(self, start_time = None, end_time = None, future = None):
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

    def get_funding_rates(self, start_time = None, end_time = None, future = None):
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

    def get_historical_index(self, market_name, resolution, start_time = None, end_time = None):
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

    def get_single_market(self, market_name, depth = None):
        endpoint = f'markets/{market_name}'
        params = {
            'depth': depth
        }
        return self._get(endpoint, params)

    def get_orderbook(self, market_name, depth = None):
        endpoint = f'markets/{market_name}/orderbook'
        params = {
            'depth': depth
        }
        return self._get(endpoint, params)

    def get_trades(self, market_name, start_time = None, end_time = None):
        endpoint = f'markets/{market_name}/trades'
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
        return self._get(endpoint, params)

    def get_historical_prices(self, market_name, resolution, start_time = None, end_time = None):
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

    # GET /nft/nft/{nft_id}
    # TODO: This method is not implemented yet.
    def get_nft_info():
        return

    # GET /nft/{nft_id}/trades
    # TODO: This method is not implemented yet.
    def get_nft_trades():
        return

    # GET /nft/all_trades
    # TODO: This method is not implemented yet.
    def get_all_nft_trades():
        return

    # GET /nft/{nft_id}/account_info
    # TODO: This method is not implemented yet.
    def get_nft_account_info():
        return

    # GET /nft/collections
    # TODO: This method is not implemented yet.
    def get_all_nft_collections():
        return

    # GET /nft/balances
    # TODO: This method is not implemented yet.
    def get_nft_balances():
        return

    # POST /nft/offer
    # TODO: This method is not implemented yet.
    def make_nft_offer():
        return

    # POST /nft/buy
    # TODO: This method is not implemented yet.
    def buy_nft():
        return

    # POST /nft/auction
    # TODO: This method is not implemented yet.
    def create_auction():
        return

    # POST /nft/edit_auction
    # TODO: This method is not implemented yet.
    def edit_auction():
        return

    # POST /nft/cancel_auction
    # TODO: This method is not implemented yet.
    def cancel_auction():
        return

    # GET /nft/bids
    # TODO: This method is not implemented yet.
    def get_bids():
        return

    # POST /nft/bids
    # TODO: This method is not implemented yet.
    def place_bid():
        return

    # GET /nft/deposits
    # TODO: This method is not implemented yet.
    def get_nft_deposits():
        return

    # GET /nft/withdrawals
    # TODO: This method is not implemented yet.
    def get_nft_withdrawals():
        return

    # GET /nft/fills
    # TODO: This method is not implemented yet.
    def get_nft_fills():
        return

    # POST /nft/redeem
    # TODO: This method is not implemented yet.
    def redeem_nft():
        return

    # GET /nft/gallery/{gallery_id}
    # TODO: This method is not implemented yet.
    def get_nft_gallery():
        return

    # GET /nft/gallery_settings
    # TODO: This method is not implemented yet.
    def get_gallery_settings():
        return

    # POST /nft/gallery_settings
    # TODO: This method is not implemented yet.
    def edit_gallery_settings():
        return

    # Options

    # GET /options/requests
    # TODO: This method is not implemented yet.
    def list_quote_requests():
        return

    # GET /options/my_requests
    # TODO: This method is not implemented yet.
    def your_quote_requests():
        return

    # POST /options/requests
    # TODO: This method is not implemented yet.
    def create_quote_request():
        return

    # DELETE /options/requests/{request_id}
    # TODO: This method is not implemented yet.
    def cancel_quote_request():
        return

    # GET /options/requests/{request_id}/quotes
    # TODO: This method is not implemented yet.
    def get_quotes_for_your_quote_request():
        return

    # POST /options/requests/{request_id}/quotes
    # TODO: This method is not implemented yet.
    def create_quote():
        return

    # GET /options/my_quotes
    # TODO: This method is not implemented yet.
    def get_my_quotes():
        return

    # DELETE /options/quotes/<quote_id>
    # TODO: This method is not implemented yet.
    def cancel_quote():
        return

    # POST /options/quotes/<quote_id>/accept
    # TODO: This method is not implemented yet.
    def accept_options_quote():
        return

    # GET /options/account_info
    # TODO: This method is not implemented yet.
    def get_account_options_info():
        return

    # GET /options/positions
    # TODO: This method is not implemented yet.
    def get_options_positions():
        return

    # GET /options/trades
    # TODO: This method is not implemented yet.
    def get_public_options_trades():
        return

    # GET /options/fills
    # TODO: This method is not implemented yet.
    def get_options_fills():
        return

    # GET /stats/24h_options_volume
    # TODO: This method is not implemented yet.
    def get_24h_option_volume():
        return

    # GET /options/historical_volumes/BTC
    # TODO: This method is not implemented yet.
    def get_option_historical_volumes():
        return

    # GET /options/open_interest/BTC
    # TODO: This method is not implemented yet.
    def get_option_open_interest():
        return

    # GET options/historical_open_interest/BTC
    # TODO: This method is not implemented yet.
    def get_option_historical_open_interest():
        return
    
    # Orders

    # GET /orders?market={market}
    # TODO: This method is not implemented yet.
    def get_open_orders():
        return

    # GET /orders/history?market={market}
    # TODO: This method is not implemented yet.
    def get_order_history():
        return

    # GET /conditional_orders?market={market}
    # TODO: This method is not implemented yet.
    def get_open_trigger_orders():
        return

    # GET /conditional_orders/{conditional_order_id}/triggers
    # TODO: This method is not implemented yet.
    def get_trigger_order_triggers():
        return

    # GET /conditional_orders/history?market={market}
    # TODO: This method is not implemented yet.
    def get_trigger_order_history():
        return

    # GET /twap_orders?market={market}
    # TODO: This method is not implemented yet.
    def get_twap_orders():
        return

    # GET /twap_orders/{twap_order_id}/executions
    # TODO: This method is not implemented yet.
    def get_twap_order_executions():
        return

    # POST /orders
    # TODO: This method is not implemented yet.
    def place_order():
        return

    # POST /conditional_orders
    # TODO: This method is not implemented yet.
    def place_trigger_order():
        return

    # POST /twap_orders
    # TODO: This method is not implemented yet.
    def place_twap_order():
        return

    # POST /orders/{order_id}/modify
    # TODO: This method is not implemented yet.
    def modify_order():
        return

    # POST /orders/by_client_id/{client_order_id}/modify
    # TODO: This method is not implemented yet.
    def modify_order_by_client_id():
        return

    # POST /conditional_orders/{order_id}/modify
    # TODO: This method is not implemented yet.
    def modify_trigger_order():
        return

    # GET /orders/{order_id}
    # TODO: This method is not implemented yet.
    def get_order_status():
        return

    # GET /orders/by_client_id/{client_order_id}
    # TODO: This method is not implemented yet.
    def get_order_status_by_client_id():
        return

    # DELETE /orders/{order_id}
    # TODO: This method is not implemented yet.
    def cancel_order():
        return

    # DELETE /twap_orders/{twap_order_id}
    # TODO: This method is not implemented yet.
    def cancel_twap_order():
        return

    # DELETE /orders/by_client_id/{client_order_id}
    # TODO: This method is not implemented yet.
    def cancel_order_by_client_id():
        return

    # DELETE /conditional_orders/{id}
    # TODO: This method is not implemented yet.
    def cancel_open_trigger_order():
        return

    # DELETE /orders
    # TODO: This method is not implemented yet.
    def cancel_all_orders():
        return

    # DELETE /orders/bulk
    # TODO: This method is not implemented yet.
    def bulk_cancel_orders():
        return

    # DELETE /orders/by_client_id/bulk
    # TODO: This method is not implemented yet.
    def bulk_cancel_orders_by_client_id():
        return

    # Spot Margin

    # GET /spot_margin/history
    # TODO: This method is not implemented yet.
    def get_lending_history():
        return

    # GET /spot_margin/borrow_rates
    # TODO: This method is not implemented yet.
    def get_borrow_rates():
        return

    # GET /spot_margin/lending_rates
    # TODO: This method is not implemented yet.
    def get_lending_rates():
        return

    # GET /spot_margin/borrow_summary
    # TODO: This method is not implemented yet.
    def get_daily_borrowed_amounts():
        return

    # GET /spot_margin/market_info?market={market}
    # TODO: This method is not implemented yet.
    def get_market_info():
        return

    # GET /spot_margin/borrow_history
    # TODO: This method is not implemented yet.
    def get_my_borrow_history():
        return

    # GET /spot_margin/lending_history
    # TODO: This method is not implemented yet.
    def get_my_lending_history():
        return

    # GET /spot_margin/offers
    # TODO: This method is not implemented yet.
    def get_lending_offers():
        return

    # GET /spot_margin/lending_info
    # TODO: This method is not implemented yet.
    def get_lending_info():
        return

    # POST /spot_margin/offers
    # TODO: This method is not implemented yet.
    def submit_lending_offer():
        return
    
    # Staking

    # GET /staking/stakes
    # TODO: This method is not implemented yet.
    def get_stakes():
        return

    # GET /staking/unstake_requests
    # TODO: This method is not implemented yet.
    def get_unstake_requests():
        return

    # GET /staking/balances
    # TODO: This method is not implemented yet.
    def get_stake_balances():
        return

    # POST /staking/unstake_requests
    # TODO: This method is not implemented yet.
    def unstake_request():
        return

    # DELETE /staking/unstake_requests/{request_id}
    # TODO: This method is not implemented yet.
    def cancel_unstake_request():
        return

    # GET /staking/staking_rewards
    # TODO: This method is not implemented yet.
    def get_staking_rewards():
        return

    # POST /srm_stakes/stakes
    # TODO: This method is not implemented yet.
    def stake_request():
        return

    # Stats

    # GET /stats/latency_stats?days={days}&subaccount_nickname={subaccount_nickname}
    # TODO: This method is not implemented yet.
    def get_latency_statistics():
        return
    
    # Subaccounts

    # GET /subaccounts
    # TODO: This method is not implemented yet.
    def get_all_subaccounts():
        return

    # POST /subaccounts
    # TODO: This method is not implemented yet.
    def create_subaccount():
        return

    # POST /subaccounts/update_name
    # TODO: This method is not implemented yet.
    def change_subaccount_name():
        return

    # DELETE /subaccounts
    # TODO: This method is not implemented yet.
    def delete_subaccount():
        return

    # GET /subaccounts/{nickname}/balances
    # TODO: This method is not implemented yet.
    def get_subaccount_balances():
        return

    # POST /subaccounts/transfer
    # TODO: This method is not implemented yet.
    def transfer_between_subaccounts():
        return
    
    # Support Tickets

    # GET /support/tickets
    # TODO: This method is not implemented yet.
    def get_all_support_tickets():
        return

    # GET /support/tickets/<int:ticket_id>/messages
    # TODO: This method is not implemented yet.
    def get_support_ticket_messages():
        return

    # POST /support/tickets
    # TODO: This method is not implemented yet.
    def create_support_ticket():
        return

    # POST /support/tickets/<int:ticket_id>/messages
    # TODO: This method is not implemented yet.
    def send_support_message():
        return

    # POST /support/tickets/<int:ticket_id>/status
    # TODO: This method is not implemented yet.
    def update_support_ticket_status():
        return

    # GET /support/tickets/count_unread
    # TODO: This method is not implemented yet.
    def count_total_number_of_unread_support_messages():
        return

    # POST /support/tickets/<int:ticket_id>/mark_as_read
    # TODO: This method is not implemented yet.
    def mark_support_messages_read():
        return
    
    # Wallet

    # GET /wallet/coins
    # TODO: This method is not implemented yet.
    def get_coins():
        return

    # GET /wallet/balances
    # TODO: This method is not implemented yet.
    def get_balances():
        return

    # GET /wallet/all_balances
    # TODO: This method is not implemented yet.
    def get_balances_of_all_accounts():
        return

    # GET /wallet/deposit_address/{coin}?method={method}
    # TODO: This method is not implemented yet.
    def get_deposit_address():
        return

    # POST /wallet/deposit_address/list
    # TODO: This method is not implemented yet.
    def get_deposit_address_list():
        return

    # GET /wallet/deposits
    # TODO: This method is not implemented yet.
    def get_deposit_history():
        return

    # GET /wallet/withdrawals
    # TODO: This method is not implemented yet.
    def get_withdrawal_history():
        return

    # POST /wallet/withdrawals
    # TODO: This method is not implemented yet.
    def request_withdrawal():
        return

    # GET /wallet/airdrops
    # TODO: This method is not implemented yet.
    def get_airdrops():
        return

    # GET /wallet/withdrawal_fee
    # TODO: This method is not implemented yet.
    def get_withdrawal_fees():
        return

    # GET /wallet/saved_addresses
    # TODO: This method is not implemented yet.
    def get_saved_addresses():
        return

    # POST /wallet/saved_addresses
    # TODO: This method is not implemented yet.
    def create_saved_addresses():
        return

    # DELETE /wallet/saved_addresses/{saved_address_id}
    # TODO: This method is not implemented yet.
    def delete_saved_addresses():
        return

    # POST /sen/deposits/{sen_link_id}
    # TODO: This method is not implemented yet.
    def register_sen_deposit():
        return

    # POST /sen/withdrawals/{sen_link_id}
    # TODO: This method is not implemented yet.
    def request_sen_withdrawal():
        return

    # POST /signet/deposits/{signet_link_id}
    # TODO: This method is not implemented yet.
    def register_signet_deposit():
        return

    # POST /signet/withdrawals/{signet_link_id}
    # TODO: This method is not implemented yet.
    def request_signet_withdrawal():
        return