import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import s from './styles.css';
import {sendMessage} from "../../../../actions/actions";

class MessageInput extends React.Component {
    static propTypes = {
        text: PropTypes.func
    };

    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleKeyPressed = this.handleKeyPressed.bind(this);
        this.state = {value: ''};
    }

    handleChange(event) {
        this.setState({value: event.target.value});
    }

    handleSubmit() {
        if(this.state.value && this.state.value.trim().length > 0)
            this.props.sendMessage(this.state.value, this.props.selectedDriverId);
        this.setState({value: ''});
    }

    handleKeyPressed(context) {
        if (context.key === 'Enter') {
            this.handleSubmit();
        }
    }

    render() {
        return (
            <div className={s["input-container"]}>
                <textarea className={s["input-msg"]} value={this.state.value} onChange={this.handleChange} onKeyPress={this.handleKeyPressed}/>
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
        sendMessage: (message, toDriverId) => {
            dispatch(sendMessage(message, toDriverId))
        }
    };
};

export default connect(
    mapStateToProps,
    mapDispatchToProps,
)(MessageInput);