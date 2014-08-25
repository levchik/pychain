class NotSupportedBlockchain(Exception):
    def __str__(self):
        return 'Provided blockchain is not supported by Chain API.'


class NotValidAddress(Exception):
    def __str__(self):
        return 'The address is not a valid address for the Bitcoin network.'


class TooManyAddresses(Exception):
    def __str__(self):
        return 'Too many addresses provided. The maximum is 200 addresses.'


class MaxTransactionsNumberExceeded(Exception):
    def __str__(self):
        return 'The max number of transactions is exceeded. The maximum is 500 transactions.'


class TransactionNotFound(Exception):
    def __str__(self):
        return 'The transaction could not be found on the Bitcoin network.'


class TransactionRejected(Exception):
    def __str__(self):
        return 'The transaction was rejected by the Bitcoin network.'


class BlockNotFound(Exception):
    def __str__(self):
        return 'The block could not be found on the Bitcoin network.'


class ServerVerificationFailed(Exception):
    def __str__(self):
        return 'Server was unable to verify url.'


class WebhookNotFound(Exception):
    def __str__(self):
        return 'Unable to find webhook with provided id.'


class InvalidWebhookEvent(Exception):
    def __str__(self):
        return 'The Webhook Event contains an invalid event name.'


class InvalidWebhookConfirmationCount(Exception):
    def __str__(self):
        return 'The Webhook Event contains an invalid confirmation number.' \
               'The valid range is 0 to 10.'
