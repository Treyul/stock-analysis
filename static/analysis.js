// get elements
const current_year_revenue = document.getElementById("current_year_revenue");
const current_year_volume = document.getElementById("current_year_volume");

const MONTHS = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "June",
  "Jul",
  "Aug",
  "Sept",
  "Oct",
  "Nov",
  "Dec",
];
const date = new Date();
// fetch data to be rendered using graphs
fetch("/analysis", {
  method: "POST",
  headers: { "content-type": "application/json" },
  //   body: JSON.stringify(search_object),
}).then(function (response) {
  if (response.status != 200) {
    console.log("ERROR");
  }
  response.json().then(function (data) {
    // get if it was a success
    if (data["message"] == "success") {
      delete data["message"];

      //   get current year revenue
      const revenue = data["revenue"];

      let revenue_data = [];

      // create plotting data
      for (var i = 0; i < revenue.length; i++) {
        var graph = [];
        // push name of the column
        graph.push(MONTHS[i]);
        // push value of the column
        graph.push(revenue[i]);

        // append data to main array for graph rendering
        revenue_data.push(graph);
      }

      // create a chart
      chart = anychart.column();

      // create a column series and set the data
      var series = chart.column(revenue_data);

      // set the container id
      chart.container("current_year_revenue");

      // initiate drawing the chart
      chart.draw();
      // get current year volume of saes
      const volume = data["volume"];

      let revenue_volume = [];

      // create mapping data
      for (var i = 0; i < volume.length; i++) {
        var graph = [];
        // push name of the column
        graph.push(MONTHS[i]);
        // push value of the column
        graph.push(volume[i]);

        // append data to main array for graph rendering
        revenue_volume.push(graph);
      }

      // create a chart
      volume_chart = anychart.column();

      // create a column series and set the data
      var series = volume_chart.column(revenue_volume);

      // set the container id
      volume_chart.container("current_year_volume");

      // initiate drawing the chart
      volume_chart.draw();
    }
  });
});

// console.log(response);
