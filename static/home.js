"use strict";

const avail_data = document.querySelectorAll("button");

avail_data.forEach((btn) => {
  //   btn.nextElementSibling.classList.add("hidden");
  btn.addEventListener("click", function () {
    console.log("hide");
    btn.nextElementSibling.classList.toggle("hidden");
    btn.nextElementSibling.classList.toggle("par-availdata");
  });
  console.log(btn.nextElementSibling);
});
