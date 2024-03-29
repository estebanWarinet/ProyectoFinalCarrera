import React from 'react';

class TablasExponentes extends React.Component{


    controlarCambioInputIntensidades = (event) => {
        switch (event.target.name) {
            case "IntLong":
                this.props.onChange("camposNecesarios","intensidadLong",event.target.value)
                break;
            case "IntTrans":
                this.props.onChange("camposNecesarios","intensidadTransv",event.target.value)
                break;
            case "IntVert":
                this.props.onChange("camposNecesarios","intensidadVerti",event.target.value)
                break;
            case "ExpLong":
                this.props.onChange("camposNecesarios","intensidadExpLong",event.target.value)
                break;
            case "ExpTrans":
                this.props.onChange("camposNecesarios","intensidadExpTransv",event.target.value)
                break;
            case "ExpVert":
                this.props.onChange("camposNecesarios","intensidadExpVerti",event.target.value)
                break;
            default :
                break;
        }
    }

    controlarCambioInputEscalaLong = (event) => {
        switch (event.target.name) {
            case "IntLong":
                this.props.onChange("camposNecesarios","escalaLongLong",event.target.value)
                break;
            case "IntTrans":
                this.props.onChange("camposNecesarios","escalaLongTransv",event.target.value)
                break;
            case "IntVert":
                this.props.onChange("camposNecesarios","escalaLongVerti",event.target.value)
                break;
            case "ExpLong":
                this.props.onChange("camposNecesarios","escalaLongExpLong",event.target.value)
                break;
            case "ExpTrans":
                this.props.onChange("camposNecesarios","escalaLongExpTransv",event.target.value)
                break;
            case "ExpVert":
                this.props.onChange("camposNecesarios","escalaLongExpVerti",event.target.value)
                break;
            default :
                break;
        }
    }

    controlarCambioInput = (event) => {
        if (this.props.name === "Intensidades") {
            this.controlarCambioInputIntensidades(event);
        }else{
            this.controlarCambioInputEscalaLong(event);
        }
    }

    render(){
        return(
            <fieldset className="groupbox-border">
                <legend className="groupbox-border">{this.props.name}</legend>
                <div className="control-group">
                    <div className="controls bootstrap-timepicker">
                        <table className="ui very basic collapsing celled table">
                            <thead>
                                <tr>
                                    <th>Dirección</th>
                                    <th>Intensidad</th>
                                    <th>Exponente</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td data-label="Dirección">Longitudinal</td>
                                    <td data-label="Intensidad">
                                        <input name="IntLong" 
                                            type="number"
                                            placeholder = "IntLong"
                                            value={this.props.intensidadLong}
                                            onChange={this.controlarCambioInput} 
                                        />
                                    </td>
                                    <td data-label="Exponente">
                                        <input name="ExpLong"
                                            type="number"
                                            placeholder = "ExpLong"
                                            value={this.props.exponentesLong}
                                            onChange={this.controlarCambioInput} 
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td data-label="Dirección">Transversal</td>
                                    <td data-label="Intensidad">
                                        <input name="IntTrans" 
                                            type="number"
                                            placeholder = "IntTrans"
                                            value={this.props.intensidadTransv}
                                            onChange={this.controlarCambioInput} 
                                        />
                                    </td>
                                    <td data-label="Exponente">
                                        <input name="ExpTrans"
                                            type="number"
                                            placeholder = "ExpTrans"
                                            value={this.props.exponentesTransv}
                                            onChange={this.controlarCambioInput} 
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td data-label="Dirección">Vertical</td>
                                    <td data-label="Intensidad">
                                        <input name="IntVert"
                                            type="number"
                                            placeholder = "IntVert"
                                            value={this.props.intensidadVerti}
                                            onChange={this.controlarCambioInput}
                                        />
                                    </td>
                                    <td data-label="Exponente">
                                        <input name="ExpVert"
                                            type="number"
                                            placeholder = "ExpVert"
                                            value={this.props.exponentesVerti}
                                            onChange={this.controlarCambioInput} 
                                        />
                                    </td>
                                </tr>
                            </tbody>
                        </table>       
                    </div>
                </div>
            </fieldset>
        );
    }

}

export default TablasExponentes;