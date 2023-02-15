const submit = document.getElementById("submit");

submit.addEventListener("click", function (e) {
  e.preventDefault();
  console.log("print");

  //   get value of the input fields
  const product = document.getElementById("product");
  const shop = document.getElementById("name");
  const size = document.getElementById("size");
  const colours = document.getElementById("colour");

  // initialize JSON object
  search_object = {};

  // tets value of the input fields
  if (product.value.trim() != "") {
    search_object["product"] = product.value.trim().split(" ")[0];
  }
  if (shop.value.trim() != "") {
    search_object["shop_no"] = shop.value.trim().split(" ")[0];
  }
  if (size.value.trim() != "") {
    search_object["size"] = size.value.trim().split(" ")[0];
  }
  if (colours.value.trim() != "") {
    search_object["colour"] = colours.value.trim().split(" ")[0];
  }
  console.log(search_object);

  let response = fetch("/search", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(search_object),
  }).then(function (response) {
    if (response.status != 200) {
      console.log("ERROR");
    }

    response.json().then(function (data) {
      console.log(data);
    });
  });
});
