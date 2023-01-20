"use strict";

const colour = document.getElementById("addColours");
const stock_type = document.getElementById("stock_type");
const clothes = document.getElementById("clothing");
const max_shoes = document.getElementById("max_size");
const min_shoes = document.getElementById("min_size");
const interval = document.getElementById("interval");
const Colour_list = document.getElementById("colours");
const form = document.getElementById("form_add_stock");
const submit = document.getElementById("stock_det");
const next_stock_details = document.getElementById("add_stock_next");
const submit_stock_details = document.getElementById("add_stock");
const stock_data = document.getElementById("stock_data");
const alert_msg = document.getElementById("message");

/*
 *catch error for empty fields and incorrect max and min sizes when next page is clicked
 *remove add color button when next page is clicked
 *During tabulation ensure all done buttons are clicked before enabling submition of form
 */
// function for adding display none to classlist of element
const hide = (el) => {
  el.classList.add("hidden");
};

// function to show the element
const show = (element) => {
  element.classList.remove("hidden");
};

// hide max,min and interval sizing
hide(max_shoes);
hide(min_shoes);
hide(interval);
hide(submit_stock_details);

// add event listener to enable the systems of numbering
stock_type.addEventListener("input", function () {
  if (stock_type.value == "Alphabetic") {
    hide(max_shoes);
    hide(min_shoes);
    hide(interval);
    show(clothes);
  } else if (stock_type.value == "Continuous") {
    hide(clothes);
    hide(interval);
    show(max_size);
    show(min_size);
  } else if (stock_type.value == "intervaled") {
    hide(clothes);
    show(max_size);
    show(min_size);
    show(interval);
  } else if (stock_type.value == "Random") {
  }
  // clothes.classList.toggle("hidden");
  // max_shoes.classList.toggle("hidden");
  // min_shoes.classList.toggle("hidden");
  // max_shoes.classList.toggle("inline");
  // min_shoes.classList.toggle("inline");
});

next_stock_details.addEventListener("click", function (e) {
  // colour.classList.add("hidden");
  // // colour.classList.remove("add_sale");
  // submit_stock_details.classList.remove("hidden");
  e.preventDefault();

  // create object to store the product variation
  let stock_json = {};

  // get colours available and their number
  const colours = Colour_list.getElementsByTagName("input");
  const len = colours.length;

  // create table to allow use input for the product variation
  let variation_template = `<table> <tr><th>Size</th>`;

  // create table head columns for the colors
  for (const el of colours) {
    // verify that colour inputs is not empty
    if (el.value == "") {
      alert_msg.innerHTML = "Colour cannot be null";
      alert_msg.classList.add("error");
      show(alert_msg);
      setTimeout(() => {
        hide(alert_msg);
      }, 5000);
      return;
    }
    variation_template += `<th> ${el.value.toLowerCase()}</th>`;
  }
  console.log("colours");
  variation_template += `<th>Total</th></tr>`;

  // Alphabetic system of numbering
  if (stock_type.value == "Alphabetic") {
    // get checked checkboxes
    const list_items = clothes.querySelectorAll("input");
    let sizes = [];
    list_items.forEach((element) => {
      if (element.checked) {
        sizes.push(element.value);
      }
    });

    //create row for each size
    for (let size of sizes) {
      // Add row for the colour
      variation_template += `<tr> <td>${size}</td>`;

      // create input fields for the number of shoes in a colour and size
      for (let k = 0; k < len; k++) {
        variation_template += `<td> <input type="number" value="0"> </td>`;
      }

      // create totaling button for the row
      variation_template += `<td> <input type="number" disabled value="0">  </td>
      <td>  <input type="button" class="summation" value="Done">  </td> </tr>`;
    }

    // create final row for totaling
    variation_template += `<tr> <td>Total</td>`;

    // totalling columns for each colour
    for (let k = 0; k < len; k++) {
      variation_template += `<td> <input type="number" disabled value="0"> </td>`;
    }

    // create cell for total of all shoes
    variation_template += `<td> <input type="number" disabled value="0">  </td>
    <td>  <input type="button" class="summation" value="Done">  </td> </tr>`;
  }

  //Continuos numbering system
  else if (stock_type.value == "Continuous") {
    const max_size = +max_shoes.value;
    let min_size = +min_shoes.value;

    console.log(max_size, min_size);
    if (min_size > max_size) {
      alert_msg.innerHTML = "mimimum size cannot be greater than maximum size";
      alert_msg.classList.add("error");
      show(alert_msg);
      setTimeout(function () {
        hide(alert_msg);
      }, 6000);
      return;
    }

    let variation = max_size - min_size + 1;

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
  } else if (stock_type.value == "intervaled") {
    if (min_size > max_size) {
      // pass error to user TODO
    }
  } else if (stock_type.value == "Random") {
  }

  // close the table and append it to the page
  variation_template += `</table>`;
  colour.insertAdjacentHTML("afterend", variation_template);
  // hide colour and submit stock
  colour.classList.add("hidden");
  // colour.classList.remove("add_sale");
  submit_stock_details.classList.remove("hidden");
  // get no of sizes available for the product
  next_stock_details.classList.add("hidden");
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
          console.log(r);
          let sum = 0;
          console.log(siblings[0].innerHTML);
          if (r == colours.length) {
            for (let rs = 0; rs < colours.length; rs++) {
              sum += +siblings[rs + 1].getElementsByTagName("input")[0].value;
              console.log(sum);
            }
            siblings[r + 1].getElementsByTagName("input")[0].value = sum;
            stock_data.value = JSON.stringify(stock_json);
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

  Colour_list.insertAdjacentHTML(
    "beforeend",
    `<li>
  <label for="${label}">Colour</label>
  <input id="${label}" name="${label}" type="text" placeholder="Colour">
  </li>`
  );
  count++;
});
