const menu_links = document.querySelectorAll(".links");
const contents = document.querySelectorAll(".contents");
const change_prices = document.querySelectorAll(".prices");
var saledata = {};

// enalbe toggling between menu settings
menu_links.forEach((element) => {
  // add event listeners to menu items
  element.addEventListener("click", function () {
    const tab = element.dataset.tab;

    //make menu items invisible
    contents.forEach((el) => {
      el.classList.remove("contents--active");
    });

    // get element to display
    const display = document.querySelector(`.content-0${tab}`);
    display.classList.add("contents--active");
  });
});

//
change_prices.forEach((element) => {
  // add event listener to each price button
  element.addEventListener("click", function () {
    // prompt user
    const new_price = prompt("Enter new price");

    // cancel ops if user cancels
    if (new_price == null) return;
    // get parent div element
    const container = element.closest("div");
    // get roduct name
    const product_name = container.querySelector(".start");

    let response = fetch("/setprice", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        product: `${product_name.innerHTML}`,
        price: +new_price,
      }),
    }).then(function (response) {
      if (response.status != 200) console.log("ERROR");

      response.json().then(function (data) {
        console.log(data);
      });
    });
  });
});
