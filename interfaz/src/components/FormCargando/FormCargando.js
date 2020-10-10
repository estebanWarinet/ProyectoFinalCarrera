import React from 'react';
import { Link } from 'react-router-dom';

import './FormCargando.css'
import BarraCargando from './BarraCargando';

class FormCargando extends React.Component{
    render(){
        return (
            <div className = "OrdenCentradoVerticalCargando">
                <img className="ui fluid image" src="./logo192.png" />
                <div className = "FlexHijoBarra" ><BarraCargando /></div>
                <Link to="/" className = "ui button">
                        Cancelar
                </Link>
            </div>
        );
    }
}

export default FormCargando;