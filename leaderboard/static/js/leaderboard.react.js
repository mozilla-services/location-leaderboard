var dispatcher = require("./dispatcher.js");
var cachedFetch = require("./cachedfetch.js");
var getUrlParameters = require('./parseurl.js').getUrlParameters;
var getLeadersKey = require("./leaderskey.js");

var LeaderMap = require("./leadermap.react.js");
var LeaderTable = require("./leadertable.react.js");

var Leaderboard = React.createClass({
  getLeadersUrl: function (selection) {
    return cachedFetch.get("countriesInfo").then(function (countriesInfo) {
      var leadersUrl = this.props.config.globalLeadersUrl;

      var countryInfo = countriesInfo[selection.iso2];
      if (countryInfo !== undefined) {
        leadersUrl = countryInfo.leaders_url;
      }

      if (selection.offset != null) {
        leadersUrl += "?offset=" + selection.offset;
      }

      return leadersUrl;
    }.bind(this));
  },

  loadLeadersData: function (selection) {
    return this.getLeadersUrl(selection).then(function (leadersUrl) {
      return cachedFetch.set(getLeadersKey(selection), leadersUrl);
    });
  },

  getInitialState: function () {
    return {
      selection: {
        iso2: null,
        offset: null
      }
    };
  },

  isMobile: function () {
    return window.matchMedia("only screen and (max-width: 480px)").matches;
  },

  render: function() {
    var map;

    if (!this.isMobile()) {
      map = <LeaderMap
        countriesGeoUrl={this.props.config.countriesGeoUrl}
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

  updateUrl: function (selection) {
    var newUrlParams = [];

    if (selection.iso2 != null && selection.iso2.length > 0) {
      newUrlParams.push("region=" + selection.iso2);
    }

    if (selection.offset != null) {
      newUrlParams.push("offset=" + selection.offset);
    }

    var newUrl = "?";
    if (newUrlParams.length > 0) {
      newUrl += newUrlParams.join("&");
    }

    window.history.pushState({}, "", newUrl);
  },

  handleUpdateSelection: function (selection) {
    this.updateUrl(selection);
    this.loadLeadersData(selection).then(function() {
      this.setState({selection: selection});
    }.bind(this));
  },

  componentWillMount: function () {
    window.addEventListener("resize", this.handleResize);
    dispatcher.on("updateSelection", this.handleUpdateSelection);
  },

  componentDidMount: function () {
    var locationParams = getUrlParameters(window.location.search);
    var selection = {
      iso2: locationParams.region || null,
      offset: locationParams.offset || null
    };
    this.handleUpdateSelection(selection);
  }
});

module.exports = {
  init: function (config) {
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
