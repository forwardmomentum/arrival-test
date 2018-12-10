import {createStore, applyMiddleware} from 'redux';
import thunk from 'redux-thunk';
import errors from './errors';

import {
    getDriversList,
    getDriverWithHistoryShort,
    getLastMessages,
    getMessageHistory
} from '../api';

const store = createStore(
    (
        state = {
            drivers: [],
            selectedDriverId: null
        },
        action,
    ) => {
        switch (action.type) {
            case 'SET_DRIVERS': {
                return {
                    ...state,
                    drivers: action.data.map((driver) => {
                        driver.messages = [];
                        return driver;
                    })
                }
            }
            case 'SELECT_DRIVER':
                return {
                    ...state,
                    selectedDriverId: action.data,
                };
            case 'SET_MESSAGES': {
                let index = state.drivers.findIndex((driver) => action.data.driverId === driver.id);
                let drivers = state.drivers;
                drivers[index].messages = [...action.data.messages];
                console.log(drivers[index].messages);
                return {
                    ...state,
                    drivers: drivers
                }
            }
            default:
                return state;
        }
    },
    applyMiddleware(thunk),
);

export default store;

