$(document).ready(function() { 
	var disabled = false;
	var confirm_count = 3;
	$(document).on("click", "button[btntype='delete-btn']", function() {
		if (!disabled) {
			if (confirm_count == 0) {
				confirm_count = 3;
				var btn = $(this);
				disabled = true;
				$.get('/daycard/delete-daycard/', 
				      function(data) {
				      	  btn.text(data);
				      	  $(btn).addClass('hide');
				      })
			    setTimeout(function() {	
			    	disabled = false;
	  	  	  	    $(btn).text("Delete today's DayCard");
	  	  	  	    $(btn).removeClass('hide');
	  	  	    }, 1000);
			}
			else {
				var btntxt = "Click " + confirm_count;
				if (confirm_count == 1) {
					btntxt += " time to confirm";
				}
				else {
					btntxt += " times to confirm";
				}
				$(this).text(btntxt);
				confirm_count--;
			}
		}
    });
});