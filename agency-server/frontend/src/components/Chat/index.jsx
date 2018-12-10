import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import s from './styles.css';
import {getDriversData} from "../../actions/actions";
import DriversList from "components/Chat/DriversList";
import ConversationWindow from "components/Chat/ConversationWindow";

class Chat extends React.Component {
    static propTypes = {
        fetchDrivers: PropTypes.func,
    };

    constructor(props) {
        super(props);

        // this.clicked = this.clicked.bind(this);
    }

    handleLoginChange(value) {
        this.setState({
            login: value,
        });
    }

    componentDidMount() {
        this.props.fetchDrivers();
    }

    render() {

        return (
            <div className={s["chat-container"]}>
                <DriversList/>
                <ConversationWindow/>
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
    mapStateToProps,
    mapDispatchToProps,
)(Chat);