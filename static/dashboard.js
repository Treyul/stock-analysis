const Show_Abstract = document.querySelectorAll(".showabstract");
const Show_Detailed = document.querySelectorAll(".showdetailed");
const worth_Containers = document.querySelectorAll("#worthsum");
const Show_Order_abtr = document.querySelectorAll(".show-order-abtr");
const Show_Order_deets = document.querySelectorAll(".show-order-var");
const Show_Worth_deets = document.querySelectorAll(".show-worth-deets");
const Sales_analysis_chart = document.getElementById("sales_analysis");
const Product_selection = document.getElementById("products");
// const default_product =  document.querySelector("#products option:checked").innerHTML
// const default_product_div = document.querySelector(`#analysis > div.${default_product}`)
const products_divs = document.querySelectorAll(`#analysis > div`);

// default_product_div.classList.toggle("hidden")
// default_product_div.classList.toggle("analysis--div")

// event listener to show more details in the sections
Show_Abstract.forEach((button) => {
  button.addEventListener("click", function () {
    toggle_abstract_class(button, "abstract");
  });
});

Show_Detailed.forEach((button) => {
  button.addEventListener("click", function () {
    toggle_detail_class(button, "detailed");
  });
});

worth_Containers.forEach((container) => {
  worth_summation(container);
});

Show_Order_abtr.forEach((button) => {
  button.addEventListener("click", function () {
    toggle_abstract_class(button, "order-abtr");
  });
});

Show_Order_deets.forEach((button) => {
  button.addEventListener("click", function () {
    toggle_detail_class(button, "order-var");
  });
});

Show_Worth_deets.forEach((button) => {
  button.addEventListener("click", function () {
    toggle_detail_class(button, "worth-deets");
  });
});

