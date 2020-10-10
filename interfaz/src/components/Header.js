import React from 'react';

import ModalComponent from './FormDocumentos/ModalComponent';

const Header = () => {
    return (
        <div className = "ui secondary pointing menu">
            <div >
                Proyecto FInal de Carrera
            </div>
            <div className = "right menu" >
                <ModalComponent />
            </div>
        </div>
    );
};

export default Header;