var dispatcher = require('./dispatcher.js');

var LeadersButton = React.createClass({
  handleClick: function () {
    dispatcher.fire('updateUrl', {url: this.props.url});
  },

  render: function() {
    var classes = 'button ';
    classes += this.props.url === null ? 'insensitive' : '';
    return (
        <button onClick={this.handleClick} className={classes}>{this.props.name}</button>
    );
  },
});

var LeadersHeader = React.createClass({
  render: function() {
    return (
      <div className="section">
        <div className="col span_3_of_12">
          <LeadersButton name="Previous" url={this.props.prevUrl} />
        </div>
        <div id="leaders-region" className="center col span_6_of_12">
          <h3>{this.props.name}</h3>
        </div>
        <div className="col span_3_of_12">
          <LeadersButton name="Next" url={this.props.nextUrl} />
        </div>
      </div>
    );
  },
});

var LeadersTable = React.createClass({
  render: function() {
    return (
      <table className="table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>Contributions</th>
          </tr>
        </thead>
        <tbody>
          {this.props.leaders.map(function (leader) {
            return (
              <tr>
                <td>{leader.rank}</td>
                <td>{leader.name}</td>
                <td>{leader.observations}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    );
  },
});

module.exports = React.createClass({
  getInitialState: function () {
    return {leaders: [], prevUrl: null, nextUrl: null};
  },

  loadData: function (url) {
    $.getJSON(url, function (data) {
      this.setState({
        leaders: data.results,
        nextUrl: data.next,
        prevUrl: data.previous
      });
    }.bind(this));
  },

  componentWillReceiveProps: function (nextProps) {
    this.loadData(nextProps.url);
  },

  componentDidMount: function () {
    this.loadData(this.props.url);
  },

  render: function() {
    return (
      <div id="leaders-table">
        <LeadersHeader
          name={this.props.name}
          prevUrl={this.state.prevUrl}
          nextUrl={this.state.nextUrl}
        />
        <LeadersTable leaders={this.state.leaders} />
      </div>
    );
  }
});
