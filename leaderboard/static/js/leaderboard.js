var Leaderboard = require('./react.leaderboard.js');

module.exports = function (config) {
  window.fetch(config.countriesInfoUrl).then(function (response) {
    return response.json();
  }).then(function (data) {

    config.countries = {};
    data.map(function(country) {
      config.countries[country.iso2] = country;
    });

    React.render(
      <Leaderboard config={config} />,
      document.getElementById('leaderboard-container')
    );
  });
};
