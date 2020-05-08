import React, {useState, useEffect} from 'react';
import logo from '../images/logo.png';
import { BASE_URL } from '../constants';
import { Link } from 'react-router-dom';

function App() {
  const [walletInfo, setWalletInfo] = useState({});
  useEffect(()=>{
    fetch(`${BASE_URL}wallet/info`)
      .then(response => response.json())
      .then(json => setWalletInfo(json))
  }, []);

  const {address, balance} = walletInfo
  return (
    <div className="App">
      <div>
        <h3>Welcome to myChain</h3><hr />
        <img className="logo" src={logo} alt="myChain logo" /><br />
      </div>
      <br />
      <Link to='/Blockchain'>Blockchain</Link><Link to='/Transaction'>Transaction</Link>
      <Link to='/TransactionPool'>TransactionPool</Link>
      <div className="WalletInfo">
        <div>Address: {address}</div>
        <div>Balance: {balance}</div>
      </div>
    </div>
  );
}

export default App;
