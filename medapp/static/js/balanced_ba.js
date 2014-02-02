
//*************************************************
//**** Adding a Bank Account Functionality ********
//*************************************************

var balanced_BA_submittable = true //Toggles if form is submittable
$(document).ready(function() {	
    balanced.init(marketplaceUri);
    Balanced_BA_Enable();
	$('#ba-submit').click(function (e) { 
		e.preventDefault();
		if (balanced_BA_submittable){
			Balanced_BA_Disable();
			var payload = {
				name: $('#ba-name').val(),
				account_number: $('#ba-number').val(),
				routing_number: $('#ba-routing').val()
			};

			// Tokenize bank account
			balanced.bankAccount.create(payload, function (response) {
				console.log(response);
				switch (response.status) {
				 case 201:
				 	if (response.data.is_valid == 'true') {
						$.post(responseTarget_ba, {
							name: response.data.name,
							bank_code: response.data.bank_code,
							account_number:response.data.account_number,
							bank_name: response.data.bank_name,
							fingerprint: response.data.fingerprint,
							uri: response.data.uri
						}, function (r) {
							if (r['status'] == 201) {
								window.location.href = success_redirect_ba
							} else {
								display_BA_Error('Error saving your Card. '+r['error']);
								Balanced_BA_Enable();
							}
						}).fail( function(xhr, textStatus, errorThrown) {
							 display_BA_Error("We experienced a problem with our servers. We will fix the problem shortly");
							 Balanced_BA_Enable();
						});
					} else {
						display_BA_Error("Failed to authorize your bank account. Please double check your name, account and routing number");
					 	Balanced_BA_Enable();
					}
					break;
				 case 400:
					 // Missing Field, display appropriate error message
					 display_BA_Error("Failed to authorize your bank account. Please double check your name, account and routing number");
					 Balanced_BA_Enable();
					 break;
				 case 402:
					 //Failed to tokenize card
					 display_BA_Error("Failed to authorize your bank account. Please double check your account and routing number");
					 Balanced_BA_Enable();
					 break;
				 case 404:
					 // Your marketplace URI is incorrect
					 display_BA_Error("We are having technical hiccups with our marketplace URI");
					 Balanced_BA_Enable();
					 break;
				 case 500:
					 // Balanced did something bad, please retry the request
					 Balanced_BA_Enable();
					 break;
				 }
			});
		}
	});
	$('#populate').click(function () {
        $('#ba-name').val('John Hancock');
        $('#ba-routing').val('021000021');
        $('#ba-number').val('9900000004');
    });
});

function display_BA_Error(error) {
	$(".ba-error").text(error);
	$('.ba-error').css('display','block');
}
function Balanced_BA_Disable() {
	balanced_BA_submittable = false;
	$("#ba-submit span").text("Processing. . .");
	$("#ba-submit img").css('display','inline-block');
	if (!($("#ba-submit").hasClass("disabled"))) {
		$("#ba-submit").addClass("disabled");
	}
}
function Balanced_BA_Enable() {
	balanced_BA_submittable = true;
	$("#ba-submit span").text(balanced_ba_button_text);
	$("#ba-submit img").css('display','none');
	$("#ba-submit").removeClass("disabled");
}