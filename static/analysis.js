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

const QUARTERS = ["Fisrt", "Second", "Third", "Fourth"];
const date = new Date();

const menu_hamburger = document.getElementById("hamburger");
const drop_down_submenus = document.querySelectorAll(".nav-dropdown");

menu_hamburger.addEventListener("click", function () {
  //   select the hamburger items
  const item_one = menu_hamburger.querySelector("#one");
  const item_two = menu_hamburger.querySelector("#two");
  const item_three = menu_hamburger.querySelector("#three");

  //   select the main menu
  const menu = document.getElementById("main-menu");

  //   toggle the class for view and close menu
  menu.classList.toggle("show");
  item_one.classList.toggle("item-one");
  item_two.classList.toggle("item-two");
  item_three.classList.toggle("item-three");
  menu.classList.toggle("menuhidden");
});
// fetch data to be rendered using graphs
// fetch("/analysis", {
//   method: "POST",
//   headers: { "content-type": "application/json" },
//   //   body: JSON.stringify(search_object),
// }).then(function (response) {
//   if (response.status != 200) {
//     console.log("ERROR");
//   }
//   response.json().then(function (data) {
//     // get if it was a success
//     if (data["message"] == "success") {
//       delete data["message"];

//       //   get current year revenue
//       const revenue = data["revenue"];

//       let revenue_data = [];

//       // create plotting data
//       for (var i = 0; i < revenue.length; i++) {
//         var graph = [];
//         // push name of the column
//         graph.push(MONTHS[i]);
//         // push value of the column
//         graph.push(revenue[i]);

//         // append data to main array for graph rendering
//         revenue_data.push(graph);
//       }

//       // create a chart
//       chart = anychart.column();

//       // create a column series and set the data
//       var series = chart.column(revenue_data);

//       // set the container id
//       chart.container("current_year_revenue");

//       // initiate drawing the chart
//       chart.draw();
//       // get current year volume of sales
//       const volume = data["volume"];

//       let revenue_volume = [];

//       // create mapping data
//       for (var i = 0; i < volume.length; i++) {
//         var graph = [];
//         // push name of the column
//         graph.push(MONTHS[i]);
//         // push value of the column
//         graph.push(volume[i]);

//         // append data to main array for graph rendering
//         revenue_volume.push(graph);
//       }

//       // create a chart
//       volume_chart = anychart.column();

//       // create a column series and set the data
//       var series = volume_chart.column(revenue_volume);

//       // set the container id
//       volume_chart.container("current_year_volume");

//       // initiate drawing the chart
//       volume_chart.draw();

//       /************** CREATE QUARTERLY GRAPHS *************/

//       let quarter_volume_graph = [];
//       let quarter_revenue_graph = [];
//       for (let k = 0; k < Math.ceil(revenue.length / 3); k++) {
//         // get starter value for each month in the quarters
//         var quarter_volume = 0;
//         var quarter_revenue = 0;
//         var vol_graph = [];
//         var rev_graph = [];

//         vol_graph.push(QUARTERS[k]);
//         rev_graph.push(QUARTERS[k]);
//         // iterate between the data arrays sent through backend
//         for (let r = k * 3 + 1; r < k * 3 + 4; r++) {
//           quarter_revenue += revenue[r];
//           quarter_volume += volume[r];
//         }
//         // push quarter's data into column
//         vol_graph.push(quarter_volume);
//         rev_graph.push(quarter_revenue);

//         // push columns into graph
//         quarter_revenue_graph.push(rev_graph);
//         quarter_volume_graph.push(vol_graph);
//       }
//     }
//   });
// });

// console.log(response);
