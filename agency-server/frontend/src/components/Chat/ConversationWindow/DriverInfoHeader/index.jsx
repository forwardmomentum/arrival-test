import React from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import s from './styles.css';

// import {getDriversData} from "../../../actions/actions";

class DriverInfoHeader extends React.Component {
    static propTypes = {
        driverInfo: PropTypes.object
    };

    constructor(props) {
        super(props);
        this.online = this.online.bind(this);
    }

    online() {
        // todo check schedule and current time
        return false;
    }

    render() {
        return (
            <div className={s["driver-info-container"]}>
                <div className={s["first-row"]}>
                    {!!this.online() && <div className={s.status}>online</div>}
                    {!this.online() && <div className={s.status}>offline</div>}
                    <div className={s.name}>{this.props.driverInfo.name}</div>
                </div>

            </div>
        );
    }
}

export default connect(
    null,
    null,
)(DriverInfoHeader);