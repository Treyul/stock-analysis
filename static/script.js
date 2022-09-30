"use strict";

const colours = document.getElementById("addColours");
const type = document.getElementById("stock_type");
const fields = document.querySelectorAll(".form");
const clothes = fields[2];
const max_shoes = fields[3];
const min_shoes = fields[4];

const hide = (el) => {
  el.classList.add("hidden");
};
hide(max_shoes);
hide(min_shoes);

type.addEventListener("input", function () {
  clothes.classList.toggle("hidden");
  max_shoes.classList.toggle("hidden");
  min_shoes.classList.toggle("hidden");
});

let count = 1;
colours.addEventListener("click", function (e) {
  e.preventDefault();
  const list = document.getElementById("colours");
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
