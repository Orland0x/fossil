# Fossil - Starknet-based State Verifier by Oiler

Fossil will allow anyone to trustlessly prove any past or current headers, state, and storage values of L1 contracts to other L2 contracts.

*Fossil is being developed by [Oiler Network](https://oiler.network), and will soon power many of Oiler's Derivative Products.*

## Architecure

Fossil is built out of the following components:

- L1 messaging contracts
- L2 contract receiving L1 messages
- L2 contract storing and processing L1 block headers
- Facts registry which stores the proven facts

![alt text](https://github.com/marcellobardus/starknet-l2-storage-verifier/blob/master/.github/storage-verifier.png?raw=true)
*Storage Verifier Flow diagram*

## Testing

In order to run the tests, please make sure to have a python 3.7 virtual environment.

## Contribute

There are countless usecases for the storage verifier and we are excited to hear what the community wants to build with it! Please reach out to <kacper@oiler.network> for any partnership, sponsorship, or other matters.
