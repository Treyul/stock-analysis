"use strict";

/*
 *catch error for empty fields and incorrect max and min sizes when next page is clicked
 *remove add color button when next page is clicked
 *During tabulation ensure all done buttons are clicked before enabling submition of form
 */
const colour = document.getElementById("addColours");
const type = document.getElementById("stock_type");
const fields = document.querySelectorAll(".form");
const next_stock_details = document.getElementById("add_stock_next");
const list = document.getElementById("colours");
const form = document.getElementById("form_add_stock");
const submit = document.getElementById("stock_det");
document.getElementsByTagName;
const clothes = fields[2];
const max_shoes = fields[3];
const min_shoes = fields[4];

const hide = (el) => {
  el.classList.add("hidden");
};
hide(max_shoes);
hide(min_shoes);
hide(fields[7]);
hide(fields[6]);

type.addEventListener("input", function () {
  if (type.value == "Shoes") {
  } else if (type.value == "Clothes") {
  }
  clothes.classList.toggle("hidden");
  max_shoes.classList.toggle("hidden");
  min_shoes.classList.toggle("hidden");
  max_shoes.classList.toggle("inline");
  min_shoes.classList.toggle("inline");
});

next_stock_details.addEventListener("click", function (e) {
  next_stock_details.classList.add("hidden");
  colour.classList.add("hidden");
  colour.classList.remove("add_sale");
  submit.classList.remove("hidden");
  e.preventDefault();

  // create object to store the product variation
  let stock_json = {};
  const max_size = +document.getElementById("max_size").value;
  let min_size = +document.getElementById("min_size").value;

  // get no of sizes available for the product
  let variation = max_size - min_size + 1;

  // get colours available and their number
  const colours = list.getElementsByTagName("input");
  const len = colours.length;

  // create table to alloe use input for th product variation
  let variation_template = `<table> <tr><th>Size</th>`;

  // create table columns for the colors
  for (const el of colours) {
    variation_template += `<th> ${el.value}</th>`;
  }
  variation_template += `<th>Total</th></tr>`;

  // create table ros for the sizes
  for (min_size; min_size <= max_size + 1; min_size++) {
    // create final tallying row
    if (min_size == max_size + 1) {
      variation_template += `<tr><td>Total</td>`;
    } else {
      // size row
      variation_template += `<tr><td>${min_size}</td>`;
    }

    // create input fields for the number of shoes in a colour and size
    for (let k = 0; k < len; k++) {
      variation_template += `<td><input type="number" value="0"></td>`;
    }

    // create totaling button for the row
    variation_template += `<td><input type="number" disabled value="0"></td><td>
    <input type="button" class="summation" value="Done"></td></tr>`;
  }

  // close the table and append it to the page
  variation_template += `</table>`;
  fields[fields.length - 1].insertAdjacentHTML("afterend", variation_template);

  // get all totalling button s and add functionality
  const summation_buttons = document.querySelectorAll(".summation");

  summation_buttons.forEach((element) => {
    element.addEventListener("click", function () {
      // get row to be totalled  and columns
      const parent = element.closest("tr");
      const siblings = parent.getElementsByTagName("td");

      // put functionality for final tallying
      if (siblings[0].innerHTML == "Total") {
        // iterate between columns
        for (let r = 0; r <= colours.length; r++) {
          let sum = 0;

          if (r == colours.length) {
            for (let rs = 0; rs < colours.length; rs++) {
              sum += +siblings[rs + 1].getElementsByTagName("input")[0].value;
              console.log(sum);
            }
            siblings[r + 1].getElementsByTagName("input")[0].value = sum;
            fields[6].getElementsByTagName("input")[0].value =
              JSON.stringify(stock_json);
          } else if (r < colours.length) {
            // iterate between variation object colors
            for (const [key, val] of Object.entries(stock_json)) {
              // get summation of the color in each size
              sum += +val[`${colours[r].value}`];
            }

            // make summation of color visible
            siblings[r + 1].getElementsByTagName("input")[0].value = sum;
          }
        }
        console.log("done");
      } else {
        // initailze sum and size object to store the color variation
        let sum = 0;
        let size = {};

        // iterate between color columns
        for (let i = 1; i < siblings.length - 2; i++) {
          // get size number and update summation
          size[`${colours[i - 1].value}`] =
            +siblings[i].getElementsByTagName("input")[0].value;
          sum += +siblings[i].getElementsByTagName("input")[0].value;
        }

        // show total tally for the row
        siblings[siblings.length - 2].getElementsByTagName("input")[0].value =
          sum;

        stock_json[`${siblings[0].innerHTML}`] = size;
        // console.log(typeof siblings[0].innerHTML);
        console.log(stock_json);
        element.classList.add("green");
      }
    });
  });
});

let count = 1;
colour.addEventListener("click", function (e) {
  e.preventDefault();
  let label = `colours-${count}`;

  list.insertAdjacentHTML(
    "beforeend",
    `<li>
  <label for="${label}">Colour</label>
  <input id="${label}" name="${label}" type="text">
  </li>`
  );
  count++;
});
