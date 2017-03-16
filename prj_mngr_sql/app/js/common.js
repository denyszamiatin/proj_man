$( document ).ready(function() {


    $( ".user_login div" ).on( "click", function() {
	  $(".user_login").css('display', 'none')
	  $(".user_registration").css('display', 'block')
	});

	 $( ".user_registration div" ).on( "click", function() {
	  $(".user_registration").css('display', 'none')
	  $(".user_login").css('display', 'block')
	});

});