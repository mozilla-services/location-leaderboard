var Leaderboard = require('./react.leaderboard.js');

module.exports = function (config) {
  React.render(
    <Leaderboard
      globalUrl={config.globalUrl}
      countriesJSONUrl={config.countriesJSONUrl}
    />,
    document.getElementById('leaderboard-container')
  );
};
