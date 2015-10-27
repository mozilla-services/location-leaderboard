var dispatcher = require('./dispatcher.js');
var cachedFetch = require('./cachedfetch.js');

var LeaderMap = require('./leadermap.react.js');
var LeaderTable = require('./leadertable.react.js');

var Leaderboard = React.createClass({
  defaultSelection : function () {
    return {
      url: this.props.config.globalLeadersUrl,
      iso2: '',
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
            config={this.props.config}
            selection={this.state.selection}
          />
        </div>
      </div>
    );
  },

  handleResize: function () {
    this.forceUpdate();
  },

  handleUpdateSelection: function (selection) {
    if (selection) {
      cachedFetch.set('countryLeaders:' + selection.iso2, selection.url);
      this.setState({selection: selection});
    } else {
      this.setState({selection: this.defaultSelection()});
    }
  },

  componentWillMount: function () {
    window.addEventListener('resize', this.handleResize);

    dispatcher.on('updateSelection', this.handleUpdateSelection);
  }
});

module.exports = {
  init: function (config) {
    cachedFetch.set('countryLeaders:', config.globalLeadersUrl);

    cachedFetch.set('countriesGeo', config.countriesGeoUrl);

    cachedFetch.set('countriesInfo', config.countriesInfoUrl, function (countriesInfo) {
      var countries = {};
      for(var country_i in countriesInfo) {
        var country = countriesInfo[country_i];
        countries[country.iso2] = country;
      }
      return countries;
    });

    ReactDOM.render(
      <Leaderboard config={config} />,
      document.getElementById('leaderboard-container')
    );
  }
}
