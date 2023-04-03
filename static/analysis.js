// get elements
const current_year_revenue = document.getElementById("current_year_revenue");
const current_year_volume = document.getElementById("current_year_volume");
const show_sale_details = document.querySelectorAll(".retail-show-btn");
const retail_data = document.querySelector(".retail-data");
const retail_table = retail_data.querySelector("table");
const MONTHS = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "June",
  "Jul",
  "Aug",
  "Sept",
  "Oct",
  "Nov",
  "Dec",
];

const QUARTERS = ["Fisrt", "Second", "Third", "Fourth"];
const date = new Date();

const menu_hamburger = document.getElementById("hamburger");
const drop_down_submenus = document.querySelectorAll(".nav-dropdown");

menu_hamburger.addEventListener("click", function () {
  //   select the hamburger items
  const item_one = menu_hamburger.querySelector("#one");
  const item_two = menu_hamburger.querySelector("#two");
  const item_three = menu_hamburger.querySelector("#three");

  //   select the main menu
  const menu = document.getElementById("main-menu");

  //   toggle the class for view and close menu
  menu.classList.toggle("show");
  item_one.classList.toggle("item-one");
  item_two.classList.toggle("item-two");
  item_three.classList.toggle("item-three");
  menu.classList.toggle("menuhidden");
});

// add event listeners to show the sales detailed analysis
show_sale_details.forEach((button) => {
  button.addEventListener("click", function () {
    // select parent element
    const parent_div = button.closest("div");

    // select the container for the details
    const details = parent_div.nextElementSibling;

    details.classList.toggle("hidden");
  });
});
