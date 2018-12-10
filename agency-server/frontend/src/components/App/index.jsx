import React, {Component} from 'react';
import {BrowserRouter} from 'react-router-dom';
import {Provider} from 'react-redux';

import s from './styles.css';

import store from '../../store/store';

import Chat from '../Chat'

export default class App extends Component {
  constructor(props) {
    super(props);

  }

  render() {
    return (
      <Provider store={store}>
        <BrowserRouter basename="/">
          <div className={s.root}>
            {/*<TopLine />*/}
            <Chat />
            {/*<Footer/>*/}
          </div>
        </BrowserRouter>
      </Provider>
    );
  }
}
