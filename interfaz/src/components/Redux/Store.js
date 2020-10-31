import {createStore, combineReducers} from 'redux';

import DatosIniciar from './reducers/DatosIniciar'

const reducers = combineReducers({
    DatosIniciar
});

const Store = createStore(reducers);

export default Store;