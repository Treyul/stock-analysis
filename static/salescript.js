"use strict";
// select elements
const table_header = document.getElementById("sales_header");
const Submit_sales = document.getElementById("submit_sales");
const return_status = document.querySelectorAll(".return");
const pay_status = document.querySelectorAll(".paid");
const search = document.querySelector(".search");
const error = document.getElementById("error");
const table = document.querySelector("table");
const form = document.querySelector("form");
const sale_submit_icon = document.getElementById("sale_submit_loading");

/*************************************/
// functions to hide elements
const hide = (element) => {
  element.classList.add("hidden");
};
const show = (element) => {
  element.classList.remove("hidden");
};

return_status.forEach((element) => {
  change_return(element);
});

// Change status of payments
pay_status.forEach((element) => {
  change_pay(element);
});

Submit_sales.addEventListener("click", function (e) {
  e.preventDefault();
  Submit_sales.classList.add("hidden");
  sale_submit_icon.classList.remove("hidden");

  // initialize sales record object
  const product = document.getElementById("id_product");
  const name = document.getElementById("id_name");
  const size = document.getElementById("id_size");
  const colour = document.getElementById("id_colour");
  const paid = document.getElementById("id_paid");

  // create object that will be sent to server
  const product_data = {
    product: product.value,
    color: colour.value,
    paid: paid.checked,
    name: name.value,
    sizes: size.value,
  };

  let response = fetch("/sales/", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "X-CSRFToken": `${crsf_token}`,
    },
    body: JSON.stringify(product_data),
  }).then(function (response) {
    // if there is an error in the server rendering
    if (response.status !== 200) {
      Show_error_messages(
        error,
        "Server error. \nPlease refresh page and try again.",
        "error"
      );
      Submit_sales.classList.remove("hidden");
      sale_submit_icon.classList.add("hidden");
    }

    response.json().then(function (data) {
      if (data["message"] == "error") {
        product.innerHTML = "";
        name.innerHTML = "";
        size.innerHTML = 0;
        colour.innerHTML = "";
        Show_error_messages(error, data["error"], "error");
        Submit_sales.classList.remove("hidden");
        sale_submit_icon.classList.add("hidden");
      } else if (data["message"] != "error") {
        Show_error_messages(error, data["success"], "success");
        Submit_sales.classList.remove("hidden");
        sale_submit_icon.classList.add("hidden");

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

        change_pay(pay);
        change_return(ret);

        product.value = "";
        name.value = "";
        size.value = 0;
        colour.value = "";
      }
    });
  });
});
