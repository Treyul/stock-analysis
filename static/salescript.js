"use strict";
// select elements
const table_header = document.getElementById("sales_header");
const Add = document.getElementById("add_sale");
const return_status = document.querySelectorAll(".return");
const pay_status = document.querySelectorAll(".paid");
const search = document.querySelector(".search");
const table = document.querySelector("table");
const form = document.querySelector("form");
// const search_div = document.getElementById("search_div");

/****** Bootstrap script *************/

document.addEventListener("DOMContentLoaded", function () {
  /////// Prevent closing from click inside dropdown
  document.querySelectorAll(".dropdown-menu").forEach(function (element) {
    element.addEventListener("click", function (e) {
      e.stopPropagation();
    });
  });

  // make it as accordion for smaller screens
  if (window.innerWidth < 992) {
    // close all inner dropdowns when parent is closed
    document
      .querySelectorAll(".navbar .dropdown")
      .forEach(function (everydropdown) {
        everydropdown.addEventListener("hidden.bs.dropdown", function () {
          // after dropdown is hidden, then find all submenus
          this.querySelectorAll(".submenu").forEach(function (everysubmenu) {
            // hide every submenu as well
            everysubmenu.style.display = "none";
          });
        });
      });

    document.querySelectorAll(".dropdown-menu a").forEach(function (element) {
      element.addEventListener("click", function (e) {
        let nextEl = this.nextElementSibling;
        if (nextEl && nextEl.classList.contains("submenu")) {
          // prevent opening link if link needs to open dropdown
          e.preventDefault();
          console.log(nextEl);
          if (nextEl.style.display == "block") {
            nextEl.style.display = "none";
          } else {
            nextEl.style.display = "block";
          }
        }
      });
    });
  }
  // end if innerWidth
});
// DOMContentLoaded  end

/*************************************/
// function to blur element
const blur_element = (element) => {
  element.classList.add("blur");
};

const unblur_element = (element) => {
  element.classList.remove("blur");
};

// functions to hide elements
const hide = (element) => {
  element.classList.add("hidden");
};
const show = (element) => {
  element.classList.remove("hidden");
};

// hide modal window
// hide(search_div);
//show modal window for searching
// search.addEventListener("click", function () {
//   blur_element(form);
//   blur_element(table);
//   blur_element(search);
//   show(search_div);
// });

// define function for fetching change payment status
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
      // element.setAttribute("d")
      let sale_data = {};
      // const sales_data{"name","data"} = "yes",
      sale_data["name"] = parent[0].innerHTML;
      sale_data["size"] = parent[1].innerHTML;
      sale_data["colour"] = parent[2].innerHTML;
      sale_data["shop"] = parent[3].innerHTML;
      sale_data["return"] = parent[4].firstElementChild.innerHTML;
      sale_data["pay"] = value;

      let reponse = fetch("/changepay", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(sale_data),
      }).then(function (response) {
        if (response.status !== 200) {
          console.log("ERROR");
        }
        response.json().then(function (data) {
          console.log(data);
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

// change return
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

      let reponse = fetch("/changereturn", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(sale_data),
      }).then(function (response) {
        if (response.status !== 200) {
          console.log("ERROR");
        }
        response.json().then(function (data) {
          console.log(data);
          if ((data["message"] = "success")) {
            element.previousElementSibling.innerHTML =
              "returned" == value ? "False" : "returned";
            element.nextElementSibling.remove();
            element.classList.remove("hidden");
            alert("successfully changed status");
          }
        });
      });
    }
  });
};
return_status.forEach((element) => {
  element.addEventListener("click", function () {
    // get status value
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

      // fetch endpoint
      let response = fetch("/changereturn", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(sale_data),
      }).then(function (response) {
        if (response.status != 200) {
          console.log("ERROR");
        }
        response.json().then(function (data) {
          if ((data["message"] = "success")) {
            alert("successfully changed status");
            element.previousElementSibling.innerHTML =
              "returned" == value ? "False" : "returned";
            element.classList.remove("hidden");
            element.nextElementSibling.remove();
            // element.removeAttribute("disabled")
          }
          console.log(data);
        });
      });
    }
  });
});

