var dispatcher = require("./dispatcher.js");
var cachedFetch = require("./cachedfetch.js");
var getUrlParameters = require("./parseurl.js").getUrlParameters;
var getLeadersKey = require("./leaderskey.js");

var LeadersButton = React.createClass({
  handleClick: function () {
    if(this.props.offset != null) {
      dispatcher.fire("updateSelection", {
        iso2: this.props.selection.iso2,
        offset: this.props.offset
      });
    }
  },

  render: function() {
    var classes = "button ";
    classes += (this.props.offset == null) ? "insensitive" : "";
    return (
        <button onClick={this.handleClick} className={classes}>{this.props.name}</button>
    );
  },
});

var LeadersHeader = React.createClass({
  getInitialState: function () {
    return {
      countries: [],
    }
  },

  componentWillMount: function () {
    cachedFetch.get("countriesInfo").then(function (countriesInfo) {
      this.setState({countries: countriesInfo});
    }.bind(this));
  },

  handleChange: function (e) {
    dispatcher.fire("updateSelection", {iso2: e.target.value});
  },

  render: function() {
    var countries = this.state.countries;
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
          <LeadersButton
            name="Previous"
            selection={this.props.selection}
            offset={this.props.prevOffset}
          />
        </div>
        <div className="center col span_6_of_12">
          <span>{this.props.start} - {this.props.stop} of {this.props.total}</span>
        </div>
        <div className="col span_3_of_12">
          <LeadersButton
            name="Next"
            selection={this.props.selection}
            offset={this.props.nextOffset}
          />
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
      nextOffset: null,
      prevOffset: null
    };
  },

  loadData: function (selection) {
    var leadersKey = getLeadersKey(selection.iso2, selection.offset);

    cachedFetch.get(leadersKey).then(function(data) {
      var nextOffset = getUrlParameters(data.next).offset;

      var prevOffset;
      if (data.previous != null) {
        prevOffset = getUrlParameters(data.previous).offset || "0";
      }

      this.setState({
        total: data.count,
        leaders: data.results,
        nextOffset: nextOffset,
        prevOffset: prevOffset
      });
    }.bind(this));
  },

  componentWillReceiveProps: function (nextProps) {
    this.loadData(nextProps.selection);
  },

  componentDidMount: function () {
    this.loadData(this.props.selection);
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
          nextOffset={this.state.nextOffset}
          prevOffset={this.state.prevOffset}
        />
      </div>
    );
  }
});
