import React, { Component } from 'react';
import { Container, Table } from 'react-bootstrap';
import axios from 'axios';

const endpoint = '/api/get_chain'
const pending = "/api/get_pending_transactions"
class Transactions extends Component {
  constructor(props){
    super(props);
    this.state = {
      transactions: [],
      pending_transactions: [],
    }
  }
  componentDidMount() {
    axios.get(endpoint)
    .then(res => {
        const transactions = res.data.chain;
        this.setState({ transactions: transactions });
    })

    axios.get(pending)
    .then(res => {
        const pending_transactions = res.data.pending_transactions;
        this.setState({ pending_transactions: pending_transactions });
    })
  }

  render(){
    return (
      <Container>
          <h3><b> Pending transactions </b></h3>
      <Table responsive>
  <thead>
  <tr>
      <th>From</th>
      <th>To</th>
      <th>Amount (Sudo)</th>
      <th>Timestamp</th>
    </tr>
  </thead>
  <tbody>
  { this.state.pending_transactions.map(t =>
    <tr key={t}>
      <td><b style={{color: '#007bff'}}>0x{t.sender}</b></td>
      <td><b style={{color: '#007bff'}}>0x{t.recipient}</b></td>
      <td><b style={{color: '#007bff'}}>{parseFloat(t.amount).toFixed(5)} </b></td>
      <td><b style={{color: '#007bff'}}>{t.time}</b></td>
    </tr>
  )}
    </tbody>
    </Table>
    <br/>
    <br/>
      <h3><b> Confirmed transactions </b></h3>
      <p>(Sync to get the latest transactions in the blockchain)</p>
      <Table responsive>
  <thead>
  <tr>
      <th>From</th>
      <th>To</th>
      <th>Amount (Sudo)</th>
      <th>Timestamp</th>
    </tr>
  </thead>
  <tbody>
  { this.state.transactions.slice(0).reverse().map(transaction =>
    transaction.transactions.map( t =>
    <tr key={t}>
      <td><b style={{color: '#007bff'}}>0x{t.sender}</b></td>
      <td><b style={{color: '#007bff'}}>0x{t.recipient}</b></td>
      <td><b style={{color: '#007bff'}}>{parseFloat(t.amount).toFixed(5)} </b></td>
      <td><b style={{color: '#007bff'}}>{t.time}</b></td>
    </tr>
  ))}
    </tbody>
    </Table>
      </Container>
    );
  }
}

export default Transactions;