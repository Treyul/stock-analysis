"use strict";

const colours = document.getElementById("addColours");
const type = document.getElementById("stock_type");
const fields = document.querySelectorAll(".form");
const next_stock_details = document.getElementById("add_stock_next");
const list = document.getElementById("colours");
const form = document.getElementById("form_add_stock");
const clothes = fields[2];
const max_shoes = fields[3];
const min_shoes = fields[4];

const hide = (el) => {
  el.classList.add("hidden");
};
hide(max_shoes);
hide(min_shoes);
hide(fields[7]);

type.addEventListener("input", function () {
  clothes.classList.toggle("hidden");
  max_shoes.classList.toggle("hidden");
  min_shoes.classList.toggle("hidden");
});

next_stock_details.addEventListener("click", function (e) {
  e.preventDefault();
  let stock_json = {};
  const max_size = +document.getElementById("max_size").value;
  let min_size = +document.getElementById("min_size").value;

  // console.log(max_size, min_size);

  let variation = max_size - min_size + 1;

  const colours = list.getElementsByTagName("input");
  const len = colours.length;

  console.log(len, variation);

  let variation_template = `<table> <tr><th>Size</th>`;
  for (const el of colours) {
    variation_template += `<th> ${el.value}</th>`;
  }
  variation_template += `<th>Total</th></tr>`;
  for (min_size; min_size <= max_size + 1; min_size++) {
    if (min_size == max_size + 1) {
      variation_template += `<tr><td>Total</td>`;
      0;
    } else {
      variation_template += `<tr><td> ${min_size}</td>`;
    }

    for (let k = 0; k < len; k++) {
      variation_template += `<td><input type="number" value="0"></td>`;
    }
    variation_template += `<td><input type="number" value="0"></td><td>
    <input type="button" class="summation" value="Done"></td></tr>`;
  }

  variation_template += `</table>`;
  fields[fields.length - 1].insertAdjacentHTML("afterend", variation_template);

  const summation_buttons = document.querySelectorAll(".summation");
  console.log(summation_buttons);

  summation_buttons.forEach((element) => {
    element.addEventListener("click", function () {
      const parent = element.closest("tr");
      const siblings = parent.getElementsByTagName("td");
      if (siblings[0].innerHTML == "Total") {
        for (let r = 0; r <= colours.length; r++) {
          console.log(r, r == colours.length);
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
            for (const [key, val] of Object.entries(stock_json)) {
              sum += +val[`${colours[r].value}`];
            }
            siblings[r + 1].getElementsByTagName("input")[0].value = sum;
          }
        }
        console.log("done");
      } else {
        let sum = 0;
        let size = {};
        for (let i = 1; i < siblings.length - 2; i++) {
          size[`${colours[i - 1].value}`] =
            +siblings[i].getElementsByTagName("input")[0].value;
          sum += +siblings[i].getElementsByTagName("input")[0].value;
        }
        console.log(size);

        siblings[siblings.length - 2].getElementsByTagName("input")[0].value =
          sum;

        stock_json[`${siblings[0].innerHTML}`] = size;
        // console.log(typeof siblings[0].innerHTML);
        console.log(stock_json);
      }
    });
  });
});

let count = 1;
colours.addEventListener("click", function (e) {
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
