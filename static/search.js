const submit = document.getElementById("submit");

submit.addEventListener("click", function (e) {
  e.preventDefault();
  console.log("print");

  //   get value of the input fields
  const product = document.getElementById("product");
  const shop = document.getElementById("name");
  const size = document.getElementById("size");
  const colours = document.getElementById("colour");

  // console.log({ 23: "tree", test: "two" });
  let test = {};
  test[3] = 17;
  // test["tet"] = "44";
  console.log(test[3]);
  // initialize JSON object
  search_object = {};

  // tets value of the input fields
  if (product.value.trim() != "") {
    // search_object["product"] =
  }
  if (shop.value.trim() != "") {
  }
  if (size.value.trim() != "") {
  }
  if (colours.value.trim() != "") {
  }
  //   let response = fetch("/search", {
  //     method: "POST",
  //     headers: { "content-type": "application/json" },
  //     body: JSON.stringify(saledata),
  //   }).then(function (response) {
  //     if (response.status != 200) {
  //       console.log("ERROR");
  //     }

  //     response.json.then(function (data) {
  //       console.log(data);
  //     });
  //   });
});
