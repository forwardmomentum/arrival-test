import React from 'react';
import {connect} from 'react-redux';
import s from './styles.css';
import DriverRow from './DriverRow';
import {selectDriver} from "../../../actions/actions";

class DriversList extends React.Component {
    static propTypes = {};

    constructor(props) {
        super(props);
        this.onClick = this.onClick.bind(this);
    }

    onClick(driverId) {
        this.props.selectDriver(driverId);
    }

    render() {
        return (
            <div className={s["drivers-list-container"]}>
                {
                    this.props.drivers.map((driver) => {
                        return <DriverRow clicked={this.onClick} driverName={driver.name}
                                          // lastMessage={driver.messages.length > 0 ? driver.messages[driver.messages.length - 1].body : "No mesages yet"}
                                          lastMessage={"Click for dialog"}
                                          key={driver.id} driverId={driver.id}
                                          selected={this.props.selectedDriverId === driver.id}/>
                    })
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
        selectDriver: (driverId) => {
            dispatch(selectDriver(driverId))
        }
    };
};

export default connect(
    mapStateToProps,
    mapDispatchToProps,
)(DriversList);