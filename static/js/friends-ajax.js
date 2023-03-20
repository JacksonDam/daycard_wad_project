$(document).ready(function() { 
	$.get('/daycard/results/', 
          {'query': ''},
          function(data) {
      	      $('#resultsbox').html(data);
          })

	$("input").on('input', function() {
		var text = encodeURI($('input:text').val()); 
		$.get('/daycard/results/', 
		      {'query': text},
		      function(data) {
		      	  $('#resultsbox').html(data);
		      })
	});

	$(document).on("click", "button[btntype='friend-btn']", function() {
		var friendname;
		friendname = $(this).attr('data-username');
		var btn = $(this);
		$.get('/daycard/friend-req/', 
		      {'username': friendname},
		      function(data) {
		      	  btn.text(data);
		      })
    });
});