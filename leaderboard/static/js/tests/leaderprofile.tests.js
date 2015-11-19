global.React = require("react");

var expect = require("chai").expect;
var LeaderCountryRow = require("../leaderprofile.react.js").LeaderCountryRow;
var skinDeep = require("skin-deep");

describe("LeaderCountryRow Tests", function () {
  var vdom, instance;

  beforeEach(function() {
    var tree = skinDeep.shallowRender(
      <LeaderCountryRow
        selection={{iso2: 'CA'}}
        rank={{
          country: null,
          rank: 1,
          observations: 1
        }}
      />
    );

    instance = tree.getMountedInstance();
    vdom = tree.getRenderOutput();
  });

  it("should do the stuff", function () {
  });
});
