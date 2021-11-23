from typing import NamedTuple
import pytest
from starkware.starknet.testing.contract import StarknetContract
from starkware.starknet.testing.starknet import Starknet
from web3 import Web3

from rlp import encode
from eth_utils import encode_hex

from utils.helpers import (
    concat_arr,
    string_to_byte,
    bytes_to_int,
    chunk_bytes_input
)
from utils.block_header import build_block_header
from mocks.blocks import mocked_blocks


class TestsDeps(NamedTuple):
    starknet: Starknet
    keccak_contract: StarknetContract


async def setup():
    starknet = await Starknet.empty()
    keccak_contract = await starknet.deploy(source="contracts/starknet/test/TestKeccak256.cairo", cairo_path=["contracts"])
    return TestsDeps(
        starknet=starknet,
        keccak_contract=keccak_contract
    )



# The testing library uses python's asyncio. So the following
# decorator and the ``async`` keyword are needed.
@pytest.mark.asyncio
async def test_keccak256():
    starknet, keccak_contract = await setup()

    keccak_input = [
        'f90218a0',
        '03b016cc',
        '9387cb3c',
        'ef86d9d4',
    ]
    
    web3_computed_hash = Web3.keccak(concat_arr(keccak_input).encode('UTF-8', 'little')).hex()

    test_keccak_call = await keccak_contract.test_keccak256(
        len(concat_arr(keccak_input)), list(map(string_to_byte, keccak_input))
    ).call()


    starknet_hashed = test_keccak_call.result.res
    output = '0x' + ''.join(v.to_bytes(8, 'little').hex() for v in starknet_hashed)

    assert output == web3_computed_hash


@pytest.mark.asyncio
async def test_blockhash_hashing():
    starknet, keccak_contract = await setup()

    block = mocked_blocks[0]
    block_header = build_block_header(block)
    block_rlp = block_header.raw_rlp()

    assert block_header.hash() == block["hash"]
    block_rlp_chunked = chunk_bytes_input(block_rlp)
    block_rlp_formatted = list(map(bytes_to_int, block_rlp_chunked))

    test_keccak_call = await keccak_contract.test_keccak256(
        len(block_rlp),
        block_rlp_formatted
    ).call()

    starknet_hashed = test_keccak_call.result.res
    output = '0x' + ''.join(v.to_bytes(8, 'little').hex() for v in starknet_hashed)

    assert output == block["hash"].hex()

