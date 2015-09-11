var getUrlParameter = require('./url_param.js');
var isVisible = require('./is_visible.js');

var regionSource   = $("#region-template").html();
var regionTemplate = Handlebars.compile(regionSource);

var leaderSource   = $("#leader-template").html();
var leaderTemplate = Handlebars.compile(leaderSource);

var leadersCountSource   = $("#leaders-count-template").html();
var leadersCountTemplate = Handlebars.compile(leadersCountSource);

var globalName = 'Global';
var globalUrl;

var nextUrl;
var prevUrl;

function pushHistory(dataUrl, countryName) {
  var urlParser = document.createElement('a');
  urlParser.href = dataUrl;
  var stateUrl = btoa(encodeURIComponent(urlParser.pathname + urlParser.search));

  var urlParams = '?data=' + stateUrl;
  if (typeof countryName !== 'undefined') {
    urlParams += '&country=' + countryName;
  }

  history.pushState(
    {url: dataUrl, countryName: countryName},
    '',
    urlParams
  );
}

function loadUrl(dataUrl, countryName) {
  if (!isVisible('#leaders')) {
    $('html,body').animate({scrollTop: $('#leaders').offset().top},'slow');
  }

  var regionName = globalName;
  if (typeof countryName !== 'undefined') {
    regionName = countryName;
  }

  $.getJSON(dataUrl, function (data) {
    var regionHtml = regionTemplate({count: data.count, region: regionName, global: regionName == globalName});
    $('#leaders-region').html(regionHtml);

    $('#leaders tbody').html('');

    nextUrl = data.next;
    if (nextUrl) {
      $('#next-button').removeClass('insensitive');
    } else {
      $('#next-button').addClass('insensitive');
    }

    prevUrl = data.previous;
    if (prevUrl) {
      $('#previous-button').removeClass('insensitive');
    } else {
      $('#previous-button').addClass('insensitive');
    }

    for(var i in data.results) {
      var result = data.results[i];

      if (typeof Intl !== 'undefined') {
        result.observations = new Intl.NumberFormat().format(result.observations);
      }

      var html = leaderTemplate(result);

      $('#leaders tbody').append(html);
    }

    if (data.results.length) {
      $('#leaders-count').html(leadersCountTemplate({
          start: data.results[0].rank,
          stop: data.results[data.results.length-1].rank,
          total: data.count
      }));
      $('#no-results').hide();
      $('#leaders table').show();
    } else {
      $('#no-results').show();
      $('#leaders table').hide();
    }

    $('.region-global-button').on('click', function (e) {
        e.preventDefault();
        requestUrl(globalUrl);
    });


  });
}

function requestUrl(url, countryName) {
  if (url) {
    loadUrl(url, countryName);
    pushHistory(url, countryName);
  }
}

function setupLeaders(config) {
  globalUrl = config.globalUrl;

  var startUrl = globalUrl;

  var paramUrl = getUrlParameter('data');
  if (typeof paramUrl !== 'undefined') {
      startUrl = decodeURIComponent(atob(paramUrl));
  }

  var countryName = getUrlParameter('country');

  $('#next-button').on('click', function (e) {
    requestUrl(nextUrl);
  });

  $('#previous-button').on('click', function (e) {
    requestUrl(prevUrl);
  });

  window.onpopstate = function (e) {
    loadUrl(e.state.url);
  }

  requestUrl(startUrl, countryName);
}

module.exports = {
  init: function (config) {
    setupLeaders(config);
  },

  requestUrl: requestUrl,
}
