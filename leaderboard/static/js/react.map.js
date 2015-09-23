var dispatcher = require('./dispatcher.js');
var ReactScriptLoader = require('../lib/ReactScriptLoader/ReactScriptLoader.js');

module.exports = React.createClass({
  mixins: [ReactScriptLoader.ReactScriptLoaderMixin],

  getScriptURL: function () {
    return this.props.config.leafletJSUrl;
  },

  render: function() {
    return (
      <div>
        <link rel="stylesheet" href={this.props.config.leafletCSSUrl} />
        <div id="leaders-map"></div>
      </div>
    );
  },

  loadCountryBoundaries: function(map, popup) {
    var countryLeadersUrl = this.props.config.countryLeadersUrl;

    $.getJSON(
      this.props.config.countriesJSONUrl,
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

        var onEachFeature = function(country_data, layer) {
          layer.on('mouseover', function (e) {
            // change the countryStyle to the hover version
            layer.setStyle(countryStyleHover);
          });

          layer.on('mouseout', function (e) {
            // reverting the countryStyle back
            layer.setStyle(countryStyle);
          });

          layer.on('click', function (e) {
            map.closePopup(popup);

            var countryIso2 = e.target.feature.properties.alpha2;
            var countryName = e.target.feature.properties.name;
            var dataUrl = countryLeadersUrl.replace('XX', countryIso2);
            dispatcher.fire('updateUrl', {
              url: dataUrl,
              name: countryName,
            });
          });
        };

        L.geoJson(
          data, {
            onEachFeature: onEachFeature,
            style: countryStyle
          }
        ).addTo(map);
      }
    );
  },

  onScriptLoaded: function () {
    var map = L.map('leaders-map', {
      closePopupOnClick: true,
      maxBounds: L.latLngBounds(
        L.latLng(-85.0511, -180.0),
        L.latLng(85.0511, 180.0)
      )
    }).setView([30, 0], 2);

    var tilesUrl = 'https://{s}.tiles.mapbox.com/v4/mozilla-webprod.g7ilhcl5/{z}/' +
      '{x}/{y}.png?access_token=pk.eyJ1IjoibW96aWxsYS13ZWJwcm9kIiwiYSI6Im5ZW' +
      'UpCb3MifQ.06LZyRt2m_MlRKsKU0gBLA';

    L.tileLayer(tilesUrl, {
      attribution: '<a href="https://www.mapbox.com/about/maps">© Mapbox</a> ' +
        '<a href="http://openstreetmap.org/copyright">© OpenStreetMap</a>' +
        '<a href="http://mapbox.com/map-feedback/" class="mapbox-improve-map">' +
        'Improve this map</a>',
      maxZoom: 18,
      minZoom: 2
    }).addTo(map);

    var popup = L.popup().setLatLng(L.latLng(20, 0)).setContent(
      '<h3 class="center">Click on a country to see its local ' +
      'leaderboard!</h3>'
    ).openOn(map);

    this.loadCountryBoundaries(map, popup);
  },

  onScriptError: function () {
  }
});
