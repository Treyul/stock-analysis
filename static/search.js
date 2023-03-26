/*************    Defination of functions  **************/
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

      let reponse = fetch("/sales/changepay", {
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

/************   selct elements  ******************/
const submit = document.getElementById("submit");
const form = document.querySelector("form");

// get the cookies in the website
const cookies = document.cookie;

// create a cookie array
const cookie_array = cookies.split("=");

// get index of the crsf key word
const crsf_key = cookie_array.indexOf("csrftoken");
const crsf_token = cookie_array[crsf_key + 1];

submit.addEventListener("click", function (e) {
  e.preventDefault();
  console.log("print");

  //   get value of the input fields
  const product = document.getElementById("id_product");
  const shop = document.getElementById("id_shop_number");
  const size = document.getElementById("id_size");
  const colours = document.getElementById("id_colour");
  const start_date = document.getElementById("id_start_date");
  const end_date = document.getElementById("id_end_date");

  // validate date range data
  // initialize JSON object
  filters = {};

  // tets value of the input fields
  if (product.value.trim() != "") {
    filters["product"] = product.value.trim().split(" ")[0];
  }
  if (shop.value.trim() != "") {
    filters["shop_no"] = shop.value.trim().split(" ")[0];
  }
  if (size.value.trim() != "") {
    filters["size"] = size.value.trim().split(" ")[0];
  }
  if (colours.value.trim() != "") {
    filters["colour"] = colours.value.trim().split(" ")[0];
  }
  if (start_date.value != "") filters["start_date"] = start_date.value;
  if (end_date.value != "") filters["end_date"] = end_date.value;
  console.log(filters);

  //get tables displayed in the page
  const tables = document.querySelectorAll("table");

  // delete the tables
  tables.forEach((table) => {
    table.remove();
  });

  fetch("/sales/search", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "X-CSRFToken": `${crsf_token}`,
    },
    body: JSON.stringify(filters),
  }).then(function (response) {
    if (response.status != 200) {
      console.log("ERROR");
      console.log(filters);
    }

    response.json().then(function (data) {
      if (data["message"] == "success") {
        console.log(data);
        // get data arrays for the results
        const wholesale_results = data["wholesale results"];
        const retail_results = data["retail results"];

        console.log(wholesale_results, retail_results);

        //create tables fro the results if they exist
        if (retail_results.length > 0 || wholesale_results.length > 0) {
          // initialize template
          let retail_template = `<table class="retail">
          <tr><th colspan=6>Retail sales</th><tr/>
          <tr>
          <th>Product</th>
          <th>size</th>
          <th>Colour</th>
          <th>Shop no</th>
          <th>return</th>
          <th>paid</th>
          </tr>`;

          // insert data into table
          if (retail_results.length > 0) {
            // create through results array
            for (let i = 0; i < retail_results.length; i++) {
              const result = retail_results[i];
              retail_template += `<tr>
              <td>${result["product"]}</td>
              <td>${result["size"]}</td>
              <td>${result["colour"]}</td>
              <td>${result["shop_no"]}</td>
              <td>${
                result["status"] == false
                  ? `False <input type="button" value="Change" class="status return" />`
                  : returned
              }</td>
            <td>${
              result["paid"] == false
                ? `False <input type="button" value="Change" class="status paid" />`
                : "returned"
            }</td>
              </tr>`;
            }

            // append template into the page
            form.insertAdjacentHTML("afterend", retail_template);

            // select tables
            const retail_table = document.querySelector(
              "table[class='retail']"
            );

            //select the buttons for changing the return and payment status
            const retail_pay_btns = retail_table.querySelectorAll(".paid");
            const retail_return_btns = retail_table.querySelectorAll(".return");

            // add event listners to th buttons
            retail_pay_btns.forEach((button) => {
              button.addEventListener("click", function () {
                // select the parent table row
                const parent = button.closest("tr");
                console.log(parent);
              });
            });
            retail_return_btns.forEach((button) =>
              button.addEventListener("click", function () {
                // select the parent table row
                const parent = button.closest("tr");
                console.log(parent);
              })
            );
          }

          let wholesale_template = `<table class="wholesale">
          <tr><th colspan=5>Wholesale sales</th><tr/>
        <tr>
        <th>Product</th>
        <th>size</th>
        <th>Colour</th>
        <th>Shop no</th>
        <th>return</th>
        <th>Paid</th>
        </tr>`;
          if (wholesale_results.length > 0) {
            // create table and headings for the wholesale results

            // iterate through results array
            for (let i = 0; i < wholesale_results.length; i++) {
              const result = wholesale_results[i];
              wholesale_template += `<tr>
              <td>${result["product"]}</td>
              <td>${result["size"]}</td>
              <td>${result["colour"]}</td>
              <td>${result["shop_no"]}</td>
              <td>${
                result["status"] == false
                  ? `<p>False</p> <input type="button" value="Change" class="status return" />`
                  : "<p>returned</p>"
              }</td>
              <td>${
                result["paid"] == false
                  ? `<p>False</p> <input type="button" value="Change" class="status paid" />`
                  : '<p>paid </p> <input type="button" value="Change" class="status paid" />'
              }</td>
              </tr>`;
            }
            form.insertAdjacentHTML("afterend", wholesale_template);
            const wholesale_table = document.querySelector(
              "table[class='wholesale']"
            );
            const wholesale_pay_btns =
              wholesale_table.querySelectorAll(".paid");
            const wholesale_return_btns =
              wholesale_table.querySelectorAll(".return");
            wholesale_pay_btns.forEach((button) => change_pay(button));
            wholesale_return_btns.forEach((button) => change_return(button));
          }

          // console.log(retail_pay_btns, retail_return_btns);

          //
        } else {
        }
      }
    });
  });
});
