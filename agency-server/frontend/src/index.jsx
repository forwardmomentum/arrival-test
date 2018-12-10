import React from 'react';
import ReactDOM from 'react-dom';

import App from './components/App';

const __svg__ = {path: 'components/Common/Icon/icons/*.svg', name: 'sprite.svg'};
require('webpack-svgstore-plugin/src/helpers/svgxhr')(__svg__);

ReactDOM.render(
  <App/>,
  document.getElementById('app')
);