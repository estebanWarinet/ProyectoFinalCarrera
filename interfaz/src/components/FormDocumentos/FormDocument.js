import React from 'react';

import './FormDocument.css';
import LinkDocumentos from './LinksDocumentos';


class FormDocument extends React.Component{

    render(){
        return(
            <div className = "OrdenCentradoVerticalDocumentos">
                <LinkDocumentos nombre="Manual" direccion = "/"/>
                <LinkDocumentos nombre="Informe" direccion = "/"/>
                <LinkDocumentos nombre="Base de Datos" direccion = "/"/>
                
            </div>
        );
    }
}

export default FormDocument;