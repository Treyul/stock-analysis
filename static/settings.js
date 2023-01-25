const menu_links = document.querySelectorAll(".links");
const contents = document.querySelectorAll(".contents");

menu_links.forEach((element) => {
  element.addEventListener("click", function () {
    console.log(element.dataset.tab);
    const tab = element.dataset.tab;

    contents.forEach((el) => {
      el.classList.remove("contents--active");
    });

    const display = document.querySelector(`.content-0${tab}`);
    console.log(display);

    display.classList.add("contents--active");
  });
});
