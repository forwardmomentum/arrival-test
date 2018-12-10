import {getDriversList, getLastMessages} from "api";

export function getDriversData() {
    return (dispatch) => {
        getDriversList()
            .then(res => {
                if (res.status !== 200) {
                    return;
                }

                console.log('[DRIVERS DATA]', res);

                dispatch({
                    type: 'SET_DRIVERS',
                    data: res.data
                });
            })
            .then(() => {
                return getLastMessages();
            })
            .then(res => {
                console.log("[LAST MESSAGES]", res);
            })
            .catch(err => {
                console.error(`[ERROR] ${err}`);
            });
    };
}

export function selectDriver(driverId) {
    return (dispatch) => {
        dispatch({
            type: "SELECT_DRIVER",
            data: driverId
        })
    }
}