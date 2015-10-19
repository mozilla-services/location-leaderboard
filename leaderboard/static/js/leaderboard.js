var Leaderboard = require('./react.leaderboard.js');

module.exports = function (config) {
  React.render(
    <Leaderboard config={config} />,
    document.getElementById('leaderboard-container')
  );
};
