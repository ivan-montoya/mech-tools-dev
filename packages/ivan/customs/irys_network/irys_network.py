import requests
from typing import Any, Dict, Optional, Tuple, Callable
import functools

from irys_sdk import Builder, DataItem, sign, create_data, EthereumSigner
from irys_sdk.bundle.tags import Tags

class IrysNetworkClient:
    def __init__(self, wallet: str, devnet: bool = False):
        if devnet:
            self.client = Builder("ethereum").wallet(wallet).network("devnet")
            self.client.rpc_url("https://sepolia.drpc.org")
            self.client = self.client.build()
        else:
            self.client = Builder("ethereum").wallet(wallet)
            self.client = self.client.build()

        self.wallet = wallet

    def address(self) -> str:
        return self.client.address

    def upload(self, data: bytearray, tags: Tags = None, target: str = None, anchor: str = None):
        upload_result = self.client.upload(data, tags, target, anchor)

        # manually create and sign a data item
        # (not required if the above ^ upload API works for your usecase)
        signer = EthereumSigner(self.wallet)
        tx = create_data(bytearray(), signer, tags=tags, anchor=anchor, target=target)
        id = sign(tx, signer)
        is_valid = DataItem.verify(tx.get_raw())

        return upload_result

    def get_balance(self) -> int:
        return self.client.get_balance()

    def get_price(self, bytes: int) -> int:
        return self.client.get_price(bytes)

    def fund(self, amount_atomic: int):
        return self.client.fund(amount_atomic)
    

def get_data(tx_id: str):
    url = f"https://gateway.irys.xyz/{tx_id}"
    response = requests.get(url)

    return response.content

def get_tx_metadata(tx_id: str):
    url = f"https://gateway.irys.xyz/tx/{tx_id}"
    response = requests.get(url)

    return response.content


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
        api_keys = kwargs.get("api_keys", None)
        wallet = api_keys.get("irys_wallet", None)

        if wallet is None:
            return error_response("No wallet has been specified.")
        
        devnet = kwargs.get("devnet", False)
        client = IrysNetworkClient(wallet, devnet)

        if client is None:
            return error_response("Error creating Irys network client.")

        if command_name == "address":
            response = client.address()
        elif command_name == "upload":
            data = kwargs.get("data", None)
            tags = kwargs.get("tags", None)
            target = kwargs.get("target", None)
            anchor = kwargs.get("anchor", None)
            response = client.upload(data, tags, target, anchor)
        elif command_name == "get_balance":
            response = client.get_balance()
        elif command_name == "get_price":
            bytes = kwargs.get("bytes", None)
            response = client.get_price(int(bytes))
        elif command_name == "fund":
            amount_atomic = kwargs.get("amount_atomic", None)
            response = client.fund(int(amount_atomic))
        elif command_name == "get_data":
            tx_id = kwargs.get("tx_id", None)
            response = get_data(tx_id)
        elif command_name == "get_tx_metadata":
            tx_id = kwargs.get("tx_id", None)
            response = get_tx_metadata(tx_id)
        else:
            return error_response(
                f"Command {command_name!r} is not in supported commands!"
            )

        # Response, prompt, transaction, cost
        return str(response), command_name, None, None
    except Exception as e:
        return f"An error occurred: {str(e)}", None, None, None