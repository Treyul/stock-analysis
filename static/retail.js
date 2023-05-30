"use strict";

// select elements
const table_header = document.getElementById("sales_header");
const Submit_sales = document.getElementById("submit_sales");
const return_status = document.querySelectorAll(".return");
const pay_status = document.querySelectorAll(".paid");
const search = document.querySelector(".search");
const table = document.querySelector("table");
const form = document.querySelector("form");
const error = document.getElementById("error");

/*************************************/
// function to blur element

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
// create function to verify correct data is sent
const form_verify = (element) => {
  if (element.value == "") {
    error.innerHTML = `${element.name} should be included`;
    error.classList.add("error");
    error.classList.remove("hide");
    setTimeout(() => {
      error.classList.add("hide");
      error.classList.remove("error");
    }, 5000);
    Submit_sales.value = "Submit";
    Submit_sales.removeAttribute("disabled");
    return false;
  } else return true;
};
//
Submit_sales.addEventListener("click", function (e) {
  e.preventDefault();
  Submit_sales.setAttribute("disabled", "True");
  Submit_sales.value = "Loading...";

  // initialize sales record object
  const product = document.getElementById("id_product");
  const name = document.getElementById("id_shop");
  const amount = document.getElementById("id_amount");
  const size = document.getElementById("id_size");
  const colour = document.getElementById("id_colour");
  const buyer = document.getElementById("id_buyer");
  const paid = document.getElementById("id_paid");

  // catch error in data to be submitted
  if (!form_verify(product)) return;
  else if (!form_verify(size)) return;
  else if (!form_verify(colour)) return;
  else if (!form_verify(name)) return;
  console.log(form_verify(name));
  if (amount.value == "" || +amount.value <= 0) {
    error.innerHTML = "Price should be included";
    error.classList.add("error");
    error.classList.remove("hide");
    Submit_sales.value = "Submit";
    Submit_sales.removeAttribute("disabled");
    setTimeout(() => {
      error.classList.add("hide");
      error.classList.remove("error");
    }, 5000);
    return;
  }

  const product_data = {
    product: product.value,
    color: colour.value,
    amount: +amount.value,
    paid: paid.checked,
    sizes: size.value,
    name: name.value,
  };
  if (buyer.value.trim() != "") product_data["buyer"] = buyer.value.trim();

  let response = fetch("/sales/retail", {
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
          error.classList.remove("error");
        }, 5000);
      } else if (data["message"] != "error") {
        // show user sale was successfully added
        error.innerHTML = "Successfully added sale";
        error.classList.remove("hide");
        error.classList.add("success");
        setTimeout(function () {
          console.log("test");
          error.classList.add("hide");
          error.classList.remove("success");
        }, 5000);

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

        setTimeout(function () {
          error.classList.add("hide");
        }, 5000);
      }
      Submit_sales.value = "Submit";
      Submit_sales.removeAttribute("disabled");
    });
  });
});
