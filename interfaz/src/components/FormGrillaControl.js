import React from 'react';

import ConGrilla from './Grilla';
import SinGrilla from './SinGrilla';


class FormGrillaControl extends React.Component{
    
    activarConGrilla = () => {
        this.props.onChange("datosGrilla","stateConGrilla",true);
    }

    activarSinGrilla = () =>{
        this.props.onChange("datosGrilla","stateConGrilla",false);
    }

    renderOpcionGrilla = () =>{
        if (this.props.stateConGrilla){
            return (
                <div>
                    <ConGrilla
                        archivoGrilla = {this.props.archivoGrilla}
                        onChange = {this.props.onChange}
                    />
                </div>
            );
        }
        console.log(this.props.stateConGrilla)
        return (
            <div>
                <SinGrilla
                    valorMinimoY = {this.props.valorMinimoY}
                    valorMaximoY = {this.props.valorMaximoY}
                    valorMinimoZ = {this.props.valorMinimoZ}
                    valorMaximoZ = {this.props.valorMaximoZ}
                    onChange = {this.props.onChange}
                />
            </div>
        );
    }

    render(){
        var itemConGrilla = "active item";
        var itemSinGrilla = "item";
        if (!this.props.stateConGrilla){
            itemConGrilla = "item";
            itemSinGrilla = "active item";
        }
        return (
            <div style={{display:'flex', flex:1, alignItems: 'center', justifyContent : 'center', flexDirection : 'column'}}>
                <div className="ui compact menu" style = {{marginBottom : 20}}>
                    <a className={itemConGrilla} href="#" onClick = {this.activarConGrilla}>Con Grilla</a>
                    <a className={itemSinGrilla} href="#" onClick = {this.activarSinGrilla} >Sin Grilla</a>
                </div>
                <div> {this.renderOpcionGrilla()} </div>
            </div>
        );
    }
}

export default FormGrillaControl;