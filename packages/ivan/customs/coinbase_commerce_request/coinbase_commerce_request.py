import http.client
import json
from typing import Any, Dict, Optional, Tuple, List, Callable
import functools


DEFAULT_CC_VERSION = '2018-03-22'


def create_charge(
    api_key: str,
    payload: str
) -> str:
    """
    Creates a charge via the Coinbase Commerce API.
    
    Args:
        api_key: The Coinbase Commerce API key for authentication
        payload: The payload to send to the API
        
    Returns:
        Response data from the API as a JSON string
    """
    conn = http.client.HTTPSConnection("api.commerce.coinbase.com")

    if isinstance(payload, str):
        try:
            # Validate it's valid JSON by parsing and re-dumping
            payload = json.dumps(json.loads(payload))
        except json.JSONDecodeError:
            raise ValueError("payload must be a valid JSON string")
    else:
        raise TypeError("payload must be a string")
    
    conn = http.client.HTTPSConnection("api.commerce.coinbase.com")
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-CC-Api-Key': api_key,
    'X-CC-Version': DEFAULT_CC_VERSION
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
    'X-CC-Version': DEFAULT_CC_VERSION
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
    'X-CC-Version': DEFAULT_CC_VERSION
    }
    conn.request("GET", "/charges", payload, headers)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


def create_new_checkout(
    api_key: str,
    payload: str
) -> str:
    """
    Creates a new checkout session via the Coinbase Commerce API.

    Args:
        api_key: The Coinbase Commerce API key for authentication
        payload: The payload to send to the API

    Returns:
        Response data from the API containing the created checkout details as a JSON string
    """
    conn = http.client.HTTPSConnection("api.commerce.coinbase.com")

    if isinstance(payload, str):
        try:
            # Validate it's valid JSON by parsing and re-dumping
            payload = json.dumps(json.loads(payload))
        except json.JSONDecodeError:
            raise ValueError("payload must be a valid JSON string")
    else:
        raise TypeError("payload must be a string")
    
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-CC-Api-Key': api_key,
    'X-CC-Version': DEFAULT_CC_VERSION
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
    'X-CC-Version': DEFAULT_CC_VERSION
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
    'X-CC-Version': DEFAULT_CC_VERSION
    }
    conn.request("GET", f"/checkouts/{checkout_id}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    return data.decode("utf-8")

def list_events(api_key: str) -> str:
    conn = http.client.HTTPSConnection("api.commerce.coinbase.com")
    payload = ''
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-CC-Api-Key': api_key,
        'X-CC-Version': DEFAULT_CC_VERSION
    }
    conn.request("GET", "/events", payload, headers)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


def show_an_event(api_key: str, event_id: str) -> str:
    conn = http.client.HTTPSConnection("api.commerce.coinbase.com")
    payload = ''
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-CC-Api-Key': api_key,
        'X-CC-Version': DEFAULT_CC_VERSION
    }
    conn.request("GET", f"/events/{event_id}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    return data.decode("utf-8")


#---- Command Handlers ----#


def handle_create_charge(api_key: str, **kwargs) -> str:
    """
    Handler function for creating a charge.
    
    Args:
        api_key: Coinbase Commerce API key
        kwargs: Dictionary containing charge creation parameters
        
    Returns:
        API response as a JSON string
    """
    payload = kwargs.get('payload', '')
    return create_charge(api_key, payload)


def handle_get_charge(api_key: str, **kwargs) -> str:
    """
    Handler function for retrieving a specific charge.
    
    Args:
        api_key: Coinbase Commerce API key
        kwargs: Dictionary containing the charge ID/code
        
    Returns:
        API response as a JSON string
    """
    charge_code_or_charge_id = kwargs.get('charge_code_or_charge_id', '')
    return get_charge(api_key, charge_code_or_charge_id)


def handle_get_all_charges(api_key: str, **kwargs) -> str:
    """
    Handler function for retrieving all charges.
    
    Args:
        api_key: Coinbase Commerce API key
        
    Returns:
        API response as a JSON string
    """
    return get_all_charges(api_key)


def handle_create_new_checkout(api_key: str, **kwargs) -> str:
    """
    Handler function for creating a new checkout session.
    
    Args:
        api_key: Coinbase Commerce API key
        kwargs: Dictionary containing checkout creation parameters
        
    Returns:
        API response as a JSON string
    """
    payload = kwargs.get('payload', '')
    return create_new_checkout(api_key, payload)


def handle_get_all_checkout_sessions(api_key: str, **kwargs) -> str:
    """
    Handler function for retrieving all checkout sessions.
    
    Args:
        api_key: Coinbase Commerce API key
        
    Returns:
        API response as a JSON string
    """
    return get_all_checkout_sessions(api_key)


def handle_get_checkout_session(api_key: str, **kwargs) -> str:
    """
    Handler function for retrieving a specific checkout session.
    
    Args:
        api_key: Coinbase Commerce API key
        kwargs: Dictionary containing the checkout ID
        
    Returns:
        API response as a JSON string
    """
    checkout_id = kwargs.get('checkout_id', '')
    return get_checkout_session(api_key, checkout_id)

def handle_list_events(api_key: str, **kwargs) -> str:
    return list_events(api_key)


def handle_show_an_event(api_key: str, **kwargs) -> str:
    event_id = kwargs.get('event_id', '')
    return show_an_event(api_key, event_id)


AVAILABLE_TOOLS = {
    "creates a charge": handle_create_charge,
    "returns the charge with the order code": handle_get_charge,
    "returns all charges": handle_get_all_charges,
    "creates a new checkout": handle_create_new_checkout,
    "returns all checkout sessions": handle_get_all_checkout_sessions,
    "returns a specific checkout session": handle_get_checkout_session,
    "list events": handle_list_events,
    "show an event": handle_show_an_event
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
    tool_name = kwargs.get("prompt", None)
    tool_name = tool_name.lower()

    if tool_name is None:
        return error_response("No tool has been specified.")

    # Check that the tool is available
    tool = AVAILABLE_TOOLS.get(tool_name, None)
    if tool is None:
        return error_response(
            f"Tool {tool_name!r} is not in supported tools: {tuple(AVAILABLE_TOOLS.keys())}."
        )
    
    api_key = kwargs.get('cc_api_key', '')

    handler_func = AVAILABLE_TOOLS[tool_name]
    response = handler_func(api_key, **kwargs)

    # Response, prompt, transaction, cost
    return str(response), None, None, None