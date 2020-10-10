import React from 'react';
import { Link } from 'react-router-dom';

class LinksDocumentos extends React.Component{

    state = {IsShow : false}

    showDescription = () =>{
        if (this.state.IsShow){
            return <div className="ui floating message">HOLA</div>;
        }
    }

    render(){
        return (
            <div>
                <Link 
                    to={{ pathname: this.props.direccion }} 
                    target="_blank" 
                    className ="button"
                    onMouseEnter={() => this.setState({IsShow:true})}
                    onMouseLeave={() => this.setState({IsShow:false})}>
                        {this.props.nombre}
                </Link>
                <div > {this.showDescription()} </div>
            </div>
        );
    }

}

export default LinksDocumentos;