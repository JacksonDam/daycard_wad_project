$(document).ready(function() { 
	var input = document.getElementById("querybox");

	input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            document.getElementById("searchbtn").click();
	    }
	});

	$('#searchbtn').click(function() {
		var url = $("#url").attr("data-url");
		var text = encodeURI($('input:text').val()); 
		if (text.length > 0) {
			location.href = url + "?query=" + text
		}
		else {
			location.href = url
		}
		console.log("AAAA");
	});
});