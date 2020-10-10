import React from 'react';
import SliderBar from './SliderBar';
import './FormOpcionesAvanzadas.css';

class FormOpcionesAvanzadas extends React.Component{

    controlarCambioInput = (event) => {
        switch (event.target.name) {
            case "constDecaimiento":
                this.props.onChange("opAv_ConstDecaimiento",event.target.value)
                break;
            case "cantSegmentos":
                this.props.onChange("opAv_CantSegmentos",event.target.value)
                break;
            case "cantFrecuencias":
                this.props.onChange("opAv_CantFrecuencias",event.target.value)
                break;
            case "frecMaxima":
                this.props.onChange("opAv_FrecMaxima",event.target.value)
                break;
            case "cantPasosTemporales":
                this.props.onChange("opAv_CantPasosTemp",event.target.value)
                break;
            case "pasoEspacial":
                this.props.onChange("opAv_PasoEspacial",event.target.value)
                break;
            case "pasoGrilla":
                this.props.onChange("opAv_PasoGrilla",event.target.value)
                break;
            default :
                break;
        }
        
    }

    render(){
        return (
            <div>
                <fieldset className="groupbox-border">
                    <legend className="groupbox-border">Opciones Avanzadas</legend>
                        <div className="control-group">
                            <div className="flexHorizontalOpcionesAvanzadas">
                                <div className = "CajasCentradasOpcionesAvanzadas">
                                    <input className="inputMargenInferior" 
                                        type="number" 
                                        name="constDecaimiento" 
                                        placeholder="constDecaimiento"
                                        value={this.props.opAv_ConstDecaimiento}
                                        onChange={this.controlarCambioInput}
                                    />
                                    <input 
                                        className="inputMargenInferior" 
                                        type="number" 
                                        name="cantSegmentos" 
                                        placeholder="cantSegmentos"
                                        value={this.props.opAv_CantSegmentos}
                                        onChange={this.controlarCambioInput}
                                    />
                                    <input className="inputMargenInferior" 
                                        type="number"
                                        name="cantFrecuencias" 
                                        placeholder="cantFrecuencias"
                                        value={this.props.opAv_CantFrecuencias}
                                        onChange={this.controlarCambioInput}
                                    />
                                </div>
                                <div className = "CajasCentradasOpcionesAvanzadas">
                                    <input className="inputMargenInferior" 
                                        type="number" 
                                        name="frecMaxima" 
                                        placeholder="frecMaxima"
                                        value={this.props.opAv_FrecMaxima}
                                        onChange={this.controlarCambioInput}
                                    />
                                    <input className="inputMargenInferior" 
                                        type="number" 
                                        name="cantPasosTemporales" 
                                        placeholder="cantPasosTemporales"
                                        value={this.props.opAv_CantPasosTemp}
                                        onChange={this.controlarCambioInput} 
                                    />
                                    <input className="inputMargenInferior" 
                                        type="number" 
                                        name="pasoEspacial" 
                                        placeholder="pasoEspacial"
                                        value={this.props.opAv_PasoEspacial}
                                        onChange={this.controlarCambioInput}
                                    />
                                </div>
                                <div className = "CajasCentradasOpcionesAvanzadas">
                                    < SliderBar 
                                        opAv_DistCaracteristica = {this.props.opAv_DistCaracteristica}
                                        onChange={this.props.onChange}
                                    />
                                    <input className="inputMargenInferior" 
                                        type="number" 
                                        name="pasoGrilla" 
                                        placeholder="pasoGrilla" 
                                        value={this.props.opAv_PasoGrilla}
                                        onChange={this.controlarCambioInput}
                                    />
                                </div>
                            </div>
                        </div>
                </fieldset>
            </div>
        );
    }

}

export default FormOpcionesAvanzadas;