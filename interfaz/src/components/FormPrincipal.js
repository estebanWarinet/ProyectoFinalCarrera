import React from 'react';


import GrillaControl from './FormGrillaControl';
import IngresoDatos from './FormIngresoDatos/FormIngresoDatos';
import OpcionesAvazadas from './FormOpcionesAvanzadas/FormOpcionesAvanzadas';
import BotonesInferiores from './BotononesInferiores';
import './FormPrincipal.css';


class FormPrincipal extends React.Component{

    state = {
        opcionesAvanzadasActive : true,
        archivoGrilla : "",
        valorMinimoY: "",
        valorMaximoY: "",
        valorMinimoZ: "",
        valorMaximoZ: "", 
        escala : "",
        alturaReferencia : "",
        velocidadMedia : "",
        exponenteVelocidad : "",
        intensidadLong : "",
        intensidadTransv : "",
        intensidadVerti : "",
        intensidadExpLong : "",
        intensidadExpTransv : "",
        intensidadExpVerti : "",
        escalaLongLong : "",
        escalaLongTransv : "",
        escalaLongVerti : "",
        escalaLongExpLong : "",
        escalaLongExpTransv : "",
        escalaLongExpVerti : "",
        opAv_ConstDecaimiento : "",
        opAv_CantSegmentos : "",
        opAv_CantFrecuencias : "",
        opAv_FrecMaxima : "",
        opAv_CantPasosTemp : "",
        opAv_PasoEspacial : "",
        opAv_DistCaracteristica : 0.5,
        opAv_PasoGrilla : ""
    }

    setEstados = (estado,valor) => {
        this.setState({
            [estado] : valor
        });
    }

    limpiarDatosAvanzados = () => {
        this.setState(
            {
                opAv_ConstDecaimiento : "",
                opAv_CantSegmentos : "",
                opAv_CantFrecuencias : "",
                opAv_FrecMaxima : "",
                opAv_CantPasosTemp : "",
                opAv_PasoEspacial : "",
                opAv_DistCaracteristica : 0.5,
                opAv_PasoGrilla : ""
            }
        );
    }

    limpiarDatos = () => {
        this.setState({
            archivoGrilla : "",
            valorMinimoY: "",
            valorMaximoY: "",
            valorMinimoZ: "",
            valorMaximoZ: "", 
            escala : "",
            alturaReferencia : "",
            velocidadMedia : "",
            exponenteVelocidad : "",
            intensidadLong : "",
            intensidadTransv : "",
            intensidadVerti : "",
            intensidadExpLong : "",
            intensidadExpTransv : "",
            intensidadExpVerti : "",
            escalaLongLong : "",
            escalaLongTransv : "",
            escalaLongVerti : "",
            escalaLongExpLong : "",
            escalaLongExpTransv : "",
            escalaLongExpVerti : ""
        });
        this.limpiarDatosAvanzados();
    }

    controlarCambioOpcionesAvanzadas = () => {
        if(this.state.opcionesAvanzadasActive){
            this.setState({opcionesAvanzadasActive : false});
        }else{
            this.setState({opcionesAvanzadasActive : true});
        }
        this.limpiarDatosAvanzados();
        
    }

    render(){
        return (
            <div>
                <div className = "CajasCentradas" >
                    <div style = {{marginBottom : 20}}> 
                        <GrillaControl
                            archivoGrilla = {this.state.archivoGrilla}
                            valorMinimoY = {this.state.valorMinimoY}
                            valorMaximoY = {this.state.valorMaximoY}
                            valorMinimoZ = {this.state.valorMinimoZ}
                            valorMaximoZ = {this.state.valorMaximoZ}
                            onChange = {this.setEstados}
                        /> 
                    </div>
                    <IngresoDatos
                        escala = {this.state.escala}
                        alturaReferencia = {this.state.alturaReferencia}
                        velocidadMedia = {this.state.velocidadMedia}
                        exponenteVelocidad = {this.state.exponenteVelocidad}
                        intensidadLong = {this.state.intensidadLong}
                        intensidadTransv = {this.state.intensidadTransv}
                        intensidadVerti = {this.state.intensidadVerti}
                        intensidadExpLong = {this.state.intensidadExpLong}
                        intensidadExpTransv = {this.state.intensidadExpTransv}
                        intensidadExpVerti = {this.state.intensidadExpVerti}
                        escalaLongLong = {this.state.escalaLongLong}
                        escalaLongTransv = {this.state.escalaLongTransv}
                        escalaLongVerti = {this.state.escalaLongVerti}
                        escalaLongExpLong = {this.state.escalaLongExpLong}
                        escalaLongExpTransv = {this.state.escalaLongExpTransv}
                        escalaLongExpVerti = {this.state.escalaLongExpVerti}
                        onChange = {this.setEstados}
                    />
                </div>
                <div className="ui toggle checkbox" style = {{marginBottom : 20}}>
                    <input type="checkbox" name="public" onChange={this.controlarCambioOpcionesAvanzadas} />
                    <label> Opciones avanzadas </label>
                </div>
                <div disabled = {this.state.opcionesAvanzadasActive} style = {{marginBottom : 20}}> 
                    < OpcionesAvazadas
                    
                        opAv_ConstDecaimiento = {this.state.opAv_ConstDecaimiento}
                        opAv_CantSegmentos = {this.state.opAv_CantSegmentos}
                        opAv_CantFrecuencias = {this.state.opAv_CantFrecuencias}
                        opAv_FrecMaxima = {this.state.opAv_FrecMaxima}
                        opAv_CantPasosTemp = {this.state.opAv_CantPasosTemp}
                        opAv_PasoEspacial = {this.state.opAv_PasoEspacial}
                        opAv_DistCaracteristica = {this.state.opAv_DistCaracteristica}
                        opAv_PasoGrilla = {this.state.opAv_PasoGrilla}
                        onChange = {this.setEstados}
                    
                    />
                </div>
                < BotonesInferiores limpiarDatos = {this.limpiarDatos}/>
            </div>
        );
    }
}

export default FormPrincipal;