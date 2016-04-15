/*global React L*/

var dispatcher = require("./dispatcher.js");
var cachedFetch = require("./cachedfetch.js");
var promisescript = require("promisescript");

// Style constants
var countryStyleEmpty = {
  "fillOpacity": 0,
  "opacity": 0,
  "weight": 0
};

var countryStyleFilled = {
  "fillOpacity": 0.1,
  "opacity": 0,
  "weight": 0
};

var countryStyleHover = {
  "weight": 1,
  "opacity": 1
};

var countryStyleSelected = {
  "fillOpacity": 0.3,
  "opacity": 0.3,
  "weight": 0
};

// Map content constants
var tilesUrl = "https://{s}.tiles.mapbox.com/v4/mozilla-webprod.g7ilhcl5/{z}/" +
  "{x}/{y}.png?access_token=pk.eyJ1IjoibW96aWxsYS13ZWJwcm9kIiwiYSI6Im5ZW" +
  "UpCb3MifQ.06LZyRt2m_MlRKsKU0gBLA";

var mapAttribution= "<a href=\"https://www.mapbox.com/about/maps\">© Mapbox</a> " +
  "<a href=\"http://openstreetmap.org/copyright\">© OpenStreetMap</a>" +
  "<a href=\"http://mapbox.com/map-feedback/\" class=\"mapbox-improve-map\">" +
  "Improve this map</a>";

var popupContent = "<h3 class=\"center\">Click on a country to see its local " +
  "leaderboard!</h3>";

var LeaderMap = React.createClass({
  map: null,
  popup: null,
  mapReady: null,
  countryLayers: {},

  componentWillMount: function () {
    var javascriptLoaded = promisescript({
      url: this.props.leafletJSUrl,
      type: "script"
    }).then(() =>
      promisescript({
        url: this.props.leafletGeometryJSUrl,
        type: "script"
      })
    );

    var geoJsonLoaded = cachedFetch.set("countriesGeo", this.props.countriesGeoUrl);

    var countriesInfoLoaded = cachedFetch.get("countriesInfo");

    this.mapReady = Promise.all([javascriptLoaded, geoJsonLoaded, countriesInfoLoaded]).then((results) => {
      var countriesGeo = results[1];
      var countriesInfo = results[2];

      this.map = L.map("leaders-map", {
        closePopupOnClick: true,
        maxBounds: L.latLngBounds(
          L.latLng(-85.0511, -190.0),
          L.latLng(85.0511, 190.0)
        )
      }).setView([30, 0], 2);

      L.tileLayer(tilesUrl, {
        attribution: mapAttribution,
        maxZoom: 18,
        minZoom: 2
      }).addTo(this.map);

      this.popup = L.popup().setLatLng(L.latLng(20, 0)).setContent(popupContent).openOn(this.map);

      var onEachFeature = (countryShapeInfo, layer) => {
        var countryIso2 = countryShapeInfo.properties.alpha2;
        var countryHasData = countriesInfo[countryIso2] !== undefined;

        this.countryLayers[countryIso2] = layer;

        if (countryHasData) {
          layer.setStyle(countryStyleFilled);

          layer.on("mouseover", () => {
            layer.setStyle(countryStyleHover);
          });

          layer.on("mouseout", () => {
            if (countryIso2 === this.props.selection.iso2) {
              layer.setStyle(countryStyleSelected);
            } else {
              layer.setStyle(countryStyleFilled);
            }
          });

          layer.on("click", () => {
            this.map.closePopup(this.popup);

            dispatcher.fire("updateSelection", {
              iso2: countryIso2
            });
          });
        }
      };

      L.geoJson(
        countriesGeo, {
          onEachFeature: onEachFeature,
          style: countryStyleEmpty
        }
      ).addTo(this.map);
    });
  },

  updateSelectedCountry: function (oldSelection, newSelection) {
    this.mapReady.then(() => {
      var oldSelectedLayer = this.countryLayers[oldSelection.iso2];
      if (oldSelectedLayer != null) {
        oldSelectedLayer.setStyle(countryStyleFilled);
      }

      var newSelectedLayer = this.countryLayers[newSelection.iso2];
      if (newSelectedLayer != null) {
        newSelectedLayer.setStyle(countryStyleSelected);
        var newLatLngs = newSelectedLayer.getLatLngs();

        if (newLatLngs[0].constructor === Array) {
          var getArea = L.GeometryUtil.geodesicArea;
          newLatLngs = newLatLngs.sort((a, b) => getArea(a) - getArea(b)).reverse()[0];
        }

        this.map.fitBounds(newLatLngs);
      } else {
        this.map.fitWorld();
      }
    });
  },

  componentWillReceiveProps: function (newProps) {
    this.updateSelectedCountry(this.props.selection, newProps.selection);
  },

  render: function () {
    return (
      <div>
        <link rel="stylesheet" href={this.props.leafletCSSUrl} />
        <div id="leaders-map"></div>
      </div>
    );
  }
});

module.exports = {
  LeaderMap: LeaderMap
};
