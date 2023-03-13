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

// add toggling of submenus
drop_down_submenus.forEach((Element) => {
  Element.addEventListener("click", function () {
    // get the submenus
    const submenus = Element.nextElementSibling;

    submenus.classList.toggle("hidden");
  });
});
