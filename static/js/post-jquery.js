$(document).ready(function() {
    $("input").keypress(function(e) {
        if (e.which === 32) {
            return false;
        };
    });

    $("#green-btn").click(function() {
        $('.card[type="preview"]').css("background", "linear-gradient(180deg, #70FF6D 0%, #05E700 100%)");
        $("#green-btn").css("border", "10px solid #0066FF");
        $("#amber-btn").css("border", "none");
        $("#red-btn").css("border", "none");
        $('.card[type="preview"]').attr("data-colour", "0");
    }); 

    $("#amber-btn").click(function() {
        $('.card[type="preview"]').css("background", "linear-gradient(180deg, #FFDF6D 0%, #E79800 100%)");
        $("#green-btn").css("border", "none");
        $("#amber-btn").css("border", "10px solid #0066FF");
        $("#red-btn").css("border", "none");
        $('.card[type="preview"]').attr("data-colour", "1");
    }); 

    $("#red-btn").click(function() {
        $('.card[type="preview"]').css("background", "linear-gradient(180deg, #FF6D6D 0%, #E70000 100%)");
        $("#green-btn").css("border", "none");
        $("#amber-btn").css("border", "none");
        $("#red-btn").css("border", "10px solid #0066FF");
        $('.card[type="preview"]').attr("data-colour", "2");
    }); 

    $("textarea").on('input', function() {
        var text = ($('#daycardcaptionfield').val().length); 
        $('#caption-length').text(text.toString() + " / 45");
    });
});