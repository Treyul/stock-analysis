const menu_links = document.querySelectorAll(".links");
const contents = document.querySelectorAll(".contents");
const change_prices = document.querySelectorAll(".prices");

// get the cookie in the website
const cookies = document.cookie;

// create a cookie array
const cookie_array = cookies.split("=");

// get index of the crsf key word
const crsf_key = cookie_array.indexOf("csrftoken");
const crsf_token = cookie_array[crsf_key + 1];
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
    console.log(element);
    // prompt user
    const new_price = prompt("Enter new price");

    // cancel ops if user cancels
    if (new_price == null) return;
    // get parent div element
    const container = element.closest("tr");
    // get roduct name
    const product_name = container.querySelector(".start");
    console.log(product_name.innerHTML);

    let response = fetch("/settings/setprice", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "X-CSRFToken": `${crsf_token}`,
      },
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
