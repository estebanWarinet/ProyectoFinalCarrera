import React from 'react';

import GrillaControl from './FormGrillaControl';
import IngresoDatos from './FormIngresoDatos/FormIngresoDatos';
import OpcionesAvazadas from './FormOpcionesAvanzadas/FormOpcionesAvanzadas';
import BotonesInferiores from './BotononesInferiores';
import ApiAddress from './Api/Api';
import history from './history';
import ModalImagen from './ModalImagenesult'

import './FormPrincipal.css';


class FormPrincipal extends React.Component{
    // ================= Estados ====================
    state = {
        opcionesAvanzadasActive : true,
        datosGrilla : {
            stateConGrilla: true,
            archivoGrilla: "",
            valorMinimoY: "-1.00",
            valorMaximoY: "1.00",
            valorMinimoZ: "0.05",
            valorMaximoZ: "1.3"
        },
        camposNecesarios : {
            escala : "500",
            alturaReferencia : "0.3644",
            velocidadMedia : "10.0",
            exponenteVelocidad : "0.3264",
            alturaReferenciaIntensidad :"0.3364",
            intensidadLong : "0.2084",
            intensidadTransv : "0.1815",
            intensidadVerti : "0.1523",
            intensidadExpLong : "-0.1914",
            intensidadExpTransv : "-0.1228",
            intensidadExpVerti : "-0.0048",
            alturaReferenciaEscalaLong :"0.254",
            escalaLongLong : "0.302",
            escalaLongTransv : "0.0815",
            escalaLongVerti : "0.0326",
            escalaLongExpLong : "0.473",
            escalaLongExpTransv : "0.8813",
            escalaLongExpVerti : "1.5390"
        },
        camposOpcionesAvanzadas : {
            opAv_ConstDecaimiento : "10",
            opAv_CantSegmentos : "50",
            opAv_CantFrecuencias : "100",
            opAv_FrecMaxima : "100",
            opAv_CantPasosTemp : "1000",
            opAv_PasoEspacial : "0.05",
            opAv_PasoGrilla : "0.2857"
        },
        opAv_DistCaracteristica : 0.3,
        imageData : null,
        openModal : false
    }

    // ================= POST al server para ejecutar CDRFG ==================
    submitAllFiles = async () => {
        let file = this.state.datosGrilla.archivoGrilla;
        const formData = new FormData();
        var dato;
        if(this.state.datosGrilla.archivoGrilla !== ""){
            formData.append("file", file);
            dato= file.name;
        }else{
            dato = "NO-Archivo"
        }
        
        formData.append("archivoGrilla",dato);
        Object.keys(this.state.camposNecesarios).map(i => {
            dato = this.state.camposNecesarios[i];
            formData.append(i, dato);
        });
        Object.keys(this.state.datosGrilla).map(i => {
            if (i !== "archivoGrilla"){
                dato = this.state.datosGrilla[i];
                formData.append(i, dato);
            }
        });
        const datosOpcionesAvanzadas = this.state.camposOpcionesAvanzadas;
        const opAv_DistCaracteristica = this.state.opAv_DistCaracteristica;
        const datosAvanzados = {...datosOpcionesAvanzadas,opAv_DistCaracteristica}
        Object.keys(datosAvanzados).map(i => {
            dato = datosAvanzados[i];
            formData.append(i, dato);
        });

            await ApiAddress
            .post('/upload', formData)
            .then(res => {
                console.log(res.data)
                this.setState({imageData : res.data, openModal : true})
            })
            .catch(err => console.warn(err));

        history.push('/Generando');  
            
    }

    // =============== Intento de limpiar datos avanzados ==================
    limpiarEstadosParticulares = (estado,valor) =>{
        this.setState({
            camposOpcionesAvanzadas: {
                ...this.state.camposOpcionesAvanzadas,
                [estado]: valor
            }
        });
    }

    // ==================== Funcion para setear estados =====================
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
            case "openModal":
                this.setState({
                    [estado]: valor
                });
                break;
            default:
                break;
        }
    }

    limpiarDatos = async () => {
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
        const response = await ApiAddress
            .get("/descargar-desdeDirectorio");
        history.push('/');  

        console.log(response.data);
        this.setState({imageData : response.data, openModal : true})
    }

    showImage = () => {

        if (this.state.imageData !== null) {
            return  <ModalImagen 
                        imageData = {this.state.imageData} 
                        openModal = {this.state.openModal}
                        onChange = {this.setEstados}/>
        }
        return <div>NO IMAGE</div>
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
    }

    // =================== Para activar y desactivar op avanzadas ======================
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
                        alturaReferenciaIntensidad = {this.state.camposNecesarios.alturaReferenciaIntensidad}
                        intensidadLong = {this.state.camposNecesarios.intensidadLong}
                        intensidadTransv = {this.state.camposNecesarios.intensidadTransv}
                        intensidadVerti = {this.state.camposNecesarios.intensidadVerti}
                        intensidadExpLong = {this.state.camposNecesarios.intensidadExpLong}
                        intensidadExpTransv = {this.state.camposNecesarios.intensidadExpTransv}
                        intensidadExpVerti = {this.state.camposNecesarios.intensidadExpVerti}
                        alturaReferenciaEscalaLong = {this.state.camposNecesarios.alturaReferenciaEscalaLong}
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
                < BotonesInferiores limpiarDatos = {this.limpiarDatos} generarDatos = {this.submitAllFiles}/>
            </div>
        );
    }
}

export default FormPrincipal;