$(document).ready(function() {
    console.log("READY");
    const cards = $('.card');
    cards.each(function(i, obj) {
       obj.addEventListener("click", function() {
           console.log("FLIP");
           cards.toggleClass("active");
       });
    });
});