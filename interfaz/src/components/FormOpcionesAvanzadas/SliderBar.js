import React from 'react';
import Slider from '@material-ui/core/Slider';

class SliderBar extends React.Component{
    state = {
        value : 0
    }

    valuetext = (value) => {
        return `${value}°C`;
    };

    controlarCambio = (event, value) =>{
        this.props.onChange("opAv_DistCaracteristica","opAv_DistCaracteristica", value)
    }

    render(){
        
        return (
            <div>
                <label>Distancia Caracteristica</label>
                <Slider
                    defaultValue={this.props.opAv_DistCaracteristica}
                    getAriaValueText={this.valuetext}
                    aria-labelledby="discrete-slider"
                    valueLabelDisplay="auto"
                    step={0.1}
                    marks
                    min={0.1}
                    max={1}
                    value = {this.props.opAv_DistCaracteristica}
                    onChange={this.controlarCambio}
                />
            </div>
            
        );
    }

}

export default SliderBar;