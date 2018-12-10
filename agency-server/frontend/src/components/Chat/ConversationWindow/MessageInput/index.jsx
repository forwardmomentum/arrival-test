import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import s from './styles.css';
// import {getDriversData} from "../../../actions/actions";

class MessageInput extends React.Component {
    static propTypes = {
        text: PropTypes.func
    };

    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.state = {value: ''};
    }

    handleChange(event) {
        this.setState({value: event.target.value});
    }

    handleSubmit(event) {
        if(this.state.value)
            console.log("TODO SEND MESSAGE")
    }

    render() {

        return (
            <div className={s["input-container"]}>
                <textarea className={s["input-msg"]} value={this.state.value} onChange={this.handleChange}/>
                <button className={s["send-btn"]} onClick={this.handleSubmit}>Send</button>
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
        fetchDrivers: () => {
            dispatch(getDriversData())
        }
    };
};

export default connect(
    null,
    null,
)(MessageInput);