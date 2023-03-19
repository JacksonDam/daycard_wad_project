$(document).ready(function() { 
	$(document).on("click", "button[btntype='like-btn']", function() {
		var postname;
		postname = $(this).attr('data-username');
		var btn = $(this);
		$.get('/daycard/like/', 
		      {'username': postname},
		      function(data) {
		      	  if (data !== "-1") {
		      	  	  btn.toggleClass("active");
		      	  }
		      	  btn.text("👍 " + data);
		      })
    });
});