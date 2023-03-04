$(document).ready(function() { 
	$("input").on('input', function() {
		var text = encodeURI($('input:text').val()); 
		$.get('/daycard/results/', 
		      {'query': text},
		      function(data) {
		      	  $('#resultsbox').html(data);
		      })
	});
});