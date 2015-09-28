var dispatcher = require('./dispatcher.js');

var LeadersButton = React.createClass({
  handleClick: function () {
    if(this.props.url !== null) {
      dispatcher.fire('updateSelection', {
        name: this.props.selection.name,
        iso2: this.props.selection.iso2,
        url: this.props.url
      });
    }
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
  handleChange: function (e) {
    var countryIso2 = e.target.value;
    var countryInfo = this.props.config.countries[countryIso2];
    var selectionInfo;
    if (countryInfo !== undefined) {
      var selectionInfo = {
        url: countryInfo.leaders_url,
        name: countryInfo.name,
        iso2: countryInfo.iso2
      };
    }

    dispatcher.fire('updateSelection', selectionInfo);
  },

  render: function() {
    var countries = this.props.config.countries;
    var selection = this.props.selection;

    return (
      <div className="section">
        <div className="col span_12_of_12">
          <select value={selection.iso2} onChange={this.handleChange}>
            <option>All Countries</option>
            {Object.keys(countries).map(function(countryIso2) {
              return (
                <option value={countryIso2}>{countries[countryIso2].name}</option>
              )
            })}
          </select>
        </div>
      </div>
    );
  },
});

var LeadersFooter = React.createClass({
  render: function() {
    return (
      <div className="section">
        <div className="col span_3_of_12">
          <LeadersButton name="Previous" selection={this.props.selection} url={this.props.prevUrl} />
        </div>
        <div className="center col span_6_of_12">
          <span>{this.props.start} - {this.props.stop} of {this.props.total}</span>
        </div>
        <div className="col span_3_of_12">
          <LeadersButton name="Next" selection={this.props.selection} url={this.props.nextUrl} />
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
    return {
      total: 0,
      leaders: [],
      prevUrl: null,
      nextUrl: null
    };
  },

  loadData: function (url) {
    window.fetch(url).then(function(response) {
      return response.json()
    }).then(function(data) {
      this.setState({
        total: data.count,
        leaders: data.results,
        nextUrl: data.next,
        prevUrl: data.previous
      });
    }.bind(this));
  },

  componentWillReceiveProps: function (nextProps) {
    if(this.props.selection.url != nextProps.selection.url) {
      this.loadData(nextProps.selection.url);
    }
  },

  componentDidMount: function () {
    this.loadData(this.props.selection.url);
  },

  render: function() {
    var start = 0,
        stop = 0;

    if (this.state.leaders.length > 0) {
      start = this.state.leaders[0].rank;
      stop = this.state.leaders[this.state.leaders.length - 1].rank;
    }

    return (
      <div id="leaders-table">
        <LeadersHeader
          config={this.props.config}
          selection={this.props.selection}
        />
        <div id="leaders-table-content">
          <LeadersTable leaders={this.state.leaders} />
        </div>
        <LeadersFooter
          selection={this.props.selection}
          total={this.state.total}
          start={start}
          stop={stop}
          prevUrl={this.state.prevUrl}
          nextUrl={this.state.nextUrl}
        />
      </div>
    );
  }
});
