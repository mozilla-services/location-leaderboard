var map = require('./map.js');
var leaders = require('./leaders.js');

module.exports = function (config) {
    map.init(config);
    leaders.init(config);
}
