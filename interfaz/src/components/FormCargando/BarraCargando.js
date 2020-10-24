import React from 'react';

const BarraCargando = () => {
    return (
        <div className="ui progress">
            <div className="bar">
                <div className="progress"></div>
            </div>
            <div className="label">Generando</div>
        </div>
    );
}
export default BarraCargando;