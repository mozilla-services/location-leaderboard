global.React = require("react");

var expect = require("chai").expect;
var LeaderCountryRow = require("../leaderprofile.react.js").LeaderCountryRow;
var skinDeep = require("skin-deep");

describe('LeaderCountryRow Tests', function () {
  var vdom, instance;

  beforeEach(function() {
    var tree = skinDeep.shallowRender(React.createElement(LeaderCountryRow, {selection: {}, rank: {}}));

    instance = tree.getMountedInstance();
    vdom = tree.getRenderOutput();
  });

  it('should do the stuff', function () {
  });
});
