"""Contains the tool definitions"""

import http.client
import json
from typing import Any, Dict, Optional, Tuple, List, Callable
import functools

def create_charge(
    api_key: str,
    name: str,
    description: str,
    buyer_locale: str,
    cancel_url: str,
    checkout_id: str,
    local_price: Dict[str, str],
    metadata: Dict[str, str],
    pricing_type: str,
    redirect_url: str,
) -> str:
    """
    Creates a charge via the Coinbase Commerce API.
    
    Args:
        api_key: The Coinbase Commerce API key for authentication
        name: Name of the product or description
        description: More detailed description of the charge
        buyer_locale: The locale/language for the charge page (e.g. 'en')
        cancel_url: URL to redirect if customer cancels
        checkout_id: Unique identifier for associated checkout
        local_price: Dictionary containing 'amount' and 'currency'
        metadata: Optional metadata to associate with the charge
        pricing_type: Either 'fixed_price' or 'no_price'
        redirect_url: URL to redirect after successful payment
        
    Returns:
        Response data from the API as a JSON string
    """
    conn = http.client.HTTPSConnection("api.commerce.coinbase.com")
    payload = {}
    
    if buyer_locale:
        payload["buyer_locale"] = buyer_locale
    if name:
        payload["name"] = name
    if description:
        payload["description"] = description
    if cancel_url:
        payload["cancel_url"] = cancel_url
    if checkout_id:
        payload["checkout_id"] = checkout_id
    if local_price:
        payload["local_price"] = local_price
    if metadata:
        payload["metadata"] = metadata
    if pricing_type:
        payload["pricing_type"] = pricing_type
    if redirect_url:
        payload["redirect_url"] = redirect_url

    payload = json.dumps(payload)
    conn = http.client.HTTPSConnection("api.commerce.coinbase.com")
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-CC-Api-Key': api_key,
    'X-CC-Version': '2018-03-22'
    }
    conn.request("POST", "/charges", payload, headers)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


def get_charge(api_key: str, charge_code_or_charge_id: str) -> str:
    """
    Retrieves details for a specific charge from the Coinbase Commerce API.

    Args:
        api_key: The Coinbase Commerce API key for authentication
        charge_code_or_charge_id: The unique identifier or code for the charge to retrieve

    Returns:
        Response data from the API containing the charge details as a JSON string
    """
    conn = http.client.HTTPSConnection("api.commerce.coinbase.com")
    payload = ''
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-CC-Api-Key': api_key,
    'X-CC-Version': '2018-03-22'
    }
    conn.request("GET", f"/charges/{charge_code_or_charge_id}", payload, headers)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


def get_all_charges(api_key: str) -> str:
    """
    Retrieves a list of all charges from the Coinbase Commerce API.

    Args:
        api_key: The Coinbase Commerce API key for authentication

    Returns:
        Response data from the API containing all charges as a JSON string
    """
    conn = http.client.HTTPSConnection("api.commerce.coinbase.com")
    payload = ''
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-CC-Api-Key': api_key,
    'X-CC-Version': '2018-03-22'
    }
    conn.request("GET", "/charges", payload, headers)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


def create_new_checkout(
    api_key: str,
    name: str,
    description: str,
    buyer_locale: str,
    local_price: Dict[str, str],
    total_price: Dict[str, str],
    metadata: Dict[str, str],
    pricing_type: str,
    requested_info: List[str]
) -> str:
    """
    Creates a new checkout session via the Coinbase Commerce API.

    Args:
        api_key: The Coinbase Commerce API key for authentication
        name: Name of the product or description
        description: More detailed description of the checkout
        buyer_locale: The locale/language for the checkout page (e.g. 'en')
        local_price: Dictionary containing 'amount' and 'currency' for display price
        total_price: Dictionary containing 'amount' and 'currency' for actual charge
        metadata: Optional metadata to associate with the checkout
        pricing_type: The type of pricing ('fixed_price' or 'no_price')
        requested_info: List of information fields to collect from customer (e.g. ['name', 'email'])

    Returns:
        Response data from the API containing the created checkout details as a JSON string
    """
    conn = http.client.HTTPSConnection("api.commerce.coinbase.com")
    payload = {}

    if name:
        payload["name"] = name
    if description:
        payload["description"] = description
    if buyer_locale:
        payload["buyer_locale"] = buyer_locale
    if local_price:
        payload["local_price"] = local_price
    if total_price:
        payload["total_price"] = total_price
    if metadata:
        payload["metadata"] = metadata
    if pricing_type:
        payload["pricing_type"] = pricing_type
    if requested_info:
        payload["requested_info"] = requested_info

    payload = json.dumps(payload)
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-CC-Api-Key': api_key,
    'X-CC-Version': '2018-03-22'
    }
    conn.request("POST", "/checkouts", payload, headers)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


def get_all_checkout_sessions(api_key: str) -> str:
    """
    Retrieves a list of all checkout sessions from the Coinbase Commerce API.

    Args:
        api_key: The Coinbase Commerce API key for authentication

    Returns:
        Response data from the API containing all checkout sessions as a JSON string
    """
    conn = http.client.HTTPSConnection("api.commerce.coinbase.com")
    payload = ''
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-CC-Api-Key': api_key,
    'X-CC-Version': '2018-03-22'
    }
    conn.request("GET", "/checkouts", payload, headers)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


