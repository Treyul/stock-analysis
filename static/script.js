"use strict";

// const colour = document.getElementById("addColours");
const stock_type = document.getElementById("id_stock_type");
const clothes = document.getElementById("id_clothing");
// select elements that specify sizing
const max_size = document.getElementById("id_max_size");
const min_size = document.getElementById("id_min_size");
const interval = document.getElementById("id_interval");
const random = document.getElementById("id_random");
// select colours
const addButton = document.getElementById("add-item");
const removeButton = document.getElementById("remove-item");
// const Colour_list = document.getElementById("id_colours");
const form = document.getElementById("form_add_stock");
const submit = document.getElementById("stock_det");
const next_stock_details = document.getElementById("add_stock_next");
const submit_stock_details = document.getElementById("add_stock");
const stock_data = document.getElementById("id_stock_data");
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

// function to hide the alphabetic sizing
const hide_clothes = (clothing) => {
  clothing.classList.remove("clothing");
  hide(clothing);
};
const show_clothes = (clothing) => {
  clothing.classList.add("clothing");
  show(clothing);
};

// hide max,min, random and interval sizing when initializing document
hide(max_size);
hide(min_size);
hide(interval);
hide(submit_stock_details);
hide(random);
show_clothes(clothes);

// add event listener to enable the systems of numbering
stock_type.addEventListener("input", function () {
  if (stock_type.value == "Alphabetic") {
    hide(max_size);
    hide(min_size);
    hide(interval);
    show_clothes(clothes);
  } else if (stock_type.value == "Continuous") {
    hide_clothes(clothes);
    hide(interval);
    show(max_size);
    show(min_size);

    // verify data submitted is correct
  } else if (stock_type.value == "intervaled") {
    hide_clothes(clothes);
    show(max_size);
    show(min_size);
    show(interval);
  } else if (stock_type.value == "Random") {
  }
});

/****************** COLOUR LIST *********************/
// Add colours
// get the number of colours
var items = 2;

// add eventlister to add colour button
addButton.addEventListener("click", () => {
  // create colour input element and set its attributes
  const item = document.createElement("input");
  item.type = "text";
  item.name = `Colour ${items}`;
  item.id = `id_Colour ${items}`;
  item.required = true;

  // create the inputs lable and set its attributes
  const label = document.createElement("label");
  label.innerHTML = `Colour ${items}: `;
  label.setAttribute("for", `id_Colour ${items}`);

  //select container to add the label and input field
  const container = document.querySelector("form");
  container.insertBefore(label, removeButton);
  container.insertBefore(item, removeButton);
  items++;
  document.querySelector("#id_num_items").value = items;
});

/*************  remove colours  ****************/
// Add event listener to rthe remove colour button
removeButton.addEventListener("click", () => {
  // get the array of colours inputs and labels
  const colours = document.querySelectorAll("input[id^='id_Colour']");
  const colour_labels = document.querySelectorAll("label[for^='id_Colour']");
  console.log(colour_labels, colours);

  // show error message if length is less than 1
  if (colours.length <= 1) {
    alert_msg.innerHTML = "Colours cannot be less than 1";
    alert_msg.classList.add("error");
    show(alert_msg);
    setTimeout(() => {
      hide(alert_msg);
      alert_msg.classList.remove("error");
      console.log("this");
    }, 5000);
  } else {
    // delete the elements from the array
    // console.log(colour_labels);
    colours[colours.length - 1].remove();
    colour_labels[colour_labels.length - 1].remove();
    // console.log(colour_labels);
    items--;
    document.querySelector("#id_num_items").value = items;
  }
});

next_stock_details.addEventListener("click", function (e) {
  e.preventDefault();

  // create object to store the product variation
  let stock_json = {};

  // get colours available and their number
  const colours = document.querySelectorAll("input[id^='id_Colour']");
  const form_colour = document.getElementById("id_colour");
  var colour_array = [];
  console.log(colours);
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
        alert_msg.classList.remove("error");
        hide(alert_msg);
      }, 5000);
      return;
    }
    variation_template += `<th> ${el.value.toLowerCase()}</th>`;
    colour_array.push(el.value.toLowerCase());
  }

  // append the colour data to its field
  form_colour.value = JSON.stringify(colour_array);

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
    const max_size_value = +max_size.value;
    let min_size_value = +min_size.value;

    console.log(max_size_value, min_size_value);
    if (min_size_value > max_size_value) {
      alert_msg.innerHTML = "mimimum size cannot be greater than maximum size";
      alert_msg.classList.add("error");
      show(alert_msg);
      setTimeout(function () {
        alert_msg.classList.remove("error");
        hide(alert_msg);
      }, 6000);
      return;
    }

    let variation = max_size_value - min_size_value + 1;

    // create table ros for the sizes
    for (
      min_size_value;
      min_size_value <= max_size_value + 1;
      min_size_value++
    ) {
      // create final tallying row
      if (min_size_value == max_size_value + 1) {
        variation_template += `<tr><td>Total</td>`;
      } else {
        // size row
        variation_template += `<tr><td>${min_size_value}</td>`;
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
  colours[colours.length - 1].insertAdjacentHTML(
    "afterend",
    variation_template
  );
  // hide colour and submit stock
  // colours.classList.add("hidden");
  // colour.classList.remove("add_sale");
  submit_stock_details.classList.remove("hidden");
  hide(addButton);
  hide(removeButton);
  // get no of sizes available for the product
  next_stock_details.classList.add("hidden");
  // get all totalling button s and add functionality
  const summation_buttons = document.querySelectorAll(".summation");

  summation_buttons.forEach((element) => {
    element.addEventListener("click", function () {
      // get row to be totalled  and columns
      console.log("here");
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
// colour.addEventListener("click", function (e) {
//   e.preventDefault();
//   let label = `colours-${count}`;

//   Colour_list.insertAdjacentHTML(
//     "beforeend",
//     `<li>
//   <label for="${label}">Colour</label>
//   <input id="${label}" name="${label}" type="text" placeholder="Colour">
//   </li>`
//   );
//   count++;
// });
