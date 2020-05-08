import React, { useState, useEffect } from 'react';
import { FormGroup, FormControl, Button } from 'react-bootstrap';
import { BASE_URL } from '../constants';
import { Link } from 'react-router-dom';
import history from '../history'

function ConductTracsaction(){
    const [amount, setAmount] = useState(0);
    const [recipient, setRecipient] = useState('');
    const [knownAddr, setKnownAddr] = useState([]);
    useEffect(()=>{
        fetch(`${BASE_URL}transact/address`)
        .then(response => response.json())
        .then(json => setKnownAddr(json))
    },[])
    const submitResponse =()=>{
        fetch(`${BASE_URL}wallet/transact`, 
            {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ 'reciepient':recipient, 'amount':amount })
            }
        ).then(response => response.json)
        .then(json => {
            console.log('Transaction submitted! ',json);
            alert('Success');
            history.push('/TransactionPool');
        })
    }
    return (
        <div className="ConductTransaction">
            <Link to='/'>Home</Link><br /><Link to='/Blockchain'>Blockchain</Link>
            <h3>Conduct Transaction</h3><br />
            <FormGroup>
                <FormControl 
                input="text" 
                placeholder="reciepient" 
                value={recipient} 
                onChange={(e)=>setRecipient(e.target.value)} />
            </FormGroup>

            <FormGroup>
            <FormControl 
                input="number" 
                placeholder="amount" 
                value={amount} 
                onChange={(e)=>setAmount(Number(e.target.value))} />
            </FormGroup>
            <div>
                <Button variant="danger" onClick={submitResponse}>Submit</Button>
            </div>
            <br />
            <div>
                <h4>Known Addresses:</h4>
                {knownAddr.map((addr, i)=>(
                <span key={addr}><u>{addr}</u>{i!==knownAddr.length-1?', ':''}</span>
                ))}
            </div>
        </div>
    )
}
export default ConductTracsaction;