import React from 'react';


class Grilla extends React.Component {

    componentDidMount(){
        this.props.onChange("valorMinimoY","")
        this.props.onChange("valorMaximoY","")
        this.props.onChange("valorMinimoZ","")
        this.props.onChange("valorMaximoZ","")
    }

    controlarCambioInput = (event) => {
        this.props.onChange("archivoGrilla",event.target.value);
    }

    render (){
        return (
            <form className = {this.stateClassNameInput}  >
                <input name="Grilla" 
                    value={this.props.archivoGrilla} 
                    onChange={this.controlarCambioInput} 
                    placeholder = "Ingrese Grilla (.slt)" 
                />
            </form>
        );
    }  
}

export default Grilla;