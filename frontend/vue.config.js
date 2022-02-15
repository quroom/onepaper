const BundleTracker = require("webpack-bundle-tracker");
const HardSourceWebpackPlugin = require("hard-source-webpack-plugin");
const SpeedMeasurePlugin = require("speed-measure-webpack-plugin");

const mode = process.argv[4];

module.exports = {
  // on Windows you might want to set publicPath: "http://127.0.0.1:5050/"
  // To access site from outside. publicPath(Public IP): "http://125.183.143.159:5050/",
  publicPath: process.env.NODE_ENV === "production" ? "/static/" : "http://127.0.0.1:5050/",
  outputDir: "./dist/",
  chainWebpack: (config) => {
    if (mode == "dev") {
      const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;
      config.plugin("BundleAnalyzerPlugin").use(BundleAnalyzerPlugin);
      config.plugin("SpeedMeasurePlugin").use(SpeedMeasurePlugin);
    }
    config.plugin("BundleTracker").use(BundleTracker, [{ filename: "./webpack-stats.json" }]);
    config.plugin("HardSourceWebpackPlugin").use(HardSourceWebpackPlugin);
    config.module
      .rule("eslint")
      .use("eslint-loader")
      .tap((opts) => ({ ...opts, failOnError: true, failOnWarning: true }));
    config.optimization.splitChunks(false);

    config.output.filename("bundle.js");

    config.resolve.alias.set("__STATIC__", "static");

    config.devServer
      // the first 3 lines of the following code have been added to the configuration
      .public("http://127.0.0.1:5050")
      // .host("localhost")
      .port(5050)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .disableHostCheck(true)
      .headers({ "Access-Control-Allow-Origin": ["*"] });
  },
  transpileDependencies: ["vuetify"],

  // uncomment before executing 'npm run build'
  css: {
    loaderOptions: {
      sass: {
        prependData: "@import '@/sass/variables.scss'"
      }
    },
    extract: {
      filename: "bundle.css"
    }
  }
};
