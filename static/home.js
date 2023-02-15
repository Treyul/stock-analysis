"use strict";

const avail_data = document.querySelectorAll("button");
const availablestock = document.getElementById("available");

avail_data.forEach((btn) => {
  //   btn.nextElementSibling.classList.add("hidden");
  btn.addEventListener("click", function () {
    console.log("hide");
    btn.nextElementSibling.classList.toggle("hidden");
    btn.nextElementSibling.classList.toggle("par-availdata");
    if (btn.nextElementSibling.classList.contains("hidden")) {
      btn.innerHTML = "Show";
    } else {
      btn.innerHTML = "Hide";
    }
  });
  console.log(btn.nextElementSibling);
});
