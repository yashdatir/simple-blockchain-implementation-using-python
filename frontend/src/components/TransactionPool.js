import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Transaction from './Transaction';
import { Button } from 'react-bootstrap';
import { BASE_URL, SECONDS_JS } from '../constants';
import history from '../history';

const POOL_INTERVAL = 10 * SECONDS_JS;

export default function TransactionPool(){
    const [transactions,setTransactions] = useState([]);

    const fetchTransactions=()=>{
        fetch(`${BASE_URL}transaction`)
            .then(response => response.json())
            .then(json => setTransactions(json))
        console.log('called!')
    }

    useEffect(()=>{
        fetchTransactions();
        const intervalId = setInterval(fetchTransactions, POOL_INTERVAL);
        return () => clearInterval(intervalId);
    }, [])

    const fetchMineBlock =()=>{
        fetch(`${BASE_URL}Blockchain/mine`)
            .then(()=>{
                alert('Success')
                history.push('/Blockchain/mine')
            })
    }

    return(
        <div className="TransactionPool">
            <Link to='/'>Home</Link>
            <h3>Transaction Pool</h3>
            <div>
                {
                    transactions.map(transact =>(
                        <div key={transact.id}>
                            <hr />
                            <Transaction transaction={transact} />
                        </div>
                    ))
                }
            </div>
            <hr />
            <Button variant="danger" onClick={fetchMineBlock}>Mine a block of these Transactions</Button>
        </div>
    )
}