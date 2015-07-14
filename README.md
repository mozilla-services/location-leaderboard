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
 Submit the number of networks detected within a series of tiles.

* **URL**

  https://leaderboard.services.mozilla.com/backend/add_stumbles

* **Method:**

  `POST`

*  **URL Params**

  None

* **Data Params**

  POST body (JSON encoded)

        {
          items: [
            {
              tile_east: <int>,
              tile_north: <int>,
              observations: <int>
            }
          ]
        }

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
                tile_east: -8872100,
                tile_north: 5435700,
                observations: 100
              },
              {
                tile_east: -8872100,
                tile_north: 5435700,
                observations: 100
              },
              {
                tile_east: -8892100,
                tile_north: 5435700,
                observations: 100
              }
            ]
          },
          type : "POST",
          success : function(r) {
            console.log(r);
          }
        });
