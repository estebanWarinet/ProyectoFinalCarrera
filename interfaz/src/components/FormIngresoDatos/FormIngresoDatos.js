import React from 'react';
import { Link } from 'react-router-dom';

import TablasExponentes from './TablasExponentes';
import IngresoDatosGenerales from './IngresoDatosGenerales';
import './FormIngresoDatos.css'


class FormIngresoDatos extends React.Component{
    render(){
        return (
            <div style = {{marginBottom : 20}}>
                <fieldset className="groupbox-border">
                    <legend className="groupbox-border">Datos</legend>
                    <div className="controlgroup">
                        <div className = "flexHorizontal">
                            <IngresoDatosGenerales 
                                escala = {this.props.escala}
                                alturaReferencia = {this.props.alturaReferencia}
                                velocidadMedia = {this.props.velocidadMedia}
                                exponenteVelocidad = {this.props.exponenteVelocidad}
                                alturaReferenciaIntensidad = {this.props.alturaReferenciaIntensidad}
                                alturaReferenciaEscalaLong = {this.props.alturaReferenciaEscalaLong}
                                onChange = {this.props.onChange}
                            />
                            <div >
                                <TablasExponentes name = "Intensidades" 
                                    intensidadLong = {this.props.intensidadLong}
                                    intensidadTransv = {this.props.intensidadTransv}
                                    intensidadVerti = {this.props.intensidadVerti}
                                    exponentesLong = {this.props.intensidadExpLong}
                                    exponentesTransv = {this.props.intensidadExpTransv}
                                    exponentesVerti = {this.props.intensidadExpVerti}
                                    onChange = {this.props.onChange}
                                />
                            </div>
                            <div >
                                <TablasExponentes name = "Escala Longitudinal" 
                                    intensidadLong = {this.props.escalaLongLong}
                                    intensidadTransv = {this.props.escalaLongTransv}
                                    intensidadVerti = {this.props.escalaLongVerti}
                                    exponentesLong = {this.props.escalaLongExpLong}
                                    exponentesTransv = {this.props.escalaLongExpTransv}
                                    exponentesVerti = {this.props.escalaLongExpVerti}
                                    onChange = {this.props.onChange}
                                />
                            </div>
                        </div>
                        <div align = "right" style = {{marginTop : 10}}>
                            <Link to={{ pathname: "http://www.nd.edu/~nathaz/" }} target="_blank" className ="button">Data Base Turbulent Air Flow</Link>
                        </div>
                        
                    </div>
                </fieldset>
            </div>
        );
    }
}

export default FormIngresoDatos;