# Orders

# GET /orders?market={market}
def get_open_orders():
    return


# GET /orders/history?market={market}
def get_order_history():
    return


# GET /conditional_orders?market={market}
def get_open_trigger_orders():
    return


# GET /conditional_orders/{conditional_order_id}/triggers
def get_trigger_order_triggers():
    return


# GET /conditional_orders/history?market={market}
def get_trigger_order_history():
    return


# GET /twap_orders?market={market}
def get_twap_orders():
    return


# GET /twap_orders/{twap_order_id}/executions
def get_twap_order_executions():
    return


# POST /orders
def place_order():
    return


# POST /conditional_orders
def place_trigger_order():
    return


# POST /twap_orders
def place_twap_order():
    return


# POST /orders/{order_id}/modify
def modify_order():
    return


# POST /orders/by_client_id/{client_order_id}/modify
def modify_order_by_client_id():
    return


# POST /conditional_orders/{order_id}/modify
def modify_trigger_order():
    return


# GET /orders/{order_id}
def get_order_status():
    return


# GET /orders/by_client_id/{client_order_id}
def get_order_status_by_client_id():
    return


# DELETE /orders/{order_id}
def cancel_order():
    return


# DELETE /twap_orders/{twap_order_id}
def cancel_twap_order():
    return


# DELETE /orders/by_client_id/{client_order_id}
def cancel_order_by_client_id():
    return


# DELETE /conditional_orders/{id}
def cancel_open_trigger_order():
    return


# DELETE /orders
def cancel_all_orders():
    return


# DELETE /orders/bulk
def bulk_cancel_orders():
    return


# DELETE /orders/by_client_id/bulk
def bulk_cancel_orders_by_client_id():
    return

