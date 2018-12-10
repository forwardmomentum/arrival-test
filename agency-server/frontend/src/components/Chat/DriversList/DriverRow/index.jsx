import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import s from './styles.css';
// import {getDriversData} from "../../../actions/actions";

class DriverRow extends React.Component {
    static propTypes = {
        driverName: PropTypes.string,
        lastMessage: PropTypes.string,
        selected: PropTypes.bool,
        driverId: PropTypes.number,
        blink: PropTypes.bool,
        clicked: PropTypes.func
    };

    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(){
        this.props.clicked(this.props.driverId)
    }

    render() {
        return (
            <div onClick={this.handleClick}  className={s["driver-row-container"] + " " + (this.props.selected ? s['selected'] : '')}>
                <div className={s["driver-name"]}>{this.props.driverName}</div>
                {
                    !!this.props.lastMessage && <div className={s["last-message"]}>{this.props.lastMessage}</div>
                }
            </div>
        );
    }
}

export default DriverRow;