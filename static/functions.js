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

// get the cookie in the website
const cookies = document.cookie;

// create a cookie array
const cookie_array = cookies.split("=");

// get index of the crsf key word
const crsf_key = cookie_array.indexOf("csrftoken");
const crsf_token = cookie_array[crsf_key + 1];

// functions to blur and unblur an element
const blur_element = (element) => {
  element.classList.add("blur");
};

const unblur_element = (element) => {
  element.classList.remove("blur");
};

// Change the Return status of sale objects in the db
const change_return = (element) => {
  element.addEventListener("click", function () {
    let value = element.previousElementSibling.innerHTML;
    let bool = false;

    // if status is false
    if (value == "False") {
      bool = confirm("Do you want to change status to returned");
    } else {
      bool = confirm("Do you want to change status to not returned");
    }

    if (bool == true) {
      // declare object to be sent to servers and set its properties
      const parent = element.closest("tr").cells;
      element.insertAdjacentHTML(
        "afterend",
        `<i class="fa-solid fa-spinner fa-spin-pulse"></i>`
      );
      element.classList.add("hidden");
      // element.setAttribute("d")
      let sale_data = {};
      // const sales_data{"name","data"} = "yes",
      sale_data["name"] = parent[0].innerHTML;
      sale_data["size"] = parent[1].innerHTML;
      sale_data["colour"] = parent[2].innerHTML;
      sale_data["shop"] = parent[3].innerHTML;
      sale_data["return"] = value;
      sale_data["pay"] = parent[5].firstElementChild.innerHTML;

      let reponse = fetch("changereturn", {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "X-CSRFToken": `${crsf_token}`,
        },
        body: JSON.stringify(sale_data),
      }).then(function (response) {
        if (response.status !== 200) {
          console.log("ERROR");
        }
        response.json().then(function (data) {
          if ((data["message"] = "success")) {
            alert("successfully changed status");
            element.previousElementSibling.innerHTML =
              "returned" == value ? "False" : "returned";
            element.classList.remove("hidden");
            element.nextElementSibling.remove();
            element.remove();
            alert("successfully changed status");
          }
        });
      });
    }
  });
};

// Change the pay status of the sale object in the db
const change_pay = (element) => {
  element.addEventListener("click", function () {
    let value = element.previousElementSibling.innerHTML;
    let bool = false;

    // if status is false
    if (value == "False") {
      bool = confirm("Do you want to change status to paid");
    } else {
      bool = confirm("Do you want to change status to not paid");
    }
    if (bool == true) {
      // declare object to be sent to servers and set its properties
      const parent = element.closest("tr").cells;
      element.insertAdjacentHTML(
        "afterend",
        `<i class="fa-solid fa-spinner fa-spin-pulse"></i>`
      );
      element.classList.add("hidden");

      let sale_data = {};

      sale_data["name"] = parent[0].innerHTML;
      sale_data["size"] = parent[1].innerHTML;
      sale_data["colour"] = parent[2].innerHTML;
      sale_data["shop"] = parent[3].innerHTML;
      sale_data["return"] = parent[4].firstElementChild.innerHTML;
      sale_data["pay"] = value;

      let reponse = fetch("changepay", {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "X-CSRFToken": `${crsf_token}`,
        },
        body: JSON.stringify(sale_data),
      }).then(function (response) {
        if (response.status !== 200) {
          console.log("ERROR");
        }
        response.json().then(function (data) {
          if ((data["message"] = "success")) {
            element.previousElementSibling.innerHTML =
              "paid" == value ? "False" : "paid";
            element.nextElementSibling.remove();
            element.classList.remove("hidden");
            alert("successfully changed status");
          }
        });
      });
    }
  });
};

const Show_error_messages = (error_element, value, css_class) => {
  error_element.innerHTML = value;
  error_element.classList.remove("hide");
  error_element.classList.add(css_class);
  setTimeout(() => {
    error_element.classList.add("hide");
  }, 5000);
};

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
