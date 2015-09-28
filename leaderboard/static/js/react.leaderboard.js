var dispatcher = require('./dispatcher.js');

var LeaderMap = require('./react.map.js');
var LeaderTable = require('./react.leaders.js');

module.exports = React.createClass({
  defaultSelection : function () {
    return {
      url: this.props.config.globalLeadersUrl,
      iso2: '',
      name: 'Global'
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
      map = <LeaderMap config={this.props.config} selection={this.state.selection} />;
    }

    return (
      <div id="leaderboard" className="section">
        <div className="col span_8_of_12">
          {map}
        </div>
        <div className="col span_4_of_12">
          <LeaderTable config={this.props.config} selection={this.state.selection} />
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
  }
});
