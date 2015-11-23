"use strict";

global.React = require("react");

var expect = require("chai").expect;
var LeaderProfileRow = require("../leaderprofile.react.js").LeaderProfileRow;
var skinDeep = require("skin-deep");

describe("LeaderProfileRow Tests", function () {
  var vdom, instance;

  beforeEach(function() {
    var tree = skinDeep.shallowRender(
      <LeaderProfileRow
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
