$(document).ready(function() { 
	var waiting = false;
	$(document).on("click", "button[btntype='post-daycard-btn']", function() {
		if (!waiting) {
			waiting = true;
			var wordOne;
			wordOne = $("input[fieldnumber='1']").val();
			var wordTwo;
			wordTwo = $("input[fieldnumber='2']").val();
			var wordThree;
			wordThree = $("input[fieldnumber='3']").val();		
			var caption;
			caption = $("#daycardcaptionfield").val();
			var colour;
			colour = $('#preview1').attr("data-colour");
			$.get('/daycard/post-new-daycard/', 
			      {'wordOne': wordOne, 'wordTwo': wordTwo, 'wordThree': wordThree, 'colour': colour, 'caption': caption},
			      function(data) {
			      	  if (data === 'SUCCESS') {
			      	  	  $('#post-container').fadeOut('normal');
			      	  	  setTimeout(function() {	
			      	  	  	  window.location.href = $('#temp-home').attr('href');
			      	  	  }, 1000);
			      	  }
			      })
		};
    });
});