import React from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import s from './styles.css';
import {loadShortHistory, loadAllHistory} from "../../../../actions/actions";

class MessagePanel extends React.Component {
    static propTypes = {
        loadShortHistory: PropTypes.func
    };

    constructor(props) {
        super(props);
        this.showAllClicked = this.showAllClicked.bind(this);
    }

    componentDidMount() {
        this.props.loadShortHistory(this.props.selectedDriverId);
    }

    componentDidUpdate(state, prevState, prevContext) {
        var element = document.getElementById("message-panel");
        element.scrollTop = element.scrollHeight;
    }

    componentWillReceiveProps(props) {
        if (props.selectedDriverId !== this.props.selectedDriverId) {
            this.props.loadShortHistory(props.selectedDriverId);
        }
    }

    showAllClicked() {
        this.props.loadAllHistory(this.props.selectedDriverId);
    }

    get messages() {
        return this.props.drivers.find((driver) => this.props.selectedDriverId === driver.id).messages;
    }

    get driverName() {
        return this.props.drivers.find((driver) => this.props.selectedDriverId === driver.id).name;
    }

    render() {
        let driverName = this.driverName;
        return (
            <div className={s["message-panel-wrapper"]}>
                <button onClick={this.showAllClicked} className={s['show-all']}>Show all</button>
                <div className={s["message-panel"]} id={"message-panel"}>
                    {
                        this.messages.map(function (message, i) {
                            return <div className={s["message"] + " " + (message.from_id === 1 ? s["message-out"] : '')}
                                        key={message.message_id}>
                                <div
                                    className={s["message-time"]}>{message.to_id === 1 ? driverName : 'you'} {new Date(message.sended_at).toLocaleTimeString()}
                                    {
                                        !!message.received && (<i className={s.icon + " fas fa-check"}></i>)
                                    }
                                    {
                                        !message.received && (<i className={s.icon + " far fa-clock"}></i>)
                                    }
                                    </div>
                                <div className={s["message-body"]}>{message.body}</div>
                            </div>
                        })
                    }
                </div>
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
        loadShortHistory: (driverId) => {
            dispatch(loadShortHistory(driverId))
        },
        loadAllHistory: (driverId) => {
            dispatch(loadAllHistory(driverId))
        }
    };
};

export default connect(
    mapStateToProps,
    mapDispatchToProps,
)(MessagePanel);