import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import s from './styles.css';
import {stopBlinking} from "../../../../actions/actions";

class DriverRow extends React.Component {
    static propTypes = {
        driverName: PropTypes.string,
        lastMessage: PropTypes.string,
        selected: PropTypes.bool,
        driverId: PropTypes.number,
        blinking: PropTypes.bool,
        clicked: PropTypes.func
    };

    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(){
        this.props.clicked(this.props.driverId)
    }

    get blinking () {
        return this.props.drivers.find((driver) => this.props.driverId === driver.id).blinking;
    }

    componentWillReceiveProps(willProps) {
        let willBlinkedValue = willProps.drivers.find((driver) => this.props.driverId === driver.id).blinking;
        let currentBlinkingValue = this.blinking;
        if(willBlinkedValue) {
            setTimeout(() => this.props.stopBlinking(this.props.driverId), 3500);
        }
    }

    render() {
        return (
            <div onClick={this.handleClick}  className={s["driver-row-container"] + " "
            + (this.props.selected ? s['selected'] : '') + ' ' + (this.blinking ? s.blinked : '')}>
                <div className={s["driver-name"]}>{this.props.driverName}</div>
                {
                    !!this.props.lastMessage && <div className={s["last-message"]}>{this.props.lastMessage}</div>
                }
            </div>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        drivers: state.drivers,
        selectedDriverId: state.selectedDriverId
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        stopBlinking: (driverId) => {
            dispatch(stopBlinking(driverId))
        }
    };
};

export default connect(
    mapStateToProps,
    mapDispatchToProps,
)(DriverRow);