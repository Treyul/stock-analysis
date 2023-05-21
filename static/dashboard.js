const toggle_abstract_class = (button, className) => {
  const parent = button.closest("div");

  const sibling = parent.nextElementSibling;

  const child = sibling.nextElementSibling;

  const variation_btn = sibling.querySelector("button");

  variation_btn.innerHTML = "Show variation";

  sibling.classList.toggle("hidden");
  child.className = "hidden";
  sibling.classList.toggle(className);

  const btn_html = button.innerHTML;

  btn_html == "Show"
    ? (button.innerHTML = "Hide")
    : (button.innerHTML = "Show");
};

const toggle_detail_class = (button, className) => {
  const parent = button.closest("div");

  const sibling = parent.nextElementSibling;

  btn_html = button.innerHTML;

  btn_html == "Show variation"
    ? (button.innerHTML = "Hide variation")
    : (button.innerHTML = "Show variation");

  sibling.classList.toggle("hidden");
  sibling.classList.toggle(className);
};

const worth_summation = (container) => {
  const worth_container = container.querySelectorAll(".worth");
  const quantity_container = container.querySelectorAll(".quantity");

  let worth_sum = 0;
  let quantity_sum = 0;

  for (i = 0; i < worth_container.length; i++) {
    if (worth_container[i] != "") {
      worth_sum += Number(worth_container[i].innerHTML);
    }
    quantity_sum += Number(quantity_container[i].innerHTML);
  }

  worth_container[0].innerHTML = worth_sum;
  quantity_container[0].innerHTML = quantity_sum;

  if (worth_container.length > 1) {
    for (i = 1; i < worth_container.length; i++) {
      worth_container[i].remove();
      quantity_container[i].remove();
    }
  }
};

const Show_Abstract = document.querySelectorAll(".showabstract");
const Show_Detailed = document.querySelectorAll(".showdetailed");
const worth_Containers = document.querySelectorAll("#worthsum");
const Show_Order_abtr = document.querySelectorAll(".show-order-abtr");
const Show_Order_deets = document.querySelectorAll(".show-order-var");
const Show_Worth_deets = document.querySelectorAll(".show-worth-deets");
const Sales_analysis_chart = document.getElementById("sales_analysis");

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
              ticks: {
                beginAtZero: true,
              },
            },
          ],
        },
      },
    });


    // gauge graphs for product performance
    const graph_containers = document.querySelectorAll("#analysis div > div#graph canvas")

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
      }
  });

  // display the gauges for each product
    for(var i = 0; i < graph_containers.length; i++)
    {
      const obj_desc = data["analysis"][i]
      new Chart(graph_containers[i],{
        type: 'doughnut',
        data:{
          labels:["sold","remaining"],
          datasets:[{
            // 
            data:[(obj_desc.ordered-obj_desc.available),obj_desc.available],
            backgroundColor: ["lightgreen","lightgrey"]
          }]
        },
        options:{
          centerArea: {
            text: 'Title',
            subText: 'Subtitle',
          },
          // title:{
          //   position:"bottom",
          //   display:true,
          //   text:
          //   ,padding:0
          // },
          centertext: `${(obj_desc.ordered-obj_desc.available)/obj_desc.ordered*100}% sold`,
          legend: {
            // display:false ,
            fullWidth:false,
            position:'bottom',
            labels: {
              boxWidth:10,
                // This more specific font property overrides the global property
                fontSize: 10
                         }
        },
          // responsive: true,
          maintainAspectRatio: false,
          cutoutPercentage:"90",
          rotation:-1.25 * Math.PI,
          circumference:1.5 * Math.PI
        }
      })
    }
    const Product_line_graphs = document.querySelectorAll("#analysis div > div#sale-line-graph canvas")
    for (var i = 0; i < Product_line_graphs.length; i++)
    {
      const obj_desc = data["analysis"][i].sales_history
      // console.log(obj_desc);
      new Chart(Product_line_graphs[i],{
        type:"line",
        data:{
          labels:obj_desc[0],
          datasets:[{
            label:"sales",
            data:obj_desc[1],
            backgroundColor:"rgb(100, 149, 237)",
            borderColor: 'white'


          }]
        },
              options: {
        title: {
          display: true,
          text: "Product performance",
        },
        legend: { display: false },
        scales: {
          yAxes: [
            {gridLines:{
            display:false,
          },
              ticks: {
                max:Math.max(...obj_desc[1])+1,
            stepSize: Math.ceil(Math.max(...obj_desc[1])/5),
                beginAtZero: true,
              },
            },
          ],
        },
      },
      })
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
