module.exports = function (selection) {
  return "countryLeaders:" + selection.iso2 + ":" + selection.offset;
}