fetch("sale-analysis", {
  method: "GET",
  headers: { "content-type": "application/json" },
}).then(function (response) {
  if (response.status !== 200) return;
  response.json().then(function (data) {
    // console.log(data);

    // graph for last 5 day sales
    new Chart(Sales_analysis_chart, {
      type: "bar",
      data: {
        labels: data["wholesale"][0],
        datasets: [
          {
            // backgroundColor: "orange",
            //  ["rgba(255, 165, 0,1)", "#20b720"],
            // label: "wholesale",
            backgroundColor: "rgba(255, 165, 0,1.0)",
            data: data["wholesale"][1],
            // borderWidth: 2,
          },
          {
            label: "retail",
            backgroundColor: "rgba(255, 165, 0,0.5)",
            data: data["retail"][1],
            // borderWidth: 1,
          },
        ],
      },
      options: {
        title: {
          display: true,
          text: "Last 5 days sales were made",
        },
        legend: { display: false },
        scales: {
          yAxes: [
            {
              gridLines: { display: false },
              ticks: {
                // beginAtZero: true,
                max:
                  Math.max(...data["wholesale"][1]) +
                  Math.ceil(
                    Math.max(...data["wholesale"][1]) /
                      Math.min(...data["wholesale"][1]) /
                      1000
                  ) *
                    1000,
                beginAtZero: true,
                stepSize:
                  Math.ceil(
                    Math.max(...data["wholesale"][1]) /
                      Math.min(...data["wholesale"][1]) /
                      1000
                  ) * 1000,
              },
            },
          ],
        },
      },
    });

    // gauge graphs for product performance
    const graph_containers = document.querySelectorAll(
      "#analysis div > div#graph canvas"
    );

    // plugin to input text in the middle of doughnut
    Chart.pluginService.register({
      beforeDraw: function (chart) {
        if (chart.options.centertext) {
          var width = chart.chart.width,
            height = chart.chart.height,
            ctx = chart.chart.ctx;

          ctx.restore();
          var fontSize = (height / 150).toFixed(2); // was: 114
          ctx.font = fontSize + "em sans-serif";
          ctx.textBaseline = "middle";

          var text = chart.options.centertext, // "75%",
            textX = Math.round((width - ctx.measureText(text).width) / 2),
            textY = height / 2 - (chart.titleBlock.height - 15);

          ctx.fillText(text, textX, textY);
          ctx.save();
        }
      },
    });

    // display the gauges for each product
    for (var i = 0; i < graph_containers.length; i++) {
      const obj_desc = data["analysis"][i];
      new Chart(graph_containers[i], {
        type: "doughnut",
        data: {
          labels: ["sold", "remaining"],
          datasets: [
            {
              //
              data: [obj_desc.ordered - obj_desc.available, obj_desc.available],
              backgroundColor: ["lightgreen", "lightgrey"],
            },
          ],
        },
        options: {
          centerArea: {
            text: "Title",
            subText: "Subtitle",
          },
          // title:{
          //   position:"bottom",
          //   display:true,
          //   text:
          //   ,padding:0
          // },
          centertext: `${
            ((obj_desc.ordered - obj_desc.available) / obj_desc.ordered) * 100
          }% sold`,
          legend: {
            // display:false ,
            fullWidth: false,
            position: "bottom",
            labels: {
              boxWidth: 10,
              // This more specific font property overrides the global property
              fontSize: 10,
            },
          },
          // responsive: true,
          maintainAspectRatio: false,
          cutoutPercentage: "90",
          rotation: -1.25 * Math.PI,
          circumference: 1.5 * Math.PI,
        },
      });
    }

    // draw a line graph for the products
    const Product_line_graphs = document.querySelectorAll(
      "#analysis div > div#sale-line-graph canvas"
    );
    for (var i = 0; i < Product_line_graphs.length; i++) {
      const obj_desc = data["analysis"][i].sales_history;
      // console.log(obj_desc[0].length == 0);
      if (obj_desc[0].length > 2) {
        // console.log("2");
        new Chart(Product_line_graphs[i], {
          type: "line",
          data: {
            labels: obj_desc[0],
            datasets: [
              {
                label: "sales",
                data: obj_desc[1],
                backgroundColor: "rgb(100, 149, 237)",
                borderColor: "white",
              },
            ],
          },
          options: {
            title: {
              display: true,
              text: "Product performance",
            },
            legend: { display: false },
            scales: {
              yAxes: [
                {
                  gridLines: {
                    display: false,
                  },
                  ticks: {
                    max: Math.max(...obj_desc[1]) + 1,
                    stepSize: Math.ceil(Math.max(...obj_desc[1]) / 5),
                    beginAtZero: true,
                  },
                },
              ],
            },
          },
        });
      } else if (obj_desc[0].length > 0 && obj_desc[0].length <= 2) {
        new Chart(Product_line_graphs[i], {
          type: "bar",
          data: {
            labels: obj_desc[0],
            datasets: [
              {
                data: obj_desc[1],
                backgroundColor: "rgb(100, 149, 237)",
                borderColor: "white",
              },
            ],
          },
          options: {
            title: {
              display: true,
              position: "top",
              text: "Product performance",
            },
            legend: { display: false },
            scales: {
              yAxes: [
                {
                  gridLines: { display: false },
                  ticks: {
                    max: Math.max(...obj_desc[1]) + 2,
                    beginAtZero: true,
                    stepSize: Math.ceil(Math.max(...obj_desc[1]) / 5),
                  },
                },
              ],
              // xAxes: [{ gridLines: { display: false } }],
            },
          },
        });
      } else if (obj_desc[0].length == 0) {
        Product_line_graphs[i].closest("div").remove();
        // console.log(3);
      }
    }

    // donought pie to show sales sharing
    const Product_pie_graphs = document.querySelectorAll(
      "#analysis div > div#sale-pie-graph canvas"
    );
    for (var i = 0; i < Product_pie_graphs.length; i++) {
      const obj_desc = data["analysis"][i];
      const available = obj_desc.available;
      const ordered_amount = obj_desc.ordered;
      var wholesale_sales = obj_desc.sales_history[1].reduce(
        (a, b) => a + b,
        0
      );
      // console.log(obj_desc);

      if (ordered_amount - available <= 0) {
        Product_pie_graphs[i].closest("div").remove();
      } else {
        new Chart(Product_pie_graphs[i], {
          type: "doughnut",
          data: {
            labels: ["Wholesale", "retail"],
            datasets: [
              {
                data: [
                  wholesale_sales,
                  ordered_amount - available - wholesale_sales,
                ],
                backgroundColor: ["lightblue", "grey"],
              },
            ],
          },
          options: {
            centerArea: {
              text: "Title",
              subText: "Subtitle",
            },
            title: {
              position: "top",
              display: true,
              text: "Sales sharing between retail and wholesale",
              padding: 0,
            },
            // centertext: `${(obj_desc.ordered-obj_desc.available)/obj_desc.ordered*100}% sold`,
            legend: {
              // display:false ,
              fullWidth: false,
              position: "bottom",
              labels: {
                boxWidth: 10,
                // This more specific font property overrides the global property
                fontSize: 10,
              },
            },
            // responsive: true,
            maintainAspectRatio: false,
            cutoutPercentage: "60",
            rotation: Math.PI,
            circumference: 2 * Math.PI,
          },
        });
      }
    }

    products_divs.forEach((container) => {
      container.classList.add("hidden");
      container.classList.remove("analysis--div");
    });

    // bar graph to show sale of product by size
    const Product_size_performance = document.querySelectorAll(
      "#analysis div > div#sale-size-performance-graph canvas"
    );
    for (var i = 0; i < Product_size_performance.length; i++) {
      const Product_Object_Analysis = data["analysis"][i].performance;
      // console.log(Product_Object_Analysis);
      if (Product_Object_Analysis.wholesale_sizes.data.length > 0) {
        new Chart(Product_size_performance[i], {
          type: "bar",
          data: {
            labels: Product_Object_Analysis.wholesale_sizes.sizes,
            datasets: [
              {
                backgroundColor: "rgba(255, 165, 0,1.0)",
                data: Product_Object_Analysis.wholesale_sizes.data,
              },
            ],
          },
          options: {
            title: {
              display: true,
              text: "Size sale performance",
              // position:"left"
            },
            legend: { display: false },
            scales: {
              yAxes: [
                {
                  gridLines: {
                    display: false,
                  },
                  ticks: {
                    max:
                      Math.max(
                        ...Product_Object_Analysis.wholesale_sizes.data
                      ) + 2,
                    stepSize:
                      Math.ceil(
                        Math.max(
                          ...Product_Object_Analysis.wholesale_sizes.data
                        ) /
                          Math.min(
                            ...Product_Object_Analysis.wholesale_sizes.data
                          ) /
                          10
                      ) * 10,
                    beginAtZero: true,
                  },
                },
              ],
            },
          },
        });
      } else {
        Product_size_performance[i].closest("div").remove();
      }
    }
    const Product_colour_performance = document.querySelectorAll(
      "#analysis div > div#sale-colour-performance-graph canvas"
    );
    for (var i = 0; i < Product_colour_performance.length; i++) {
      const Product_Object_Analysis = data["analysis"][i].performance;
      // console.log(Product_Object_Analysis.wholesale_colours.data.length > 0);
      if (Product_Object_Analysis.wholesale_colours.data.length > 0) {
        new Chart(Product_colour_performance[i], {
          type: "bar",
          data: {
            labels: Product_Object_Analysis.wholesale_colours.colours,
            datasets: [
              {
                backgroundColor: "rgba(255, 165, 0,1.0)",
                data: Product_Object_Analysis.wholesale_colours.data,
              },
            ],
          },
          options: {
            title: {
              display: true,
              text: "Colour sale performance",
              // position:"left"
            },
            legend: { display: false },
            scales: {
              yAxes: [
                {
                  gridLines: {
                    display: false,
                  },
                  ticks: {
                    max:
                      Math.max(
                        ...Product_Object_Analysis.wholesale_colours.data
                      ) + 2,
                    stepSize:
                      Math.ceil(
                        Math.max(
                          ...Product_Object_Analysis.wholesale_colours.data
                        ) /
                          Math.min(
                            ...Product_Object_Analysis.wholesale_colours.data
                          ) /
                          10
                      ) * 10,
                    beginAtZero: true,
                  },
                },
              ],
            },
          },
        });
      } else {
        Product_colour_performance[i].closest("div").remove();
      }
    }
  });
});

