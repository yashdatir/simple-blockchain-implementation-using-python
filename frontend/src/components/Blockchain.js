import React, { useState, useEffect } from 'react';
import { BASE_URL } from '../constants';
import Block from './Block';
import { Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const PAGE_RANGE = 3;

function Blockchain(){
    const [blockchain, setBlockchain] = useState([]);
    const [blockchainLength, setBlockchainLength] = useState(0);
    const fetchPage = ({start, end}) =>{
        fetch(`${BASE_URL}Blockchain/range?start=${start}&end=${end}`)
            .then(response => response.json())
            .then(array => setBlockchain(array))
    }

    useEffect(()=>{
        fetchPage({start: 0, end: PAGE_RANGE});

        fetch(`${BASE_URL}Blockchain`)
            .then(response => response.json())
            .then(array => setBlockchain(array))

        fetch(`${BASE_URL}Blockchain/length`)
            .then(response => response.json())
            .then(array => setBlockchainLength(array))
    },[]);

    const ButtonNumber = []
    for(let i=0; i<blockchainLength/PAGE_RANGE; i++){
        ButtonNumber.push(i)
    }

    return (
        <div className="Blockchain">
            <Link to='/'>Home</Link><Link to='/Transaction'>Transaction</Link><br />
            <h3>Blockchain</h3>
            <div>
                {blockchain.map( block => <Block key={block.hash} block={block} />)}
            </div>
            <div>{ButtonNumber.map(nos => {
                const start = nos * PAGE_RANGE;
                const end = (nos+1) * PAGE_RANGE;
                return <span key={nos} onClick={()=>fetchPage({start, end})}>
                    <Button size="sm" variant="danger">{nos+1}</Button>{' '}
                </span>
            })}</div>
        </div>
    )
}
export default Blockchain;