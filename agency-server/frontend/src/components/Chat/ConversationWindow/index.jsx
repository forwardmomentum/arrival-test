import React from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import s from './styles.css';
import DriverInfoHeader from './DriverInfoHeader'
import MessageInput from './MessageInput'
import Placeholder from './Placeholder'
import MessagePanel from "components/Chat/ConversationWindow/MessagesPanel";

class ConversationWindow extends React.Component {
    static propTypes = {
        fetchDrivers: PropTypes.func,
    };

    constructor(props) {
        super(props);
    }

    render() {
        return (

            <div className={s["cw-container"]}>
                {
                    !!this.props.selectedDriverId && (
                        <React.Fragment>
                            <DriverInfoHeader
                                driverInfo={this.props.drivers.find((driver) => driver.id === this.props.selectedDriverId)}/>
                            <MessagePanel/>
                            <MessageInput/>
                        </React.Fragment>
                    )
                }
                {
                    !this.props.selectedDriverId && (
                        <Placeholder/>
                    )
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
    return {};
};

export default connect(
    mapStateToProps,
    mapDispatchToProps,
)(ConversationWindow);