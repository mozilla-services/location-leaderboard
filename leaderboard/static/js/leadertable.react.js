var dispatcher = require("./dispatcher.js");
var cachedFetch = require("./cachedfetch.js");
var getUrlParameters = require("./parseurl.js").getUrlParameters;
var getLeadersKey = require("./leaderskey.js");

var LeadersButton = React.createClass({
  handleClick: function () {
    if(this.props.offset != null) {
      dispatcher.fire("updateSelection", {
        iso2: this.props.selection.iso2,
        offset: this.props.offset,
        highlight: this.props.selection.highlight
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

  componentDidMount: function () {
    cachedFetch.get("countriesInfo").then((countriesInfo) => {
      this.setState({countries: countriesInfo});
    });
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
            <option value="">All Countries</option>
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

var LeadersTableRow = React.createClass({
  handleClick: function (e) {
    e.preventDefault();
    dispatcher.fire("updateSelection", {
      iso2: this.props.selection.iso2,
      offset: this.props.selection.offset,
      profile: this.props.leader.uid
    });
  },

  render: function () {
    var highlighted = (this.props.selection.highlight === this.props.leader.uid) ? "highlight" : "";
    return (
      <tr className={highlighted}>
        <td>{this.props.leader.rank}</td>
        <td><a href="" onClick={this.handleClick}>{this.props.leader.name}</a></td>
        <td>{this.props.leader.observations}</td>
      </tr>
    )
  }
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
          {this.props.leaders.map((leader) => {
            return (
              <LeadersTableRow
                selection={this.props.selection}
                leader={leader}
              />
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
    var leadersKey = getLeadersKey(selection);

    if (cachedFetch.keys[leadersKey] != null ) {
      cachedFetch.get(leadersKey).then((data) => {
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
      });
    }
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
          <LeadersTable
            selection={this.props.selection}
            leaders={this.state.leaders}
          />
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
