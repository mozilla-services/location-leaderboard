window.onload = function () {
  var getAppAttr = function (attrName) {
      document.getElementById('leaderboard-container').getAttribute('data-' + attrName);
  };

  leaderboard.init({
    leafletJSUrl: getAppAttr('leaflet-js-url'),
    leafletGeometryJSUrl: getAppAttr('leaflet-geometry-js-url'),
    leafletCSSUrl: getAppAttr('leaflet-css-url'),
    countriesGeoUrl: getAppAttr('countries-geo-url'),
    countriesInfoUrl: getAppAttr('countries-info-url'),
    globalLeadersUrl: getAppAttr('global-leaders-url'),
    countryLeadersUrl: getAppAttr('country-leaders-url'),
    leaderProfileUrl: getAppAttr('leader-profile-url')
  });

  try {
    Tabzilla.disableEasterEgg()
  } catch (e) {
  }
}
