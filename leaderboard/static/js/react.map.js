var dispatcher = require('./dispatcher.js');
var ReactScriptLoader = require('../lib/ReactScriptLoader/ReactScriptLoader.js');

// Style constants
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

var countryStyleSelected = {
  'fillOpacity': 0.3,
  'opacity': 0.3,
  'weight': 0
};

module.exports = React.createClass({
  mixins: [ReactScriptLoader.ReactScriptLoaderMixin],

  map: null,
  popup: null,

  getScriptURL: function () {
    return this.props.config.leafletJSUrl;
  },

  countryLayers: {},

  updateSelectedCountry: function (newSelection) {
    var oldSelection = this.props.selection;
    var oldSelectedLayer = this.countryLayers[oldSelection.iso2];
    if (oldSelectedLayer !== undefined) {
      oldSelectedLayer.setStyle(countryStyleFilled);
    }

    var newSelectedLayer = this.countryLayers[newSelection.iso2];
    if (newSelectedLayer !== undefined) {
      newSelectedLayer.setStyle(countryStyleSelected);
      this.map.fitBounds(newSelectedLayer.getLatLngs());
    } else {
      this.map.fitWorld();
    }
  },

  componentWillReceiveProps: function (newProps) {
    this.updateSelectedCountry(newProps.selection);
  },

  render: function () {
    return (
      <div>
        <link rel="stylesheet" href={this.props.config.leafletCSSUrl} />
        <div id="leaders-map"></div>
      </div>
    );
  },

  loadCountryBoundaries: function () {
    var onEachFeature = function (countryShapeInfo, layer) {
      var countryInfo = this.props.config.countries[countryShapeInfo.properties.alpha2];

      if (countryInfo === undefined) {
        return;
      }

      this.countryLayers[countryInfo.iso2] = layer;

      layer.setStyle(countryStyleFilled);

      var currentStyle;

      layer.on('mouseover', function (e) {
        layer.setStyle(countryStyleHover);
      });

      layer.on('mouseout', function (e) {
        if (countryInfo.iso2 === this.props.selection.iso2) {
          layer.setStyle(countryStyleSelected);
        } else {
          layer.setStyle(countryStyleFilled);
        }
      }.bind(this));

      layer.on('click', function (e) {
        this.map.closePopup(this.popup);

        dispatcher.fire('updateSelection', {
          url: countryInfo.leaders_url,
          name: countryInfo.name,
          iso2: countryInfo.iso2
        });
      }.bind(this));
    }.bind(this);

    window.fetch(this.props.config.countriesJSONUrl).then(function (response) {
      return response.json()
    }).then(function (data) {
      L.geoJson(
        data, {
          onEachFeature: onEachFeature,
          style: countryStyleEmpty
        }
      ).addTo(this.map);
    }.bind(this));
  },

  onScriptLoaded: function () {
    this.map = L.map('leaders-map', {
      closePopupOnClick: true,
      maxBounds: L.latLngBounds(
        L.latLng(-85.0511, -190.0),
        L.latLng(85.0511, 190.0)
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
    }).addTo(this.map);

    this.popup = L.popup().setLatLng(L.latLng(20, 0)).setContent(
      '<h3 class="center">Click on a country to see its local ' +
      'leaderboard!</h3>'
    ).openOn(this.map);

    this.loadCountryBoundaries();
  },

  onScriptError: function () {
  }
});
