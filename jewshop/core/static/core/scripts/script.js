var multipleCardCarousel = document.querySelector(
  "#carouselExampleControls"
);
var carousel = new bootstrap.Carousel(multipleCardCarousel, {
interval: false,
});
var carouselWidth = $(".carousel-inner")[0].scrollWidth;
var cardWidth = $(".carousel-item").width();
var scrollPosition = 0;
$("#carouselExampleControls .carousel-control-next").on("click", function () {
  scrollPosition += cardWidth;
  $("#carouselExampleControls .carousel-inner").animate(
    { scrollLeft: scrollPosition },
    600
  );
});
$("#carouselExampleControls .carousel-control-prev").on("click", function () {
if (scrollPosition > 0) {
  scrollPosition -= cardWidth;
  $("#carouselExampleControls .carousel-inner").animate(
    { scrollLeft: scrollPosition },
    600
  );
}
});