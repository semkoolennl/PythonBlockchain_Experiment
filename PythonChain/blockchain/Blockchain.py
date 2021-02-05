from datetime import datetime
import hashlib
import json
import socket
import requests
from urllib.parse import urlparse


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.dificulty_target = 5
        self.new_block(
            previous_hash="A lady came up to me one day and said 'Sir! You are drunk', to which I replied 'I am drunk today madam, and tomorrow I shall be sober but you will still be ugly. ― Winston Churchill",
            nonce=1
        )
        self.nodes = set()


    def new_block(self, nonce, previous_hash):
        """
        Creates a new block and adds it to the existing chain.
        """
        block = { 
            'version': '1',
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.utcnow()),
            'transactions': self.pending_transactions,
            'dificulty_target': self.dificulty_target,
            'nonce': nonce,
            'previous_hash': previous_hash,
        }
        self.pending_transactions = []
        self.chain.append(block)

        return block


    @property
    def previous_block(self):
        """
        Return the last block of the existing chain.
        """
        return self.chain[-1]


    def proof_of_work(self, previous_nonce):
        """
        Implementation of the consensus algorithm.
        """
        nonce = 0
        while self.valid_nonce(previous_nonce, nonce, self.dificulty_target) is False:
            nonce +=1

        return nonce


    @staticmethod
    def valid_nonce(previous_nonce, nonce, dificulty_target):
        """
        Validates the block.
        """
        guess = str(nonce**2 - previous_nonce**2).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:dificulty_target] == "0" * dificulty_target


    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of the given block.
        The dictionary is also sorted by its keys.
        """
        encoded_block = json.dumps(block, sort_keys=True).encode()
        block_hash = hashlib.sha256(encoded_block).hexdigest()

        return block_hash


    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:self.dificulty_target] != "0" * self.dificulty_target:
                return False
            previous_block = block
            block_index += 1

        return True


    def add_transaction(self, transaction):
        """
        Creates a new transaction which will be added to the nex block.
        """
        transaction = {
            'sender': transaction['sender'],
            'recipient': transaction['recipient'],
            'amount': transaction['amount'],
            'time': str(datetime.utcnow())
            }
        self.pending_transactions.append(transaction)
        previous_block = self.previous_block

        response = {
            'block_index': previous_block['index'] + 1,
            'transaction': transaction, 
            }
        return response

    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)


    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/api/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True

        return False


