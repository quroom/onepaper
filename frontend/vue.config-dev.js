const BundleTracker = require("webpack-bundle-tracker");
const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;

module.exports = {
  // on Windows you might want to set publicPath: "http://127.0.0.1:5050/"
  // publicPath: "http://125.183.143.159:5050/",
  publicPath: process.env.NODE_ENV === "production" ? "/static/" : "http://124.63.4.136:5050/",
  outputDir: "./dist/",
  chainWebpack: (config) => {
    config.resolve.extensions.add(".ts");
    config.module
      .rule("eslint")
      .use("eslint-loader")
      .options({ quiet: true });
    config.plugin("BundleAnalyzerPlugin").use(BundleAnalyzerPlugin);
    config.plugin("BundleTracker").use(BundleTracker, [{ filename: "./webpack-stats.json" }]);

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
  lintOnSave: true,

  // uncomment before executing 'npm run build'
  css: {
    extract: {
      filename: "bundle.css"
    }
  }
};
