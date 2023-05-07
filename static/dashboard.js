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
  });
});

// });
