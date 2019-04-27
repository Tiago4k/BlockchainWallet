from hash_util import hash_block, hash_string_256


class Verification:

    def valid_proof(self, transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) +
                 str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        print(guess_hash)
        return guess_hash[0:2] == '00'

    # Function to verify the blockchain. This prevents with tampering of the blockchain.
    # Checks if the first block of a given chain matches the entire previous block's value
    def verify_chain(self, blockchain):
        """Verify the current block and returns True if it's valid, or False if it's not valid."""
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not self.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof of work invalid!')
                return False
        return True

    def verify_transaction(self, transaction, get_balance):
        """Verify a transaction by checking whether the sender has sufficient coins.

        Arguments:
            :transaction: The transaction that should be verified.
        """
        sender_balance = get_balance(transaction.sender)

        return sender_balance >= transaction.amount

    def verify_transactions(self, open_transactions, get_balance):
        """Verifies all open transactions."""
        return all([self.verify_transaction(tx, get_balance) for tx in open_transactions])
