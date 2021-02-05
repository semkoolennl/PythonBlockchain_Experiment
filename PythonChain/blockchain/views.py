from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt #New
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse, HttpRequest

import io
from uuid import uuid4
from urllib.parse import urlparse
import json, socket

from .Blockchain import Blockchain
from .serializers import BlockchainSerializer, ChainSerializer, TransactionSerializer, NodeSerializer



PyChain = Blockchain()
node_address = str(uuid4()).replace('-', '')
root_node = 'e36f0158f0aed45b3bc755dc52ed4560d'
# Create your views here.
class get_chain(viewsets.ViewSet):
    """
    View for retrieving the chain.
    """
    serializer_class = BlockchainSerializer
    def list(self, request):
        response = {
            'message': 'Chain succesfully retrieved.',
            'node_address': node_address,
            'chain': PyChain.chain,
            'chain_length': len(PyChain.chain),
        }
        statuscode = 200
        return Response(response, statuscode)    


class mine_block(viewsets.ViewSet):
    def list(self, request):
        previous_block = PyChain.previous_block
        nonce = PyChain.proof_of_work(previous_block['nonce'])
        new_block = PyChain.new_block(nonce, PyChain.hash(previous_block))
        response = {
            'result': 'Nonce found!',
            'new_block': new_block,
        }
        
        return Response(response, 200)


class is_valid(viewsets.ViewSet):
    def list(self, request):
        is_valid = PyChain.is_chain_valid(PyChain.chain)
        return Response(is_valid)


class get_pending_transactions(viewsets.ViewSet):
    def list(self, request):
        pending_transactions = PyChain.pending_transactions
        response = {
            'message': 'Pending transactions, succesfully retrieved.',
            'pending_transactions': pending_transactions,
            'total_pending': len(pending_transactions),
        }
        return Response(response, 200)



class add_transaction(viewsets.ViewSet):
    serializer_class = TransactionSerializer
    @csrf_exempt
    def create(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            result = PyChain.add_transaction(validated_data)
            response = {
                'message': 'Success',
                'transaction': result['transaction'],
                'block_index': result['block_index'],
            }
            statuscode = 201
        else:
            response = {
                'message': 'Failure',
                'error_message': serializer.errors,
            }
            statuscode = 400
        return Response(response, statuscode)


class connect_node(viewsets.ViewSet):
    serializer_class = NodeSerializer
    @csrf_exempt
    def list(self, request):
        response = {
            'result': 'Success',
            'data': {
                'message': 'Node currently connected to is:',
                'node_address': node_address,
            }
        }
        return Response()

class connect_node(viewsets.ViewSet):
    serializer_class = NodeSerializer
    @csrf_exempt
    def create(self, request):
        serializer = NodeSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            nodes = validated_data.get('nodes')
            if nodes is None:
                return Response('No node', 400)
            for node in nodes:
                PyChain.add_node(node)

            response = {
                'result': 'Success',
                'data': {
                    'message': 'All the nodes are now connected. The PythonCoin now contains the following nodes:',
                    'total_nodes': list(PyChain.nodes),
                },
            }
            statuscode = 200
        else:
            response = {
                'result': 'Failure',
                'data': {
                    'error_message': serializer.errors,
                }
            }
            statuscode = 300
        return Response(response, statuscode)


class replace_chain(viewsets.ViewSet):
    def list(self, request):
        is_chain_replaced = PyChain.replace_chain()
        if is_chain_replaced:
            data = {
                'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                'new_chain': PyChain.chain,
            }  
        else:
            data = {
                'message': 'All good. The chain is the largest one.',
                'actual_chain': PyChain.chain
            }
        response = {
            'result': 'Success',
            'data': data,
        }
        return Response(response, 200)


    def replace_chain(self):
        network = PyChain.nodes
        longest_chain = None
        max_length = len(PyChain.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and PyChain.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            PyChain.chain = longest_chain
            return True

        return False

