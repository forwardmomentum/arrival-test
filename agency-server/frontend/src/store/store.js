import {createStore, applyMiddleware} from 'redux';
import thunk from 'redux-thunk';
import websocket from '@giantmachines/redux-websocket'
import errors from './errors';

import {
    getDriversList,
    getDriverWithHistoryShort,
    getLastMessages,
    getMessageHistory
} from '../api';
import {WEBSOCKET_MESSAGE} from "@giantmachines/redux-websocket";

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
                        driver.blinking = false;
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
                let drivers = [...state.drivers];
                drivers[index].messages = [...action.data.messages].sort((a, b) => {
                    return new Date(a.sended_at) - new Date(b.sended_at);
                });
                return {
                    ...state,
                    drivers: drivers
                }
            }
            case WEBSOCKET_MESSAGE: {
                let wsMessage = JSON.parse(action.payload.data);
                if (wsMessage.message_id) {
                    let driverId = wsMessage.to_id === 1 ? wsMessage.from_id : wsMessage.to_id;
                    let index = state.drivers.findIndex((driver) => driverId === driver.id);
                    if (!state.drivers[index].messages.find((message) => message.message_id === wsMessage.message_id)) {
                        let drivers = [...state.drivers];
                        drivers[index].messages.push(wsMessage);
                        if (drivers[index].id !== state.selectedDriverId) drivers[index].blinking = true;
                        return {
                            ...state,
                            drivers: drivers
                        }
                    }
                }
                else {
                    let receivedId = wsMessage.received_id;
                    var drivers = [...state.drivers];
                    drivers = drivers.map((driver) => {
                        driver.messages = driver.messages.map((message) => {
                            if (message.message_id === receivedId) message.received = true;
                            return message;
                        });
                        return driver;
                    });
                    return {
                        ...state,
                        drivers: drivers
                    }
                }
                return {
                    ...state
                }
            }
            case 'STOP_BLINKING': {
                let drivers = [...state.drivers];
                let index = drivers.findIndex((driver) => action.driverId === driver.id);
                drivers[index].blinking = false;
                return {
                    ...state,
                    drivers: drivers
                }
            }
            default:
                return state;
        }
    },
    applyMiddleware(thunk, websocket),
);

export default store;

