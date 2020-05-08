import React from 'react';

function Transaction({ transaction }){
    const {input, output} = transaction;
    const recipients = Object.keys(output)
    return (
        <div className="Transaction">
            <div>From: {input.address}</div>
            {recipients.map(resip=>(
            <div key={resip}>
                To: {resip} | Sent: {output[resip]}
            </div>
            ))}
        </div>
    )
}
export default Transaction;