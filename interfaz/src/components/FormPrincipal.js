import React from 'react';

import GrillaControl from './FormGrillaControl';
import IngresoDatos from './FormIngresoDatos/FormIngresoDatos';
import OpcionesAvazadas from './FormOpcionesAvanzadas/FormOpcionesAvanzadas';
import BotonesInferiores from './BotononesInferiores';
import ApiAddress from './Api/Api';
import history from './history';

import './FormPrincipal.css';


class FormPrincipal extends React.Component{

    state = {
        opcionesAvanzadasActive : true,
        datosGrilla : {
            stateConGrilla: true,
            archivoGrilla : "",
            valorMinimoY: "", 
            valorMaximoY: "", 
            valorMinimoZ: "", 
            valorMaximoZ: "",
        },
        camposNecesarios : {
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
        },
        camposOpcionesAvanzadas : {
            opAv_ConstDecaimiento : "",
            opAv_CantSegmentos : "",
            opAv_CantFrecuencias : "",
            opAv_FrecMaxima : "",
            opAv_CantPasosTemp : "",
            opAv_PasoEspacial : "",
            opAv_PasoGrilla : ""
        },
        opAv_DistCaracteristica : 0.5,
    }

    limpiarEstadosParticulares = (estado,valor) =>{
        this.setState({
            camposOpcionesAvanzadas: {
                ...this.state.camposOpcionesAvanzadas,
                [estado]: valor
            }
        });
    }

    setEstados = (nombre,estado,valor) => {
        switch (nombre){
            case "datosGrilla":
                this.setState({
                    datosGrilla: {
                        ...this.state.datosGrilla,
                        [estado]: valor
                    }
                });
                break;
            case "camposNecesarios":
                this.setState({
                    camposNecesarios: {
                        ...this.state.camposNecesarios,
                        [estado]: valor
                    }
                });
                break;
            case "camposOpcionesAvanzadas":
                this.setState({
                    camposOpcionesAvanzadas: {
                        ...this.state.camposOpcionesAvanzadas,
                        [estado]: valor
                    }
                });
                break;
            case "opAv_DistCaracteristica":
                this.setState({
                    [estado]: valor
                });
                break;
            default:
                break;
        }
    }

    limpiarDatos = () => {
        //this.setState({
        //    archivoGrilla : "",
        //    valorMinimoY: "",
        //    valorMaximoY: "",
        //    valorMinimoZ: "",
        //    valorMaximoZ: "", 
        //    escala : "",
        //    alturaReferencia : "",
        //    velocidadMedia : "",
        //    exponenteVelocidad : "",
        //    intensidadLong : "",
        //    intensidadTransv : "",
        //    intensidadVerti : "",
        //    intensidadExpLong : "",
        //    intensidadExpTransv : "",
        //    intensidadExpVerti : "",
        //    escalaLongLong : "",
        //    escalaLongTransv : "",
        //    escalaLongVerti : "",
        //    escalaLongExpLong : "",
        //    escalaLongExpTransv : "",
        //    escalaLongExpVerti : ""
        //});
        //this.limpiarDatosAvanzados();
        
    }

    manejarArchivo = () => {
        const formData = new FormData();
        return formData.append('file', this.state.archivoGrilla);
    }

    onSubmit = async () => {
        //console.log(this.controlarOpcionesVacias())
        const datosGrilla = this.state.datosGrilla;
        const datosNecesarios = this.state.camposNecesarios;
        const datosOpcionesAvanzadas = this.state.camposOpcionesAvanzadas;
        const opAv_DistCaracteristica = this.state.opAv_DistCaracteristica;
        const datosAvanzados = {...datosOpcionesAvanzadas,opAv_DistCaracteristica}
        const datos = {datosGrilla, datosNecesarios, datosAvanzados}
        await ApiAddress.post('/DatosEntrada',{
            datos
        });
        history.push('/Generando');
    }

    controlarCambioOpcionesAvanzadas = () => {
        if(this.state.opcionesAvanzadasActive){
            this.setState({opcionesAvanzadasActive : false});
        }else{
            this.setState({opcionesAvanzadasActive : true});
        }
        this.limpiarDatosAvanzados();
    }

