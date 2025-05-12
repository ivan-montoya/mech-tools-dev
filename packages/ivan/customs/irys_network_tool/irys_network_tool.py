import requests
from typing import Any, Dict, Optional, Tuple, List, Callable
import functools

from irys_sdk.Builder import Builder
from irys_sdk.bundle.tags import Tags


class IrysNetworkClient:
    def __init__(self, wallet: str):
        self.client = Builder("ethereum").wallet(wallet).network("devnet").rpc_url("https://blissful-wild-uranium.ethereum-sepolia.quiknode.pro/ef19a9df3b775be8b295b8e1f01ca9067daf8e78/").build()

    def address(self) -> str:
        return self.client.token_config.address()

    def upload(self, data: bytearray, tags: Tags = None, target: str = None, anchor: str = None):
        return self.client.upload(data, tags, target, anchor)

    def get_balance(self) -> int:
        return self.client.get_balance()

    def get_price(self, bytes: int) -> int:
        return self.client.get_price(bytes)

    def fund(self, amount_atomic: int, multiplier=1.0):
        return self.client.fund(amount_atomic, multiplier)
    

def get_data(self, tx_id: str):
    url = f"https://gateway.irys.xyz/{tx_id}"
    response = requests.get(url)

    return response.json()

def get_tx_metadata(self, tx_id: str):
    url = f"https://gateway.irys.xyz/tx/{tx_id}"
    response = requests.get(url)

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
    # Check that the tool has been specified
    command_name = kwargs.get("prompt", None)

    if command_name is None:
        return error_response("No command has been specified.")
    
    try:
        client = IrysNetworkClient()

        if command_name == "address":
            response = handle_address(client)
        elif command_name == "upload":
            response = handle_upload(client, **kwargs)
        elif command_name == "get_balance":
            response = handle_get_balance(client)
        elif command_name == "get_price":
            response = handle_get_price(client, **kwargs)
        elif command_name == "fund":
            response = handle_fund(client, **kwargs)
        elif command_name == "get_data":
            response = handle_get_data(client, **kwargs)
        elif command_name == "get_tx_metadata":
            response = handle_get_tx_metadata(client, **kwargs)
        else:
            return error_response(
                f"Command {command_name!r} is not in supported commands!"
            )

        # Response, prompt, transaction, cost
        return str(response), None, None, None
    except Exception as e:
        return f"An error occurred: {str(e)}", None, None, None

def handle_address(client):
    return client.address()

def handle_upload(client, **kwargs):
    data = kwargs.get("data", None)
    tags = kwargs.get("tags", None)
    target = kwargs.get("target", None)
    anchor = kwargs.get("anchor", None)
    return client.upload(data, tags, target, anchor)

def handle_get_balance(client):
    return client.get_balance()

def handle_get_price(client, **kwargs):
    bytes = kwargs.get("bytes", None)
    return client.get_price(bytes)

def handle_fund(client, **kwargs):
    amount_atomic = kwargs.get("amount_atomic", None)
    return client.fund(amount_atomic)

def handle_get_data(client, **kwargs):
    tx_id = kwargs.get("tx_id", None)
    return client.get_data(tx_id)

def handle_get_tx_metadata(client, **kwargs):
    tx_id = kwargs.get("tx_id", None)
    return client.get_tx_metadata(tx_id)