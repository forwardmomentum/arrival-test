const path = require('path');

const HtmlWebPackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const SvgStore = require('webpack-svgstore-plugin');
const src = path.join(__dirname, 'src');

const appConfig = {
  name: 'app',
  mode: 'development',
  node: {
    fs: 'empty'
  },
  resolve: {
    extensions: ['.js', '.jsx', '.css'],
    alias: {
      components: path.join(src, 'components'),
      api: path.join(src, 'api'),
      store: path.join(src, 'store'),
      lib: path.join(src, 'lib'),
      services: path.join(src, 'services')
    }
  },
  optimization: {
    splitChunks: {
      cacheGroups: {
        styles: {
          name: 'styles',
          test: /\.css$/,
          chunks: 'all',
          enforce: true
        }
      }
    }
  },
  entry: './src/index.jsx',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.[contenthash].js',
    publicPath: '/'
  },
  devServer: {
    contentBase: path.join(__dirname, 'dist'),
    compress: true,
    port: 5000,
    publicPath: '/',
    historyApiFallback: true,
    proxy: {
      '/api': 'http://localhost:9001'
    }
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: 'babel-loader'
      },
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          // 'css-loader'
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              sourceMap: true,
              modules: true,
              localIdentName: '[local]___[hash:base64:5]'
            }
          }
        ]
      },
      {
        test: /\.(png|jpg|gif|svg|eot|ttf|woff|woff2)$/,
        loader: 'url-loader',
        options: {
          limit: 10000
        }
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name].css' //.[contenthash].css
    }),
    new HtmlWebPackPlugin({
      template: './src/index.html',
      filename: './index.html'
    }),
    new SvgStore({
      svgoOptions: {
        plugins: [
          {removeTitle: true},
          {removeUselessStrokeAndFill: false}
        ]
      },
      prefix: 'icon-'
    })
  ]
};


module.exports = [
  appConfig,
];