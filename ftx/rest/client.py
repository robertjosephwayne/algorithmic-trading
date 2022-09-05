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

    # POST /historical_balances/requests
    # TODO: This method is not implemented yet.
    def request_historical_balances_and_positions_snapshot():
        return

    def get_historical_balances_and_positions_snapshot(self, request_id):
        return self._get(f'historical_balances/requests/{request_id}')

    def get_all_historical_balances_and_positions_snapshot(self):
        return self._get('historical_balances/requests')

    def get_positions(self):
        return self._get('positions')

    # POST /account/leverage
    # TODO: This method is not implemented yet.
    def change_account_leverage():
        return
    
    # Convert

    # POST /otc/quotes
    # TODO: This method is not implemented yet.
    def request_quote():
        return

    # GET /otc/quotes/{quoteId}
    # TODO: This method is not implemented yet.
    def get_quote_status():
        return

    # POST /otc/quotes/{quote_id}/accept
    # TODO: This method is not implemented yet.
    def accept_quote():
        return
    
    # Fills

    # GET /fills?market={market}
    # TODO: This method is not implemented yet.
    def get_fills():
        return

    # Funding Payments

    # GET /funding_payments
    # TODO: This method is not implemented yet.
    def get_funding_payments():
        return
    
    # Futures

    # GET /futures
    # TODO: This method is not implemented yet.
    def list_all_futures():
        return

    # GET /futures/{future_name}
    # TODO: This method is not implemented yet.
    def get_future():
        return

    # GET /futures/{future_name}/stats
    # TODO: This method is not implemented yet.
    def get_future_stats():
        return

    # GET /funding_rates
    # TODO: This method is not implemented yet.
    def get_funding_rates():
        return

    # GET /indexes/{index_name}/weights
    # TODO: This method is not implemented yet.
    def get_index_weights():
        return

    # GET /expired_futures
    # TODO: This method is not implemented yet.
    def get_expired_futures():
        return

    # GET /indexes/{market_name}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}
    # TODO: This method is not implemented yet.
    def get_historical_index():
        return

    # GET /index_constituents/{underlying}
    # TODO: This method is not implemented yet.
    def get_index_constituents():
        return
    
    # Leveraged Tokens

    # GET /lt/tokens
    # TODO: This method is not implemented yet.
    def list_leveraged_tokens():
        return

    # GET /lt/{token_name}
    # TODO: This method is not implemented yet.
    def get_token_info():
        return

    # GET /lt/balances
    # TODO: This method is not implemented yet.
    def get_leveraged_token_balances():
        return

    # GET /lt/creations
    # TODO: This method is not implemented yet.
    def list_leveraged_token_creation_requests():
        return

    # POST /lt/{token_name}/create
    # TODO: This method is not implemented yet.
    def request_leveraged_token_creation():
        return

    # GET /lt/redemptions
    # TODO: This method is not implemented yet.
    def list_leveraged_token_redemption_requests():
        return

    # POST /lt/{token_name}/redeem
    # TODO: This method is not implemented yet.
    def request_leveraged_token_redemption():
        return

    # GET /etfs/rebalance_info
    # TODO: This method is not implemented yet.
    def request_etf_rebalance_info():
        return
    
    # Markets

    # GET /markets
    # TODO: This method is not implemented yet.
    def get_markets():
        return

    # GET /markets/{market_name}
    # TODO: This method is not implemented yet.
    def get_single_market():
        return

    # GET /markets/{market_name}/orderbook?depth={depth}
    # TODO: This method is not implemented yet.
    def get_orderbook():
        return

    # GET /markets/{market_name}/trades
    # TODO: This method is not implemented yet.
    def get_trades():
        return

    # GET /markets/{market_name}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}
    # TODO: This method is not implemented yet.
    def get_historical_prices():
        return
    
    # NFTs

    # GET /nft/nfts
    # TODO: This method is not implemented yet.
    def list_nfts():
        return

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