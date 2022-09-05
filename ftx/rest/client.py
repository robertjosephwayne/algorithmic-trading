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

    # GET /historical_balances/requests/<request_id>
    # TODO: This method is not implemented yet.
    def get_historical_balances_and_positions_snapshot():
        return

    def get_all_historical_balances_and_positions_snapshot(self):
        return self._get('historical_balances/requests')

    def get_positions(self):
        return self._get('positions')

    # POST /account/leverage
    # TODO: This method is not implemented yet.
    def change_account_leverage():
        return