// Change status of payments
pay_status.forEach((element) => {
  element.addEventListener("click", function () {
    // get status value
    let value = element.previousElementSibling.innerHTML;

    let bool = false;

    // if status is false
    if (value == "False") {
      bool = confirm("Do you want to change status to paid");
    } else {
      bool = confirm("Do you want to change status to not paid");
    }
    if (bool == true) {
      // Fetch endpoint from server
      console.log("print stat ");
      const parent = element.closest("tr").cells;
      element.insertAdjacentHTML(
        "afterend",
        `<i class="fa-solid fa-spinner fa-spin-pulse"></i>`
      );
      element.classList.add("hidden");
      console.log(parent);
      let sale_data = {};
      // set properties of the sale to be changed status
      sale_data["name"] = parent[0].innerHTML;
      sale_data["size"] = parent[1].innerHTML;
      sale_data["colour"] = parent[2].innerHTML;
      sale_data["shop"] = parent[3].innerHTML;
      sale_data["return"] = parent[4].firstElementChild.innerHTML;
      sale_data["pay"] = value;
      let response = fetch("/changepay", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(sale_data),
      }).then(function (response) {
        if (response.status != 200) {
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
          console.log(data);
        });
      });
    }
    // console.log(bool);
  });
});
Add.addEventListener("click", function (e) {
  e.preventDefault();
  console.log("print");

  let saledata = {};
  const product = document.getElementById("id_product");
  const name = document.getElementById("id_name");
  const size = document.getElementById("id_size");
  const colour = document.getElementById("id_colour");
  // const status = document.getElementById("id_status");
  const paid = document.getElementById("id_paid");

  const product_data = {
    color: `${colour.value}`,
    // status: `${status.checked}`,
    paid: `${paid.checked}`,
    name: `${name.value}`,
  };

  saledata[product.value] = {};
  saledata[product.value][size.value] = product_data;

  let response = fetch("/sales/retail", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(saledata),
  }).then(function (response) {
    if (response.status !== 200) {
      console.log("ERROR");
    }
    response.json().then(function (data) {
      if (data["message"] == "error") {
        const error = document.getElementById("error");

        error.innerHTML = data["error"];
        error.classList.remove("hide");
        error.classList.add("error");
        product.innerHTML = "";
        name.innerHTML = "";
        size.innerHTML = 0;
        colour.innerHTML = "";
        setTimeout(function () {
          console.log("test");
          error.classList.add("hide");
        }, 5000);
      } else if (data["message"] != "error") {
        // show user sale was successfully added
        error.innerHTML = "Successfully added sale";
        error.classList.remove("hide");
        error.classList.add("success");

        // append data to sales table
        // initialize template
        let template = `<tr> 
        <td>${product.value}</td>
        <td>${size.value}</td>
        <td>${product_data.color}</td>
        <td>${product_data.name}</td>
        <td><p>False</p><input type="button" value="Change" class="status return" /></td>
        <td><p>${
          product_data.paid == "true" ? "paid" : "False"
        }</p><input type="button" value="Change" class="status paid" /></td>
  </tr>`;
        table_header.insertAdjacentHTML("afterend", template);

        // get added html element
        const row = table_header.nextElementSibling;

        const pay = row.querySelector(".paid");
        const ret = row.querySelector(".return");

        console.log(pay);

        change_pay(pay);
        change_return(ret);
        // console.log(template.getElementsByTagName("td"));
        // set input value to initial
        product.value = "";
        name.value = "";
        size.value = 0;
        colour.value = "";
        console.log("passed");

        setTimeout(function () {
          error.classList.add("hide");
        }, 5000);
      }
    });
  });
});
