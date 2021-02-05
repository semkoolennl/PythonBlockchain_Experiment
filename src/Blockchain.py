import json, hashlib
from datetime import datetime

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.new_block(
            previous_hash="A lady came up to me one day and said 'Sir! You are drunk', to which I replied 'I am drunk today madam, and tomorrow I shall be sober but you will still be ugly. ― Winston Churchill",
            proof=100
        )

    
    def print(self):
        print(json.dumps(self.chain, indent=4, sort_keys=True))


    def new_block(self, proof, previous_hash=None):
        """
        Creates a new block and adds it to the existing chain.
        """
        block = { 
            'version': '1',
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.utcnow()),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)

        return block

    
    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction which will be added to the nex block.
        """
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        }
        self.pending_transactions.append(transaction)

        return transaction

    
    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of the given block.
        The dictionary is also sorted by its keys.
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        block_hash = hashlib.sha256(block_string).hexdigest()

        return block_hash


    @property
    def last_block(self):
        """
        Return the last block of the existing chain.
        """
        return self.chain[-1]

    
    def proof_of_work(self, last_proof):
        """
        Implementation of the consensus algorithm.
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof +=1

        return proof


    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the block.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexigest()

        return guess_hash[:4] == "0000"


    


blockchain = Blockchain()
t1 = blockchain.new_transaction("Alice", "Mikie", "5 BTC")
t2 = blockchain.new_transaction("Bob", "Satoshi", "24 BTC")
blockchain.new_block(200)
t3 = blockchain.new_transaction("Greg", "Etnies", "5434 BTC")
t4 = blockchain.new_transaction("Sophie", "Siggurd", "321 BTC")
blockchain.new_block(530)


blockchain.print()
