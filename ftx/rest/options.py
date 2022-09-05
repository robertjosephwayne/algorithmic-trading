# Options

# GET /options/requests
def list_quote_requests():
    return


# GET /options/my_requests
def your_quote_requests():
    return


# POST /options/requests
def create_quote_request():
    return


# DELETE /options/requests/{request_id}
def cancel_quote_request():
    return


# GET /options/requests/{request_id}/quotes
def get_quotes_for_your_quote_request():
    return


# POST /options/requests/{request_id}/quotes
def create_quote():
    return


# GET /options/my_quotes
def get_my_quotes():
    return


# DELETE /options/quotes/<quote_id>
def cancel_quote():
    return


# POST /options/quotes/<quote_id>/accept
def accept_options_quote():
    return


# GET /options/account_info
def get_account_options_info():
    return


# GET /options/positions
def get_options_positions():
    return


# GET /options/trades
def get_public_options_trades():
    return


# GET /options/fills
def get_options_fills():
    return


# GET /stats/24h_options_volume
def get_24h_option_volume():
    return


# GET /options/historical_volumes/BTC
def get_option_historical_volumes():
    return


# GET /options/open_interest/BTC
def get_option_open_interest():
    return


# GET options/historical_open_interest/BTC
def get_option_historical_open_interest():
    return

    