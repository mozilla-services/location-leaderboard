var urlPromises = {};

module.exports = {
  set: function (key, url, preprocessor) {
    urlPromises[key] = window.fetch(url).then(function (response) {
      return response.json();
    });

    if (preprocessor !== undefined) {
      urlPromises[key] = urlPromises[key].then(function (data) {
        return preprocessor(data);
      });
    };
  },

  get: function (key) {
    if (urlPromises[key] === undefined) {
      throw "Unknown key: " + key;
    }

    return urlPromises[key];
  }
};
