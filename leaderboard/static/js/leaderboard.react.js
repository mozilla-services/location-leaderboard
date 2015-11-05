var dispatcher = require("./dispatcher.js");
var cachedFetch = require("./cachedfetch.js");
var getUrlParameters = require('./parseurl.js').getUrlParameters;
var getLeadersKey = require("./leaderskey.js");

var LeaderMap = require("./leadermap.react.js");
var LeaderTable = require("./leadertable.react.js");
var LeaderProfile = require("./leaderprofile.react.js");

var Leaderboard = React.createClass({
  getInitialState: function () {
    return {
      selection: {
        iso2: null,
        offset: null,
        profile: null,
        highlight: null
      }
    };
  },

  isMobile: function () {
    return window.matchMedia("only screen and (max-width: 480px)").matches;
  },

  render: function() {
    var map;
    var content;

    if (!this.isMobile()) {
      map = <LeaderMap
        countriesGeoUrl={this.props.config.countriesGeoUrl}
        leafletJSUrl={this.props.config.leafletJSUrl}
        leafletCSSUrl={this.props.config.leafletCSSUrl}
        selection={this.state.selection}
      />;
    }

    if (this.state.selection.profile != null) {
      content = <LeaderProfile
        selection={this.state.selection}
      />;
    } else {
      content = <LeaderTable
        selection={this.state.selection}
      />;
    }

    return (
      <div id="leaderboard" className="section">
        <div className="col span_8_of_12">
          {map}
        </div>
        <div className="col span_4_of_12">
          {content}
        </div>
      </div>
    );
  },

  updateWindowLocation: function (selection) {
    var newLocationParams = [];

    for (var paramName in selection) {
      var paramValue = selection[paramName];
      if ((paramValue != null) && ((("" + paramValue).length) > 0)) {
        newLocationParams.push(paramName + '=' + paramValue);
      }
    }

    var newLocation = "?";
    if (newLocationParams.length > 0) {
      newLocation += newLocationParams.join("&");
    }

    window.history.pushState({}, "", newLocation);
  },

  getLeadersUrl: function (selection) {
    var leadersUrl = this.props.config.globalLeadersUrl;

    if (selection.iso2 != null && selection.iso2.length > 0) {
      leadersUrl = this.props.config.countryLeadersUrl.replace("XX", selection.iso2);
    }

    if (selection.offset != null) {
      leadersUrl += "?offset=" + selection.offset;
    }

    return leadersUrl;
  },

  loadLeadersData: function (selection) {
    var leadersUrl = this.getLeadersUrl(selection);
    return cachedFetch.set(getLeadersKey(selection), leadersUrl);
  },

  loadProfileData: function (selection) {
    var profileUrl = this.props.config.leaderProfileUrl.replace("XX", selection.profile);
    var profileKey = "profile:" + selection.profile;
    return cachedFetch.set(profileKey, profileUrl);
  },

  handleUpdateSelection: function (selection) {
    this.updateWindowLocation(selection);

    if (selection.profile != null) {
      this.loadProfileData(selection).then(function() {
        this.setState({selection: selection});
      }.bind(this));
    } else {
      this.loadLeadersData(selection).then(function() {
        this.setState({selection: selection});
      }.bind(this));
    }
  },

  handleResize: function () {
    this.forceUpdate();
  },

  componentWillMount: function () {
    window.addEventListener("resize", this.handleResize);
    dispatcher.on("updateSelection", this.handleUpdateSelection);
  },

  componentDidMount: function () {
    this.handleUpdateSelection(getUrlParameters(window.location.search));
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
