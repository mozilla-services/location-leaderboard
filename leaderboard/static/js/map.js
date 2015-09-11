var leaders = require('./leaders.js');

function setupMap() {
  var map = L.map('map', {
    maxBounds: L.latLngBounds(
      L.latLng(-85.0511, -180.0),
      L.latLng(85.0511, 180.0)
    )
  }).setView([30, 0], 2);

  var src = 'https://{s}.tiles.mapbox.com/v4/mozilla-webprod.g7ilhcl5/{z}/' +
    '{x}/{y}.png?access_token=pk.eyJ1IjoibW96aWxsYS13ZWJwcm9kIiwiYSI6Im5ZW' +
    'UpCb3MifQ.06LZyRt2m_MlRKsKU0gBLA';
  L.tileLayer(src, {
    attribution: '<a href="https://www.mapbox.com/about/maps">© Mapbox</a> ' +
      '<a href="http://openstreetmap.org/copyright">© OpenStreetMap</a>' +
      '<a href="http://mapbox.com/map-feedback/" class="mapbox-improve-map">' +
      'Improve this map</a>',
    maxZoom: 18,
    minZoom: 2
  }).addTo(map);

  var popup = L.popup()
      .setLatLng(L.latLng(20, 0))
      .setContent(
        '<h3 class="center">Click on a country to see its local ' +
        'leaderboard!</h3>'
      )
      .openOn(map);

  $.getJSON(
    'https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/' +
    'master/countries.geojson',
    function (data) {
      var countryStyle = {
        'fillOpacity': 0,
        'opacity': 0
      };

      var countryStyleHover = {
        'weight': 1,
        'opacity': 1
      };

      var countryStyleClick = {
      };

      function onEachFeature(country_data, layer) {
        layer.on('mouseover', function (e) {
          // change the countryStyle to the hover version
          layer.setStyle(countryStyleHover);
        });

        layer.on('mouseout', function (e) {
          // reverting the countryStyle back
          layer.setStyle(countryStyle);
        });

        layer.on('click', function (e) {
          var countryIso2 = e.target.feature.properties.iso_a2;
          var countryName = e.target.feature.properties.name;
          var dataUrl = '/api/v1/leaders/country/' + countryIso2 + '/';
          leaders.requestUrl(dataUrl, countryName);
        });
      }
      L.geoJson(
        data, {
          onEachFeature: onEachFeature,
          style: countryStyle
        }
      ).addTo(map);
    }
  );
}

module.exports = {
  init: function (config) {
    setupMap();
  }
};
