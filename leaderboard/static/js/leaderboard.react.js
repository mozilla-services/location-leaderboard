var dispatcher = require("./dispatcher.js");
var cachedFetch = require("./cachedfetch.js");
var getLeadersKey = require("./leaderskey.js");

var LeaderMap = require("./leadermap.react.js");
var LeaderTable = require("./leadertable.react.js");

var Leaderboard = React.createClass({
  defaultSelection : function () {
    return {
      iso2: null,
      offset: null,
    }
  },

  getInitialState: function () {
    return {
      selection: this.defaultSelection()
    };
  },

  isMobile: function () {
    return window.matchMedia("only screen and (max-width: 480px)").matches;
  },

  render: function() {
    var map;

    if (!this.isMobile()) {
      map = <LeaderMap
        leafletJSUrl={this.props.config.leafletJSUrl}
        leafletCSSUrl={this.props.config.leafletCSSUrl}
        selection={this.state.selection}
      />;
    }

    return (
      <div id="leaderboard" className="section">
        <div className="col span_8_of_12">
          {map}
        </div>
        <div className="col span_4_of_12">
          <LeaderTable
            selection={this.state.selection}
          />
        </div>
      </div>
    );
  },

  handleResize: function () {
    this.forceUpdate();
  },

  loadLeadersData: function (selection) {
    return cachedFetch.get("countriesInfo").then(function (countriesInfo) {
      var leadersUrl = this.props.config.globalLeadersUrl;

      var countryInfo = countriesInfo[selection.iso2];
      if (countryInfo !== undefined) {
        leadersUrl = countryInfo.leaders_url;
      }

      if (selection.offset != null) {
        leadersUrl += "?offset=" + selection.offset;
      }

      cachedFetch.set(
        getLeadersKey(selection.iso2, selection.offset),
        leadersUrl
      );
    }.bind(this));
  },

  handleUpdateSelection: function (selection) {
    this.loadLeadersData(selection).then(function() {
      this.setState({selection: selection});
    }.bind(this));
  },

  componentWillMount: function () {
    window.addEventListener("resize", this.handleResize);
    dispatcher.on("updateSelection", this.handleUpdateSelection);
  }
});

module.exports = {
  init: function (config) {
    cachedFetch.set(getLeadersKey(null, null), config.globalLeadersUrl);

    cachedFetch.set("countriesGeo", config.countriesGeoUrl);

    cachedFetch.set("countriesInfo", config.countriesInfoUrl, function (countriesInfo) {
      var countries = {};
      for(var country_i in countriesInfo) {
        var country = countriesInfo[country_i];
        countries[country.iso2] = country;
      }
      return countries;
    });

    ReactDOM.render(
      <Leaderboard config={config} />,
      document.getElementById("leaderboard-container")
    );
  }
}
