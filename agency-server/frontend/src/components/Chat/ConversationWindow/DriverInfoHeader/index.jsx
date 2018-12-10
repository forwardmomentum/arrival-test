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
        let ws = new Date("2000-01-01T" + this.props.driverInfo.working_day_start); // dirty trick to read time
        let wf = new Date("2000-01-01T" + this.props.driverInfo.working_day_finish);
        let ls = new Date("2000-01-01T" + this.props.driverInfo.launch_rest_start);
        let lf = new Date("2000-01-01T" + this.props.driverInfo.launch_rest_stop);
        let rs1 = new Date("2000-01-01T" + this.props.driverInfo.first_rest_start);
        let rf1 = new Date("2000-01-01T" + this.props.driverInfo.first_rest_stop);
        let rs2 = new Date("2000-01-01T" + this.props.driverInfo.second_rest_start);
        let rf2 = new Date("2000-01-01T" + this.props.driverInfo.second_rest_stop);
        let rs3 = new Date("2000-01-01T" + this.props.driverInfo.third_rest_start);
        let rf3 = new Date("2000-01-01T" + this.props.driverInfo.third_rest_stop);
        let currentTime = new Date();
        currentTime.setFullYear(2000, 0, 1);
        if (ws < currentTime < wf) {
            if (ls < currentTime < lf) return false;
            if (rs1 < currentTime < rf1) return false;
            if (rs2 < currentTime < rf2) return false;
            if (rs3 < currentTime < rf3) return false;
            return true;
        }
        return false;
    }

    prettyTime(timestr) {
        return timestr.substring(0, timestr.length - 3);
    }

    render() {
        return (
            <div className={s["driver-info-container"]}>
                <div className={s["first-row"]}>
                    {!!this.online() && <div className={s.status}>online</div>}
                    {!this.online() && <div className={s.status}>offline</div>}
                    <div className={s.name}>{this.props.driverInfo.name}</div>
                </div>
                <div className={s["second-row"]}>
                    <div className={s["second-item"]}>{this.props.driverInfo.birthdate}</div>
                    <div className={s["second-item"]}>{this.props.driverInfo.email}</div>
                    <div>{this.props.driverInfo.phone}</div>
                </div>
                <div className={s["schedule-row"]}>
                    <div className={s["schedule-subrow"]}>
                        <span>Working: </span>
                        <span>{this.prettyTime(this.props.driverInfo.working_day_start)} - {this.prettyTime(this.props.driverInfo.working_day_finish)}
                            </span>
                    </div>
                    <div className={s["schedule-subrow"]}>
                        <span>Launch: </span>
                        <span>{this.prettyTime(this.props.driverInfo.launch_rest_start)} - {this.prettyTime(this.props.driverInfo.launch_rest_stop)}
                            </span>
                    </div>
                    <div className={s["schedule-subrow"]}>
                        <span>Rests:</span>
                        <span
                            className={s["rest-time"]}>{this.prettyTime(this.props.driverInfo.first_rest_start)}-{this.prettyTime(this.props.driverInfo.first_rest_stop)}
                            </span>
                        <span
                            className={s["rest-time"]}>{this.prettyTime(this.props.driverInfo.second_rest_start)}-{this.prettyTime(this.props.driverInfo.second_rest_stop)}
                            </span>
                        <span
                            className={s["rest-time"]}>{this.prettyTime(this.props.driverInfo.third_rest_start)}-{this.prettyTime(this.props.driverInfo.third_rest_stop)}
                            </span>
                    </div>

                </div>

            </div>
        );
    }
}

export default connect(
    null,
    null,
)(DriverInfoHeader);