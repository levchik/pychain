# Pychain

Python library for Chain API

It is built on top of excellent Requests library, has its own exceptions and follows PEP8! Please feel free to contribute and send pull requests. If you've committed, feel free to include your name in contributors list.

## Install

    pip install pychain

## Quick Start

    from pychain import ChainAPI
    chain = ChainAPI(API_KEY_ID, API_KEY_SECRET)
    chain.addresses('17x23dNjXJLzGMev6R63uyRhMWP1VHawKc')

You can get an API key and secret by signing up at https://chain.com.

## Documentation

    The Chain API Documentation is available at https://chain.com/docs

### Example of usage

    from pychain import ChainAPI
    chain = ChainAPI(API_KEY_ID, API_KEY_SECRET)

    # Get Bitcoin Address
    chain.addresses('17x23dNjXJLzGMev6R63uyRhMWP1VHawKc')
    # Get Bitcoin Address Transactions
    chain.transactions('17x23dNjXJLzGMev6R63uyRhMWP1VHawKc')
    # Get Bitcoin Address Unspent Outputs
    chain.unspents('17x23dNjXJLzGMev6R63uyRhMWP1VHawKc')
    # Get Bitcoin Address OP_RETURNs
    chain.address_op_returns('17x23dNjXJLzGMev6R63uyRhMWP1VHawKc')

    # Get Bitcoin Transaction
    chain.transaction('0f40015ddbb8a05e26bbacfb70b6074daa1990b..')
    # Get Bitcoin Transaction OP_Return
    chain.transaction_op_returns('0f40015ddbb8a05e26bbacfb70b6..')
    # Send Bitcoin Transaction
    chain.send_transaction('0100000001ec...')

    # Get Bitcoin Block
    chain.block_by_hash('00000000000000009cc33fe219537756a68ee..')
    chain.block_by_height('308920')
    chain.latest_block()
    # Get Bitcoin Block OP_RETURNs
    chain.block_op_returns_by_hash('00000000000000009cc33fe219..')
    chain.block_op_returns_by_height('308920')

    # Create Webhook
    chain.create_webhook('https://username:password@your-serve..')
    # List Webhooks
    chain.list_webhooks()
    # Update Webhook
    chain.update_webhook('FFA21991-5669-4728-..', 'https://use..')
    # Delete Webhook
    chain.remove_webhook('FFA21991-5669-4728-..')

    # Create Webhook Event
    chain.create_webhook_event('FFA-..', 'address-transaction', 'bitcoin', '1..')
    # List Webhook Events
    chain.list_webhook_events('FFA21991-5669-4728-..')
    # Delete Webhook Event
    chain.delete_webhook_event('FFA-..', 'address-transaction', '1..')

### Useful links

[HISTORY](HISTORY.md)
[LICENSE](LICENSE)
