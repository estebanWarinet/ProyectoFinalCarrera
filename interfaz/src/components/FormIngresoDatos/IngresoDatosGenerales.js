import React from 'react';

class IngresoDatosGenerales extends React.Component{

    controlarCambioInput = (event) => {
        switch (event.target.name) {
            case "escala":
                this.props.onChange("escala",event.target.value)
                break;
            case "altReferencia":
                this.props.onChange("alturaReferencia",event.target.value)
                break;
            case "velMedia":
                this.props.onChange("velocidadMedia",event.target.value)
                break;
            case "expVelocidad":
                this.props.onChange("exponenteVelocidad",event.target.value)
                break;
            default :
                break;
        }
    }

    render(){
        return (

            <div className = "CajaSeparada">
                <input className = "CajaSeparada" 
                    type = "number" 
                    name="escala" 
                    placeholder="Escala 1:" 
                    value={this.props.escala}
                    onChange={this.controlarCambioInput}
                />
                <input className = "CajaSeparada" 
                    type="number" 
                    name="altReferencia" 
                    placeholder="Altura de Referencia" 
                    value={this.props.alturaReferencia}
                    onChange={this.controlarCambioInput}
                />
                <input className = "CajaSeparada" 
                    type="number" 
                    name="velMedia" 
                    placeholder="Velocidad Media" 
                    value={this.props.velocidadMedia}
                    onChange={this.controlarCambioInput}
                />
                <input className = "CajaSeparada" 
                    type="number" 
                    name="expVelocidad" 
                    placeholder="Exponente de Velocidad" 
                    value={this.props.exponenteVelocidad}
                    onChange={this.controlarCambioInput}
                />
            </div>

        );
    }
}

export default IngresoDatosGenerales;