import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import s from './styles.css';

class MessagePanel extends React.Component {
    static propTypes = {
        fetchDrivers: PropTypes.func
    };

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <div className={s["message-panel"]}>
                MESSAGES
                {/*{*/}
                    {/*this.props.drivers.map(function (driver, i) {*/}
                        {/*return  <span key={driver.id}>{driver.id}</span>*/}
                    {/*})*/}
                {/*}*/}

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
    };
};

export default connect(
    mapStateToProps,
    mapDispatchToProps,
)(MessagePanel);