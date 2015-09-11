var dispatcher = require('./dispatcher.js');

var LeaderMap = require('./react.map.js');
var LeaderTable = require('./react.leaders.js');

module.exports = React.createClass({
  getInitialState: function () {
    return {
      url: this.props.globalUrl,
      name: 'Global'
    };
  },

  updateUrl: function (data) {
    this.setState({url: data.url, name: data.name || 'Global'});
  },

  render: function() {
    return (
      <div id="leaderboard" className="section">
        <div className="col span_8_of_12">
          <LeaderMap />
        </div>
        <div className="col span_4_of_12">
          <LeaderTable name={this.state.name} url={this.state.url} />
        </div>
      </div>
    );
  },

  componentWillMount: function () {
    dispatcher.on('updateUrl', function (data) {
      this.updateUrl(data);
    }.bind(this));
  }
});
