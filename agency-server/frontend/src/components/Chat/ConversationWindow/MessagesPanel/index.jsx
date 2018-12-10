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
        this.currentSelectedDriverId = null;
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

    render() {
        return (
            <div className={s["message-panel-wrapper"]}>
                <button onClick={this.showAllClicked} className={s['show-all']}>Show all</button>
                <div className={s["message-panel"]} id={"message-panel"}>
                    {
                        this.props.messages.map(function (message, i) {
                            return <div className={s["message"]} key={message.message_id}>
                                <div className={s["message-time"]}>{new Date(message.sended_at).toLocaleTimeString()}</div>
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
        messages: state.drivers.find((driver) => state.selectedDriverId === driver.id).messages,
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