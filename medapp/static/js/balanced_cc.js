//*************************************************
//**** Adding a Credit Card Functionality *********
//*************************************************

//Hover functionality for the security code (?)
$(document).ready(function () {
	$( "#cvv-info").hover(function() {
		$('#imageoverlay').css('display','block');
		}, function() {
			$('#imageoverlay').css('display','none');
		}
	);
});


//Submitting a Credit Card
//Needs the global variables responsetarget,success_redirect,marketplaceuri, and balanced_cc_button_text
var balanced_cc_submitable = true //Toggles if form is submittable
$(document).ready(function () {
    balanced.init(marketplaceUri);
    $('#cc-submit').click(function (e) {
        e.preventDefault();
		if (balanced_cc_submitable){
			bd = Balanced_CC_Disable();
			//Create Payload
        	var payload = {
				card_number: $('#cc-number').val(),
				expiration_month: $('#cc-ex-month').val(),
				expiration_year: $('#cc-ex-year').val(),
				security_code: $('#cc-csc').val(),
				postal_code: $('#cc-zipcode').val()
        	};
        
        	// Tokenize credit card
        	balanced.card.create(payload, function (response) {
            switch (response.status) {
			 case 201:
			 	if (response.data.postal_code_check == "passed" || response.data.security_code_check == "passed") {
					$.post(responseTarget_cc, {
						brand: response.data.brand,
						hash: response.data.hash,
						expiration_month: response.data.expiration_month,
						expiration_year: response.data.expiration_year,
						last_four: response.data.last_four,
						uri: response.data.uri
					}, function(r) {
						if (r['status'] == 201) {
							window.location.href = success_redirect_cc;
						} else {
							display_CC_Error('Error saving your Card. '+r['error']);
							Balanced_CC_Enable();
						}
					});
				} else {
					display_CC_Error("We failed to verify your card. Please double check your information and try again");
					Balanced_CC_Enable();
				}
				break;
			 case 400:
				 // Missing Field, display appropriate error message
				 error_message = "";
				 //Comma formatting for error text
				 comma = false;
				 $.each(response.error, function(index,value) {;
				 	if (comma) {
				 		error_message =error_message+", "+value
				 	} else {
				 		comma = true;
				 		error_message = error_message + value
				 	}
				 });
				 display_CC_Error(error_message);
				 Balanced_CC_Enable();
			 case 402:
			 	 //Failed to tokenize card
				 display_CC_Error("Failed to authorize your credit card");
				 Balanced_CC_Enable();
				 break;
			 case 404:
				 // Your marketplace URI is incorrect
				 display_CC_Error("We are having technical hiccups with our marketplace URI");
				 Balanced_CC_Enable();
				 break;
			 case 500:
				 // Balanced did something bad, please retry the request
				 Balanced_CC_Enable();
				 break;
		     }
           
        }); 
    	} //End of balanced_cc_submitable if statement
    });
    
    
    ////
    // Simply populates credit card and bank account fields with test data
    ////
    $('.populate').click(function () {
        $('#cc-number').val('4111111111111111');
        $('#cc-ex-month').val('12');
        $('#cc-ex-year').val('2020');
        $('#cc-csc').val('123');
        $('#cc-zipcode').val('00000');
        $('#ba-name').val('John Hancock');
        $('#ba-number').val('9900000000');
        $('#ba-routing').val('321174851');
    });
});
function Balanced_CC_Disable() {
	balanced_cc_submitable = false;
	$("#cc-submit span").text("Processing. . .");
	$("#cc-submit img").css('display','inline-block');
	if (!($("#cc-submit").hasClass("disabled"))) {
		$("#cc-submit").addClass("disabled");
	}
}
function Balanced_CC_Enable() {
	balanced_cc_submitable = true;
	$("#cc-submit span").text(balanced_cc_button_text);
	$("#cc-submit img").css('display','none');
	$("#cc-submit").removeClass("disabled");
}
function display_CC_Error(error) {
	$(".cc-error").text(error);
	$('.cc-error').css('display','block');
}