$(document).ready(function() { 
	var input = document.getElementById("querybox");

	input.addEventListener("keydown", function(event) {
		var text = encodeURI($('input:text').val()); 
		$.get('/daycard/results/', 
		      {'query': text},
		      function(data) {
		      	  $('#resultsbox').html(data)
		      })
	});
});