// get elements
const current_year_revenue = document.getElementById("current_year_revenue");
const current_year_volume = document.getElementById("current_year_volume");
const show_sale_details = document.querySelectorAll(".retail-show-btn");
const retail_data = document.querySelector(".retail-data");
const retail_table = retail_data.querySelector("table");
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

// fiunctions
// get data from table cells
const derive_data = (cell) => {
  const p_tag = cell.querySelector("p");
  const data = p_tag.innerHTML;
  return data;
};

const get_shop_no = (button) => {
  const parent_div = button.closest(".retail-details");

  const summary_div = parent_div.previousElementSibling;

  const shop_no = summary_div.firstElementChild.innerHTML;

  return shop_no;
};

// get buttons for updating analysis
const retail_buttons = document.querySelectorAll(".brokered");
const wholesale_buttons = document.querySelectorAll(".shop");

// event listener to toggle the analysis data
show_sale_details.forEach((button) => {
  button.addEventListener("click", function () {
    // select parent element
    const parent_div = button.closest("div");

    button.value == "Show" ? (button.value = "Hide") : (button.value = "Show");

    // select the container for the details
    const details = parent_div.nextElementSibling;

    details.classList.toggle("hidden");
  });
});

// iterate between the shop sales
retail_buttons.forEach((button) => {
  // for each button add the event listener to change pay status
  button.addEventListener("click", function () {
    // prompt user if he is sure he wants to change status
    const Change_Status = confirm("Are you sure you want to change to Sorted?");

    const parent_div = button.closest(".retail-details");

    const summary_div = parent_div.previousElementSibling;

    const shop_no = summary_div.firstElementChild.innerHTML;

    const summary = summary_div.querySelectorAll("p");

    if (Change_Status) {
      const parent = button.closest("tr");
      const parent_row = button.closest("tr").cells;
      console.log(parent_row);

      // initialize JSON object
      let object_data = {};

      object_data["product"] = derive_data(parent_row[0]);
      object_data["colour"] = derive_data(parent_row[2]);
      object_data["size"] = derive_data(parent_row[3]);
      object_data["date"] = derive_data(parent_row[4]);
      object_data["shop"] = shop_no;

      // fetch endpoint to change status
      let response = fetch("retailsort", {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "X-CSRFToken": `${crsf_token}`,
        },
        body: JSON.stringify(object_data),
      }).then(function (response) {
        if (response.status != 200) {
          console.log("ERROR");
        }
        response.json().then(function (data) {
          if (data["message"] == "success") {
            summary[1].innerHTML = +summary[1].innerHTML - 1;
            summary[2].innerHTML =
              +summary[2].innerHTML - +derive_data(parent_row[1]);
            parent.remove();
          }
        });
      });
    } else {
      return;
    }
  });
});

// iterate between the shop sales
wholesale_buttons.forEach((button) => {
  // for each button add the event listener to change pay status
  button.addEventListener("click", function () {
    // prompt user if he is sure he wants to change status
    const Change_Status = confirm("Are you sure you want to change to Sorted?");

    const parent_div = button.closest(".retail-details");

    const summary_div = parent_div.previousElementSibling;

    const shop_no = summary_div.firstElementChild.innerHTML;

    const summary = summary_div.querySelectorAll("p");

    if (Change_Status) {
      const parent = button.closest("tr");
      const parent_row = button.closest("tr").cells;
      console.log(parent_row);

      // initialize JSON object
      let object_data = {};

      object_data["product"] = derive_data(parent_row[0]);
      object_data["colour"] = derive_data(parent_row[2]);
      object_data["size"] = derive_data(parent_row[3]);
      object_data["date"] = derive_data(parent_row[4]);
      object_data["shop"] = shop_no;
      // fetch endpoint to change status
      let response = fetch("sort", {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "X-CSRFToken": `${crsf_token}`,
        },
        body: JSON.stringify(object_data),
      }).then(function (response) {
        if (response.status != 200) {
          console.log("ERROR");
        }
        response.json().then(function (data) {
          if (data["message"] == "success") {
            summary[1].innerHTML = +summary[1].innerHTML - 1;
            summary[2].innerHTML =
              +summary[2].innerHTML - +derive_data(parent_row[1]);
            parent.remove();
          }
          console.log(data);
        });
      });
    } else {
      return;
    }
  });
});
