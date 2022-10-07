"use strict";

const sale_records = document.getElementById("Sales_data");
let add_sales = document.querySelectorAll(".add_sale");
const sales = document.getElementById("sales");

const add_events = (addbtns, no) => {
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
      console.log(data);
    });
  });
  console.log(saledata);
});
