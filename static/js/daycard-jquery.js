$(document).ready(function() {
    const cards = $('.card');
    $(document).click(function(e) {
        if (!$(e.target).is('button')) {
            if (!$(".card").is(e.target) && !$(".card").has(e.target).length) {
                cards.each(function(i, obj) {
                    $(obj).toggleClass("active", false);
                    $(obj).stop(true, true).fadeTo(200, 1);
                });
            }
            else {
                const obj = e.target.closest(".card");
                $(obj).toggleClass("active");
                $(obj).fadeTo(200, 1);
                var otherCards = cards.not(obj);
                var thisCardActive = $(obj).hasClass("active");
                console.log(thisCardActive);
                if (thisCardActive) {
                    otherCards.each(function(j, obj2) {
                        $(this).toggleClass("active", false);
                        $(this).stop(true, true).fadeTo(200, 0.5);
                    });
                }
                else {
                    otherCards.each(function(k, obj3) {
                        $(this).toggleClass("active", false);
                        $(this).stop(true, true).fadeTo(200, 1);
                    });
                }
            };
        };
    });
});