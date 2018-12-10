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
                console.log("SETTING");
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
            default:
                return state;
        }
    },
    applyMiddleware(thunk),
);

export default store;

