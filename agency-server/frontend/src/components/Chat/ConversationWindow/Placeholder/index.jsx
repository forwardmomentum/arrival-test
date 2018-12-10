import React from 'react';
import PropTypes from 'prop-types';
import s from './styles.css';
import connect from "react-redux/es/connect/connect";

class Placeholder extends React.Component {
    static propTypes = {
    };

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className={s["conv-placeholder"]}>
                Choose driver to communicate
            </div>
        );
    }
}

export default connect(
    null,
    null,
)(Placeholder);