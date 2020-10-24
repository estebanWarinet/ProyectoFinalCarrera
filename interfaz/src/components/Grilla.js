import React from 'react';

//import ApiAddress from './Api/Api';


class Grilla extends React.Component {

    componentDidMount(){
        this.props.onChange("datosGrilla","valorMinimoY","")
        this.props.onChange("datosGrilla","valorMaximoY","")
        this.props.onChange("datosGrilla","valorMinimoZ","")
        this.props.onChange("datosGrilla","valorMaximoZ","")
    }

    controlarCambioInput = (event) => {
        //let data = new FormData();
        //data.append('file', event.target.files[0])
        let data =  event.target.files[0]

        this.props.onChange("datosGrilla","archivoGrilla",data);
    }

    //controlarCambioInput = (event) => {
    //    console.log(event.target.files)
    //    let data = new FormData();
    //    data.append('file', event.target.files[0])
    //    this.props.onChange("archivoGrilla",data);
    //    const options = {
    //        onUploadProgress : (progressEvent) => {
    //            const {loaded,total} = progressEvent;
    //            let percent = Math.floor((loaded*100)/total)
    //            console.log(`${loaded}kb of ${total} | ${percent}%`);
    //        }
    //    }
//
    //    ApiAddress.post('/DatosEntrada',data).then( res => {console.log(res)})
    //}

    render (){
        return (
            <form className = {this.stateClassNameInput}  >
                <input name="Grilla" 
                    type="file" id="input"
                    //value={this.props.archivoGrilla} 
                    onChange={this.controlarCambioInput} 
                    placeholder = "Ingrese Grilla (.slt)" 
                />
            </form>
        );
    }  
}

export default Grilla;