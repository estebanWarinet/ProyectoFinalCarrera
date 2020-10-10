import React from 'react';


class SinGrilla extends React.Component {

    componentDidMount(){
        this.props.onChange("archivoGrilla","")
    }

    controlarCambioInput = (event) => {
        switch (event.target.name) {
            case "MinimoY":
                this.props.onChange("valorMinimoY",event.target.value);
                break;
            case "MaximoY":
                this.props.onChange("valorMaximoY",event.target.value);
                break;
            case "MinimoZ":
                this.props.onChange("valorMinimoZ",event.target.value);
                break;
            case "MaximoZ":
                this.props.onChange("valorMaximoZ",event.target.value);
                break;
            default :
                break;
        }        
    }

    render (){
        return (
            <div className = "ui two column grid" align = "center">
                <div className = "row">
                    <div className = "column">
                        <form className = {this.stateClassNameInput}  >
                            <input name="MinimoY"
                                type = "number" 
                                value={this.props.valorMinimoY} 
                                onChange={this.controlarCambioInput} 
                                placeholder = "Valor Minimo Y" 
                            />
                        </form>
                    </div>
                    <div className = "column">
                        <form className = {this.stateClassNameInput}  >
                            <input name="MinimoZ" 
                                type = "number" 
                                value={this.props.valorMinimoZ} 
                                onChange={this.controlarCambioInput} 
                                placeholder = "Valor Minimo Z" 
                            />
                        </form>
                    </div>
                </div>
                <div className = "row">
                    <div className = "column">
                        <form className = {this.stateClassNameInput}  >
                            <input name="MaximoY"
                                type = "number"  
                                value={this.props.valorMaximoY} 
                                onChange={this.controlarCambioInput} 
                                placeholder = "Valor Maximo Y" 
                            />
                        </form>
                    </div>
                    <div className = "column">
                        <form className = {this.stateClassNameInput}  >
                            <input name="MaximoZ" 
                                type = "number" 
                                value={this.props.valorMaximoZ} 
                                onChange={this.controlarCambioInput} 
                                placeholder = "Valor Maximo Z" 
                            />
                        </form>
                    </div>
                </div>
            </div>
            
        );
    }  
}

export default SinGrilla;