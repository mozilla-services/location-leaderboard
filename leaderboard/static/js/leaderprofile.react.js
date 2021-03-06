/*global React*/

var cachedFetch = require("./cachedfetch.js");
var dispatcher = require("./dispatcher.js");

var LeaderCountryRow = React.createClass({
  handleClick: function (e) {
    e.preventDefault();
    dispatcher.fire("updateSelection", {
      iso2: this.props.rank.country ? this.props.rank.country.iso2 : "",
      offset: Math.floor((this.props.rank.rank - 1) / 10) * 10,
      highlight: this.props.selection.profile
    });
  },

  render: function () {
    var countryName = this.props.rank.country != null ? this.props.rank.country.name : "All Countries";

    return (
      <tr>
        <td>{this.props.rank.rank}</td>
        <td><a href="" onClick={this.handleClick}>{countryName}</a></td>
        <td>{this.props.rank.observations}</td>
      </tr>
    );
  }
});

var LeaderProfile = React.createClass({
  getInitialState: function () {
    return {
      profile: {
        ranks: []
      }
    };
  },

  componentDidMount: function () {
    var profileKey = "profile:" + this.props.selection.profile;
    cachedFetch.get(profileKey).then((profile) => {
      this.setState({profile: profile});
    });
  },

  render: function () {
    return (
      <div id="leaders-profile-content">
        <h2>{this.state.profile.name}</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Region</th>
              <th>Contributions</th>
            </tr>
          </thead>
          <tbody>
            {this.state.profile.ranks.map((rank) =>
              <LeaderCountryRow
                key={this.props.selection.profile + (rank.country && rank.country.iso2)}
                selection={this.props.selection}
                rank={rank}
              />
            )}
          </tbody>
        </table>
      </div>
    );
  }
});

module.exports = {
  LeaderProfile: LeaderProfile
};
