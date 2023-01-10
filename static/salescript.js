"use strict";

// const sale_records = document.getElementById("Sales_data");
// let add_sales = document.querySelectorAll(".add_sale");
// const sale = { sales };
const Add = document.getElementById("add_sale");

Add.addEventListener("click", function (e) {
  e.preventDefault();
  console.log("print");

  let saledata = {};
  const product = document.getElementById("product");
  const name = document.getElementById("name");
  const size = document.getElementById("size");
  const colour = document.getElementById("colour");
  const status = document.getElementById("status");
  const paid = document.getElementById("paid");

  const product_data = {
    color: `${colour.value}`,
    status: `${status.checked}`,
    paid: `${paid.checked}`,
    name: `${name.value}`,
  };

  saledata[product.value] = {};
  saledata[product.value][size.value] = product_data;

  let response = fetch("/sales", {
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
        error.innerHTML = "Successfully added sale";
        error.classList.remove("hide");
        error.classList.add("success");
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

/*const add_events = (addbtns, no) => {
  addbtns.forEach((element) => {
    element.addEventListener("click", function () {
      const parent = element.closest("div");
      const duplicate = parent.firstElementChild.outerHTML;
      element.insertAdjacentHTML("beforebegin", duplicate);
      //   console.log(duplicate);
      //   console.log("done");
      //   console.log(add_sales);
      const updated_sales = document.querySelectorAll(".add_sale");
      if (add_sales.length != updated_sales.length) {
        let temp1 = Array.from(add_sales);
        let updatetemp = Array.from(updated_sales);
        // console.log(Array.from(updated_sales));
        updatetemp = updatetemp.filter((el) => {
          //   console.log(el);
          let i = 0;
          let bool = false;
          for (i; i < temp1.length; i++) {
            if (el == temp1[i]) {
              bool = true;
            }
          }
          if (!bool) {
            return !bool;
          }
        });
        // add_sales = updated_sales;
        add_sales = updated_sales;
        add_events(updatetemp);
      } else {
        return;
      }
      //   return;
    });
  });
};
add_events(add_sales);

sales.addEventListener("click", function (e) {
  e.preventDefault();
  let saledata = {};
  const product_names = sale_records.querySelectorAll(".Sale_name");
  product_names.forEach((el) => {
    const pkey = el.firstElementChild.value;
    saledata[pkey] = {};
    const product_sizes = el.querySelectorAll(".Sale_sizes > div");
    product_sizes.forEach((size) => {
      const selement = size;
      const skey = selement.firstElementChild.value;
      console.log(size);
      let tempobj = {};
      const colparent = selement.querySelectorAll("#Sale_Colour > div");
      colparent.forEach((val) => {
        const color = val.firstElementChild.value;
        const sold = +val.lastElementChild.value;
        tempobj[color] = sold;
      });
      saledata[pkey][skey] = tempobj;
    });
  });
  let response = fetch("/sales", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(saledata),
  }).then(function (response) {
    if (response.status !== 200) {
      console.log("ERROR");
    }
    response.json().then(function (data) {
      console.log(data["message"]);
      if (data["message"] == "error") {
        const error = document.getElementById("error");

        error.innerHTML = data["error"];
        error.classList.remove("hidden");
      }
    });
  });
  console.log(saledata);
});
*/
