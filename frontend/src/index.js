import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Switch, Route } from 'react-router-dom';
import App from './components/App';
import Blockchain from './components/Blockchain';
import ConductTransaction from './components/ConductTransaction';
import TransactionPool from './components/TransactionPool';
import history from './history';
import './index.css';

ReactDOM.render(
  <Router history={history}>
    <Switch>
      <Route path='/' exact component={App} />
      <Route path='/Blockchain' component={Blockchain} />
      <Route path='/Transaction' component={ConductTransaction} />
      <Route path='/TransactionPool' component={TransactionPool} />
    </Switch>
  </Router>,
  document.getElementById('root')
);
