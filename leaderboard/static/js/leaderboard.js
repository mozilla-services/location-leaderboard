var Leaderboard = require('./react.leaderboard.js');

module.exports = function (config) {
  React.render(
    <Leaderboard globalUrl={config.globalUrl} />,
    document.getElementById('leaderboard-container')
  );
};
