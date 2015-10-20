var dispatcher = require('./dispatcher.js');

var LeaderMap = require('./leadermap.react.js');
var LeaderTable = require('./leadertable.react.js');

var Leaderboard = React.createClass({
  defaultSelection : function () {
    return {
      url: this.props.config.globalLeadersUrl,
      iso2: '',
      name: 'Global'
    }
  },

  getInitialState: function () {
    return {
      countries: [],
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
        key={this.state.countries}
        config={this.props.config}
        countries={this.state.countries}
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
            countries={this.state.countries}
            selection={this.state.selection}
          />
        </div>
      </div>
    );
  },

  handleResize: function () {
    this.forceUpdate();
  },

  componentWillMount: function () {
    window.addEventListener('resize', this.handleResize);

    dispatcher.on('updateSelection', function (selection) {
      if (selection === null) {
        this.setState({selection: this.defaultSelection()});
      } else {
        this.setState({selection: selection});
      }
    }.bind(this));
  },

  componentDidMount: function () {
    window.fetch(this.props.config.countriesInfoUrl).then(function (response) {
      return response.json();
    }).then(function (data) {
      var countries = {};
      for(var country_i in data) {
        var country = data[country_i];
        countries[country.iso2] = country;
      }
      this.setState({countries: countries});
    }.bind(this));
  }
});

module.exports = function (config) {
  ReactDOM.render(
    <Leaderboard config={config} />,
    document.getElementById('leaderboard-container')
  );
};
