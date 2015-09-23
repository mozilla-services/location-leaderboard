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
    var selectedCountry;

    var countryStyleEmpty = {
      'fillOpacity': 0,
      'opacity': 0,
      'weight': 0
    };

    var countryStyleFilled = {
      'fillOpacity': 0.1,
      'opacity': 0,
      'weight': 0
    };

    var countryStyleHover = {
      'weight': 1,
      'opacity': 1
    };

    var countryStyleClick = {
      'fillOpacity': 0.3,
      'opacity': 0.3,
      'weight': 0
    };

    var onEachFeature = function(countryShapeInfo, layer) {
      var countryInfo = this.props.config.countries[countryShapeInfo.properties.alpha2];

      if (countryInfo !== undefined) {
        layer.setStyle(countryStyleFilled);

        layer.on('mouseover', function (e) {
          // change the countryStyle to the hover version
          layer.setStyle(countryStyleHover);
        });

        layer.on('mouseout', function (e) {
          // reverting the countryStyle back
          if (layer !== selectedCountry) {
            layer.setStyle(countryStyleFilled);
          } else if (selectedCountry !== undefined) {
            selectedCountry.setStyle(countryStyleClick);
          }
        });

        layer.on('click', function (e) {
          if (selectedCountry && layer !== selectedCountry) {
            selectedCountry.setStyle(countryStyleFilled);
          }
          map.closePopup(popup);
          layer.setStyle(countryStyleClick);
          selectedCountry = layer;

          dispatcher.fire('updateUrl', {
            url: countryInfo.leaders_url,
            name: countryInfo.name
          });
        });
      }
    }.bind(this);

    window.fetch(this.props.config.countriesJSONUrl).then(function(response) {
      return response.json()
    }).then(function(data) {
      L.geoJson(
        data, {
          onEachFeature: onEachFeature,
          style: countryStyleEmpty
        }
      ).addTo(map);
    });
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