/*
var options = {
  type: 'doughnut',
  data: {
    labels: ["Red", "grey"
    // , "Yellow", "Green", "Purple", "Orange"
  ],
    datasets: [{
      // label: '# of Votes',
      data: [12,12],
      backgroundColor: ["Red", "grey"],
      // borderWidth:1,
      // cutout:'95%',
      // needleValue: 50,
      // borderColor: "blue",
      // borderWidth: 1,
      // cutoutPercentage: "80",
      // circumference: 180,
      // rotation: 270,
      
    // borderRadius: 5,
  }]
},
options: {
  // cutout:"50%",
  cutoutPercentage: "90",
  // borderWidth:2,
  roundedCorners: true,
  borderRadius: 45,
  // borderRadius: 5,
  rotation: -1.0 * Math.PI, // start angle in degrees
    circumference: Math.PI, // sweep angle in degrees
  }
}

var ctx = document.getElementById('chartJSContainer').getContext('2d');
new Chart(ctx, options);
// });
*/

Product_selection.addEventListener("change", function () {
  const product = document.querySelector("#products option:checked").innerHTML;
  const product_div = document.querySelector(`#analysis > div.${product}`);
  const product_containers = document.querySelectorAll(`#analysis > div`);

  product_containers.forEach((container) => {
    container.classList.add("hidden");
    container.classList.remove("analysis--div");
  });
  product_div.classList.toggle("hidden");
  product_div.classList.toggle("analysis--div");

  // console.log(product_div);
});
