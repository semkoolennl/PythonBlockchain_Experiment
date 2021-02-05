import hashlib
from datetime import datetime

class Block:
    def __init__(self, previous_hash, transactions):
        self.version = '1'
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = datetime.utcnow()
        

    def __str__(self):
        return f"""
        --------------------
        Timestamp:            {self.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')}
        Transactions:         {self.transactions}
        Previous Block Hash:  {self.previous_hash}    
        Version:              {self.version}   
        --------------------
        """


    def getHash(self):
        string_to_hash = str(self.timestamp) + "".join(self.transactions) + self.previous_hash + self.version
        raw_hash = hashlib.sha256(string_to_hash.encode())
        hex_hash = raw_hash.hexdigest()

        return hex_hash