    limpiarDatosAvanzados = () => {
        //this.setState(
        //    {
        //        opAv_ConstDecaimiento : "",
        //        opAv_CantSegmentos : "",
        //        opAv_CantFrecuencias : "",
        //        opAv_FrecMaxima : "",
        //        opAv_CantPasosTemp : "",
        //        opAv_PasoEspacial : "",
        //        opAv_DistCaracteristica : 0.5,
        //        opAv_PasoGrilla : ""
        //    }
        //);
        Object.keys(this.state.camposOpcionesAvanzadas).map(i => {
            this.setState({
                camposOpcionesAvanzadas: {
                    ...this.state.camposOpcionesAvanzadas,
                    [i]: ""
                }
            });
        });
        console.log(this.state.camposOpcionesAvanzadas);
    }

    render(){
        return (
            <div>
                <div className = "CajasCentradas" >
                    <div style = {{marginBottom : 20}}> 
                        <GrillaControl
                            stateConGrilla = {this.state.datosGrilla.stateConGrilla}
                            archivoGrilla = {this.state.datosGrilla.archivoGrilla}
                            valorMinimoY = {this.state.datosGrilla.valorMinimoY}
                            valorMaximoY = {this.state.datosGrilla.valorMaximoY}
                            valorMinimoZ = {this.state.datosGrilla.valorMinimoZ}
                            valorMaximoZ = {this.state.datosGrilla.valorMaximoZ}
                            onChange = {this.setEstados}
                        /> 
                    </div>
                    <IngresoDatos
                        escala = {this.state.camposNecesarios.escala}
                        alturaReferencia = {this.state.camposNecesarios.alturaReferencia}
                        velocidadMedia = {this.state.camposNecesarios.velocidadMedia}
                        exponenteVelocidad = {this.state.camposNecesarios.exponenteVelocidad}
                        intensidadLong = {this.state.camposNecesarios.intensidadLong}
                        intensidadTransv = {this.state.camposNecesarios.intensidadTransv}
                        intensidadVerti = {this.state.camposNecesarios.intensidadVerti}
                        intensidadExpLong = {this.state.camposNecesarios.intensidadExpLong}
                        intensidadExpTransv = {this.state.camposNecesarios.intensidadExpTransv}
                        intensidadExpVerti = {this.state.camposNecesarios.intensidadExpVerti}
                        escalaLongLong = {this.state.camposNecesarios.escalaLongLong}
                        escalaLongTransv = {this.state.camposNecesarios.escalaLongTransv}
                        escalaLongVerti = {this.state.camposNecesarios.escalaLongVerti}
                        escalaLongExpLong = {this.state.camposNecesarios.escalaLongExpLong}
                        escalaLongExpTransv = {this.state.camposNecesarios.escalaLongExpTransv}
                        escalaLongExpVerti = {this.state.camposNecesarios.escalaLongExpVerti}
                        onChange = {this.setEstados}
                    />
                </div>
                <div className="ui toggle checkbox" style = {{marginBottom : 20}}>
                    <input type="checkbox" name="public" onChange={this.controlarCambioOpcionesAvanzadas} />
                    <label> Opciones avanzadas </label>
                </div>
                <div disabled = {this.state.opcionesAvanzadasActive} style = {{marginBottom : 20}}> 
                    < OpcionesAvazadas
                        stateConGrilla = {this.state.datosGrilla.stateConGrilla}
                        opAv_ConstDecaimiento = {this.state.camposOpcionesAvanzadas.opAv_ConstDecaimiento}
                        opAv_CantSegmentos = {this.state.camposOpcionesAvanzadas.opAv_CantSegmentos}
                        opAv_CantFrecuencias = {this.state.camposOpcionesAvanzadas.opAv_CantFrecuencias}
                        opAv_FrecMaxima = {this.state.camposOpcionesAvanzadas.opAv_FrecMaxima}
                        opAv_CantPasosTemp = {this.state.camposOpcionesAvanzadas.opAv_CantPasosTemp}
                        opAv_PasoEspacial = {this.state.camposOpcionesAvanzadas.opAv_PasoEspacial}
                        opAv_DistCaracteristica = {this.state.opAv_DistCaracteristica}
                        opAv_PasoGrilla = {this.state.camposOpcionesAvanzadas.opAv_PasoGrilla}
                        onChange = {this.setEstados}
                    
                    />
                </div>
                < BotonesInferiores limpiarDatos = {this.limpiarDatos} generarDatos = {this.onSubmit}/>
            </div>
        );
    }
}

export default FormPrincipal;