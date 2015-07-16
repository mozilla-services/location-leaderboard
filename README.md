# leaderboard-server

The leaderboard-server is a RESTful service which implements an API
for submitting data which describes the geolocation stumbling efforts
of contributors to the Mozilla Location Service project.  Mozilla Stumbler
users can submit data to the leaderboard-server about how many networks
were detected within a geospatial 'tile' at a given time, and then query
the top contributors.

# API Interface

Add Stumbles
----
 Submit the number of networks detected within a series of tiles for a given contributor.

* **URL**

  https://leaderboard.services.mozilla.com/backend/add_stumbles

* **Method:**

  `POST`

*  **URL Params**

  None

* **Data Params**

  The data submitted in a single POST request describes how many observations 
  were made by a contributor.  Each observation is made at a given time and place,
  however to reduce the size of the data sent, the observations are grouped into 'tiles'.
  The tile size is requested from the server, and is measured in meters.  Observations are
  then grouped into tiles of that size and summed.  Each data point sent 
  describes the coordinates of a point within that tile (the server will round the coordinates
  provided to the nearest containing tile), and the number of observations made within that
  tile.

  * **POST body (JSON encoded)**

        {
          items: [
            {
              tile_easting_m: <int>,
              tile_northing_m: <int>,
              observations: <int>
            }
          ]
        }

  * **tile_easting_m**

  The number of meters east from 0,0 in the [EPSG 3857 coordinate system](http://spatialreference.org/ref/sr-org/7483/)

  * **tile_northing_m**

  The number of meters north from 0,0 in the [EPSG 3857 coordinate system](http://spatialreference.org/ref/sr-org/7483/)

  * **observations**

  The number of observations made by the contributor since the last time they submitted
  to the leaderboard within the specified 1km x 1km tile.

* **Request Headers**

  * Content-Encoding 

  The submission API optionally supports gzipped payloads.  To submit a gzipped
  request, include the gzipped JSON data in the request body and add the
  header to the request.

  Example: `Content-Encoding: gzip`
  
  * Authorization 

  A successful submission must include a valid Firefox Accounts authorization
  bearer token
  
  Example: `Authorization: Bearer kf94k5jsgsl3kj`

* **Success Response:**

  * **Code:** 201

* **Error Responses:**

  * **Code:** 400 INVALID  <br />
    **Content:** `{"detail":"JSON parse error - Expecting object: line 1 column 1 (char 0)"}`

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{"detail":"Unable to determine a valid Firefox Accounts authorization token"}`

* **Sample Call:**

        $.ajax({
          url: "https://leaderboard.services.mozilla.com/backend/add_stumbles",
          dataType: "json",
          beforeSend: function(xhr) {
            xhr.setRequestHeader('Authorization', 'Bearer fksdf90sek4jk50');
          },
          data : {
            items: [
              {
                tile_easting_m: -8872100,
                tile_northing_m: 5435700,
                observations: 100
              },
              {
                tile_easting_m: -8872100,
                tile_northing_m: 5435700,
                observations: 100
              },
              {
                tile_easting_m: -8892100,
                tile_northing_m: 5435700,
                observations: 100
              }
            ]
          },
          type : "POST",
          success : function(r) {
            console.log(r);
          }
        });
