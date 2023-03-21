$(document).ready(function() {
    var sortByVibe = false;
    var cards = $('.card');
    var disabled = false;
    if ($("#cards").length) {
        $.get('/daycard/get-cards/', 
              {'sortmode': sortByVibe},
              function(data) {
                  $('#cards').html(data);
                  cards = $('.card');
              })
    }
    else {
        $.get('/daycard/get-card-history/', 
              function(data) {
                  $('#cardhistory').html(data);
                  cards = $('.card');
              })
    }
    $(document).click(function(e) {
        console.log(e.target);
        if (!$(e.target).is('button')) {
            if ($(e.target).hasClass("sort-btn") && !disabled) {
                sortByVibe = !sortByVibe;
                $.get('/daycard/get-cards/', 
                      {'sortmode': sortByVibe},
                      function(data) {
                          disabled = true;
                          $('#cards').html(data);
                          $(e.target).addClass("hide");
                          cards = $('.card');
                          setTimeout(function() { 
                              disabled = false;
                              $(e.target).removeClass('hide');
                          }, 1000);
                      })
            }
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