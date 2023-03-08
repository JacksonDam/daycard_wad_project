$(document).ready(function() {
    const cards = $('.card');
    cards.each(function(i, obj) {
        obj.addEventListener("click", function() {
            $(obj).toggleClass("active");
            $(this).fadeTo(200, 1);
            var otherCards = cards.not(this);
            otherCards.each(function(j, obj2) {
                $(this).toggleClass("active", false);
                $(this).fadeTo(200, 0.5);
            });
       });
    });
    $(document).click(function(e) {
        console.log(e.target);
        if (!$( ".card" ).is(e.target) && !$( ".card" ).has(e.target).length) {
            cards.each(function(i, obj) {
                $(obj).toggleClass("active", false);
                $(obj).fadeTo(200, 1);
            });
        }
        else {
            console.log(e.target);
        };
    });
});