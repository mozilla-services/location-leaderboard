function parseUrl(url) {
  var parser = document.createElement("a");
  parser.href = url;
  return parser;
}

function getUrlParameters(url) {
  var params = parseUrl(url).search.replace("?", "").split("&");
  var parsedParams = {};
  for(var param_i in params) {
    var splitParam = params[param_i].split("=");
    parsedParams[splitParam[0]] = splitParam[1];
  }
  return parsedParams;
}

module.exports = {
  parseUrl: parseUrl,
  getUrlParameters: getUrlParameters
}
