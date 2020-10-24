import React from 'react';
import { Router, Route } from 'react-router-dom';

import FormPrincipal from './FormPrincipal';
import FormCargando from './FormCargando/FormCargando';
import history from './history';
import Header from './Header';


class App extends React.Component{
    render(){
        return (
        <div className = "ui container">
            <Router history = {history}>
                <Header />
                <div>
                    <Route path = "/" exact component = {FormPrincipal} />
                    <Route path = "/Generando" exact component = {FormCargando} />
                </div>
            </Router>
        </div>
        );
    }
}

export default App;