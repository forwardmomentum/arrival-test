import axios from 'axios';

/**
 * get drivers list
 */
export function getDriversList() {
    return axios.get('/api/drivers');
}

/**
 * get last 100 messages list
 */
export function getLastMessages() {
    return axios.get('/api/messages');
}

/**
 * get driver info with short history
 */
export function getDriverWithHistoryShort(driverId) {
    return axios.get('/api/drivers/' + driverId);
}

/**
 * get all message history for driver
 */
export function getMessageHistory(driverId) {
    return axios.get('/api/drivers/' + driverId + '/history');
}
