import React from 'react';
import { Link } from 'react-router-dom';

import ApiAddress from './Api/Api';
import history from './history';

class BotononesInferiores extends React.Component {

    onSubmitDescarga = async () => {
        const FileDownload = require('js-file-download');
        const response = await ApiAddress.get('/descargarZip',{
        }).then((response) => {
            FileDownload(response.data, 'report.zip');
       });
        history.push('/');
    }

    render(){
        return (
            <div className = "ui two column grid">
                <div className = "column">
                    <button className = "ui button" onClick = {this.onSubmitDescarga}>Descargar</button>
                </div>
                <div className = "column" align = "right" >
                    <Link to="/Generando" className = "ui button" onClick = {this.props.generarDatos}>
                        Generar
                    </Link>
                    <button className = "ui button" onClick = {this.props.limpiarDatos}>Limpiar</button>
                </div>
            </div>
        )
    }

}

export default BotononesInferiores;