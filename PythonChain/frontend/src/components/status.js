import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'font-awesome/css/font-awesome.min.css';
import { Container, Row, Col } from 'react-bootstrap';
import axios from 'axios';

const endpoint = '/api/get_chain'
const mineEndpoint = '/api/mine_block'
class Status extends Component {
    constructor(props) {
        super(props);
        this.state = {
            length: [],
            address: "",
        }
    }

    componentDidMount() {
        axios.get(endpoint)
          .then(res => {
              console.log(res);
              const length = res.data.chain_length;
              const address = res.data.node_address;
              this.setState( { length, address });
          })
    }

    handleMine() {
        axios.get(mineEndpoint).then(res => {
           console.log(res);
           console.log(res.data);
           window.location.reload(false);
         }
        )
    }

    render(){
        return (
            <Container>
                <br/>
                <Row>
                    <Col sm="6">
                        <h5><div><i className="fa fa-cubes"></i></div>No. of Blocks Mined (<a href="#" onClick={this.handleMine}>Mine block</a>)</h5>
                        <hr/>
                        <h5 style={{color: '#007bff'}}>#<b>{this.state.length}</b></h5>
                    </Col>
                    <Col md="6">
                        <br/>
                        <h5> <div>Node Address (sync <a href=""><i className="fa fa-refresh"></i></a> )</div></h5>
                        <hr/>
                        <h5 style={{color: '#007bff'}}>0x{this.state.address}</h5>
                    </Col>
                </Row>
            <br/>
            </Container>
        )
    }
}

export default Status;