"use strict";
// select elements
const table_header = document.getElementById("sales_header");
const Submit_sales = document.getElementById("submit_sales");
const return_status = document.querySelectorAll(".return");
const pay_status = document.querySelectorAll(".paid");
const search = document.querySelector(".search");
const table = document.querySelector("table");
const form = document.querySelector("form");

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

return_status.forEach((element) => {
  change_return(element);
});

// Change status of payments
pay_status.forEach((element) => {
  change_pay(element);
});

Submit_sales.addEventListener("click", function (e) {
  e.preventDefault();
  Submit_sales.value = "Loading...";
  Submit_sales.setAttribute("disabled", "True");
  // TODO ensure field are not empty

  // initialize sales record object
  form.checkValidity();
  const product = document.getElementById("id_product");
  const name = document.getElementById("id_name");
  const size = document.getElementById("id_size");
  const colour = document.getElementById("id_colour");
  const paid = document.getElementById("id_paid");

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
    if (response.status !== 200) {
      console.log("ERROR");
    }
    // console.log(response.json());
    response.json().then(function (data) {
      // console.log(data);
      // console.log("here");
      if (data["message"] == "error") {
        const error = document.getElementById("error");
        product.innerHTML = "";
        name.innerHTML = "";
        size.innerHTML = 0;
        colour.innerHTML = "";
        Show_error_messages(error, data["error"], "error");
      } else if (data["message"] != "error") {
        Show_error_messages(error, data["success"], "success");

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

        // console.log(pay);

        change_pay(pay);
        change_return(ret);
        // console.log(template.getElementsByTagName("td"));
        // set input value to initial
        product.value = "";
        name.value = "";
        size.value = 0;
        colour.value = "";
        // console.log("passed");
      }
      Submit_sales.removeAttribute("disabled");
      Submit_sales.value = "Submit";
    });
  });
});
