import React from 'react';
import { Link } from 'react-router-dom';


class BotononesInferiores extends React.Component {

    render(){
        return (
            <div className = "ui two column grid">
                <div className = "column">
                    <button className = "ui button">Descargar</button>
                </div>
                <div className = "column" align = "right">
                    <Link to="/Generando" className = "ui button">
                        Generar
                    </Link>
                    <button className = "ui button" onClick = {this.props.limpiarDatos}>Limpiar</button>
                </div>
            </div>
        )
    }

}

export default BotononesInferiores;