import React, { useState } from 'react';
import { MILLISECONDS_PY } from "../constants";
import Transaction from './Transaction';
import { Button } from 'react-bootstrap';
function ToggleDisplay({ block }){
    const [ displayTransaction,setDisplay ] = useState(false);
    const { data } = block;
    const toggleClick=()=>{
        setDisplay(!displayTransaction);
    }
    if(displayTransaction){
        return (
            <div>
                {
                data.map(transactions => 
                    <div key={transactions.id}>
                        <hr />
                        <Transaction transaction={transactions} />
                    </div>
                    )
                }
                <br />
                <Button onClick={toggleClick} variant="danger" size="sm">Collapse</Button>
            </div>
        )
    }
    return (
        <div>
            <br />
            <Button onClick={toggleClick} variant="danger" size="sm">Expand</Button>
        </div>) 
}
function Block({block}){
    const {timestamp, hash} = block;
    const hashDisplay = `${hash.substring(0, 15)}...`;
    const timestampDisplay = new Date(timestamp / MILLISECONDS_PY).toLocaleString();
    return (
        <div className="Block">
            <div>Hash: {hashDisplay}</div>
            <div>Timestamp: {timestampDisplay}</div>
            <ToggleDisplay block={block} />
        </div>
    )
}
export default Block