def get_checkout_session(api_key: str, checkout_id: str) -> str:
    """
    Retrieves details for a specific checkout session from the Coinbase Commerce API.

    Args:
        api_key: The Coinbase Commerce API key for authentication
        checkout_id: The unique identifier for the checkout session to retrieve

    Returns:
        Response data from the API containing the checkout session details as a JSON string
    """
    conn = http.client.HTTPSConnection("api.commerce.coinbase.com")
    payload = ''
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-CC-Api-Key': api_key,
    'X-CC-Version': '2018-03-22'
    }
    conn.request("GET", f"/checkouts/{checkout_id}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    return data.decode("utf-8")


AVAILABLE_TOOLS = {
    "create_charge": create_charge,
    "get_charge": get_charge,
    "get_all_charges": get_all_charges,
    "create_new_checkout": create_new_checkout,
    "get_all_checkout_sessions": get_all_checkout_sessions,
    "get_checkout_session": get_checkout_session
}


def error_response(msg: str) -> Tuple[str, None, None, None]:
    """
    Creates a formatted error response tuple.
    
    Args:
        msg: The error message to include
        
    Returns:
        A tuple containing the error message and three None values for prompt, transaction and cost
    """
    return msg, None, None, None

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

    # Check that the tool has been specified
    tool_name = kwargs.get("command", None)

    if tool_name is None:
        return error_response("No tool has been specified.")

    # Check that the tool is available
    tool = AVAILABLE_TOOLS.get(tool_name, None)
    if tool is None:
        return error_response(
            f"Tool {tool_name!r} is not in supported tools: {tuple(AVAILABLE_TOOLS.keys())}."
        )
    
    api_key = kwargs.get('api_key', '')

    if tool_name == 'create_charge':
        response = handle_create_charge(kwargs, api_key)
    elif tool_name == 'get_charge':
        response = handle_get_charge(kwargs, api_key)
    elif tool_name == 'get_all_charges':
        response = handle_get_all_charges(api_key)
    elif tool_name == 'create_new_checkout':
        response = handle_create_new_checkout(kwargs, api_key)
    elif tool_name == 'get_all_checkout_sessions':
        response = handle_get_all_checkout_sessions(api_key)
    elif tool_name == 'get_checkout_session':
        response = handle_get_checkout_session(kwargs, api_key)

    # Response, prompt, transaction, cost
    return str(response), None, None, None


def handle_create_charge(kwargs: Dict[str, Any], api_key: str) -> str:
    """
    Handler function for creating a charge.
    
    Args:
        kwargs: Dictionary containing charge creation parameters
        api_key: Coinbase Commerce API key
        
    Returns:
        API response as a JSON string
    """
    buyer_locale = kwargs.get('buyer_locale', '')
    name = kwargs.get('name', '')
    description = kwargs.get('description', '')
    cancel_url = kwargs.get('cancel_url', '')
    checkout_id = kwargs.get('checkout_id', '')
    local_price = kwargs.get('local_price', '')
    metadata = kwargs.get('metadata', '')
    pricing_type = kwargs.get('pricing_type', '')
    redirect_url = kwargs.get('redirect_url', '')
    return create_charge(api_key, name, description, buyer_locale, cancel_url, checkout_id, local_price, metadata, pricing_type, redirect_url)


def handle_get_charge(kwargs: Dict[str, Any], api_key: str) -> str:
    """
    Handler function for retrieving a specific charge.
    
    Args:
        kwargs: Dictionary containing the charge ID/code
        api_key: Coinbase Commerce API key
        
    Returns:
        API response as a JSON string
    """
    charge_code_or_charge_id = kwargs.get('charge_code_or_charge_id', '')
    return get_charge(api_key, charge_code_or_charge_id)


def handle_get_all_charges(api_key: str) -> str:
    """
    Handler function for retrieving all charges.
    
    Args:
        api_key: Coinbase Commerce API key
        
    Returns:
        API response as a JSON string
    """
    return get_all_charges(api_key)


def handle_create_new_checkout(kwargs: Dict[str, Any], api_key: str) -> str:
    """
    Handler function for creating a new checkout session.
    
    Args:
        kwargs: Dictionary containing checkout creation parameters
        api_key: Coinbase Commerce API key
        
    Returns:
        API response as a JSON string
    """
    name = kwargs.get('name', '')
    description = kwargs.get('description', '')
    buyer_locale = kwargs.get('buyer_locale', '')
    local_price = kwargs.get('local_price', '')
    total_price = kwargs.get('total_price', '')
    metadata = kwargs.get('metadata', '')
    pricing_type = kwargs.get('pricing_type', '')
    requested_info = kwargs.get('requested_info', '')
    return create_new_checkout(api_key, name, description, buyer_locale, local_price, total_price, metadata, pricing_type, requested_info)


def handle_get_all_checkout_sessions(api_key: str) -> str:
    """
    Handler function for retrieving all checkout sessions.
    
    Args:
        api_key: Coinbase Commerce API key
        
    Returns:
        API response as a JSON string
    """
    return get_all_checkout_sessions(api_key)


def handle_get_checkout_session(kwargs: Dict[str, Any], api_key: str) -> str:
    """
    Handler function for retrieving a specific checkout session.
    
    Args:
        kwargs: Dictionary containing the checkout ID
        api_key: Coinbase Commerce API key
        
    Returns:
        API response as a JSON string
    """
    checkout_id = kwargs.get('checkout_id', '')
    return get_checkout_session(api_key, checkout_id)