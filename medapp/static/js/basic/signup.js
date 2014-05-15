/*************************************************/
/* Custom Built Form Validator For All Forms *****/
/*************************************************/
/* Built by Mitchell Kates */

// var states = ['Alaska', 'Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'Washington D.C.', 'West Virginia', 'Wisconsin', 'Wyoming'];

$.fn.formValidator = function() {
	$(this).find("input").blur(function() {
		validateInput($(this),'blur');
	});
	$(this).find("input").keyup(function() {
		validateInput($(this),'keyup');
	});
	$(this).find("input[type='checkbox']").change(function() {
		validateInput($(this),'check');
	});
	$(this).submit(function() {
		all_valid = checkAllInputs($(this));
		if (all_valid) {
			return true;
		} else {
			$(this).find(".form-error").css("display","block");
			return false;
		}
	});

	var validateInput = function(input,action) {
		var data_type = $(input).attr("data-type");
		var required = $(input).attr('data-required') == 'true' ? true : false;
		if (data_type == 'text') {
			var valid = $(input).val().length >= 2;
		} else if (data_type == 'email') {
			var valid = checkEmail($(input));
		} else if (data_type == 'password') {
			var valid = $(input).val().length > 5 ;
		} else if (data_type == 'confirmpassword') {
			var original_password = $(input).closest('form').find("input.password");
			var valid = ($(original_password).val() == $(input).val());
		} else if (data_type == 'promocode') {
			var valid = checkPromoCode($(input));
		}  else if (data_type == 'phonenumber') {
			var valid = $(input).val().length >= 10;
		} else if (data_type == 'checkbox') {
			var valid = $(input).is(":checked");
		}
		valid ? updateCSS(input,true,required,action) : updateCSS(input,false,required,action);
		return (valid || !(required));
	}

	var updateCSS = function(input,valid,required,action) {
		var parent = $(input).parent();
		var helper_text = $(parent).find(".error");
		var success_text = $(parent).find(".success");
		var glyphicon_div = $(parent).children('.status');
		var activated = ($(glyphicon_div).children('span.glyphicon-ok').is(":visible") || $(glyphicon_div).children('span.glyphicon-remove').is(":visible"));
		var only_good = (!(activated) && action =='keyup');
		if (valid) {
			$(glyphicon_div).children('span.glyphicon-ok').css('display','block');
			$(glyphicon_div).children('span.glyphicon-remove').css('display','none');
			$(helper_text).css('display','none');
			$(success_text).css('display','block');
			$(input).removeClass('has-error');
		} else if (!(valid) && !(required)) { // Not a valid input but not a required field
			console.log("onvsafsa");
			$(glyphicon_div).children('span.glyphicon-ok').css('display','none');
			$(success_text).css('display','none');
		} else if (!(valid) && !(only_good)) { // Not valid and it has been activated as a field (used so x doesnt appear before a blur event)
			if (!($(input).addClass('has-error'))) {
				$(input).addClass('has-error');
			};
			$(glyphicon_div).children('span.glyphicon-ok').css('display','none');
			$(glyphicon_div).children('span.glyphicon-remove').css('display','block');
			$(helper_text).css('display','block');
			$(success_text).css('display','none');
		}
		//For required checkboxes
		if (action=="check" && !(valid) && required) {
			parent.css('color','red');
			parent.children('a').css('color','red');
		} else if (action=="check" && valid && required){
			parent.css('color','#333');
			parent.children('a').css('color','#009CC3');
		}
	}


	var isEmail = function(email) {
		var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
	 	return emailReg.test(email);
	}

	var checkEmail = function(input) {
		var email = $(input).val();
		var validemail = (isEmail(email) && email.length >0);
		if (!(validemail)) {
			$(input).parent().find('.error').text("Invalid Email");
			return false;
		}
		$.ajax({
			type : "GET",
			data : {'email':email},
			url : "/checkemail",
			success : function(data) {
				if (data == 'valid') {
					updateCSS(input,true,true,'email-check')
				} else {
					$(input).parent().find('.error').text("Email Already In Use. Sign In Instead");
					updateCSS(input,false,true,'email-check')
				}
			}
		});
		return true;
	}

	var checkPromoCode = function(input) {
		var promo = $(input).val();
		$.ajax({
			type : "GET",
			data : {'promo':promo},
			url : "/checkpromo",
			success : function(data) {
				if (data['status'] == 201) {
					$(input).parent().find('.success').text(data['text']);
					updateCSS(input,true,false,'promo-check')
				} else {
					$(input).parent().find('.success').text("");
					updateCSS(input,false,false,'promo-check')
				}
			}
		});
	}

	var checkAllInputs = function(element) {
		inputs = $(element).find("input");
		all_valid = true
		$.each(inputs,function(index,value) {
			valid = validateInput($(value),'submit');
			if (!(valid)) {
				all_valid = false;
			}
		});
		return all_valid;
	}
} 



$(document).ready(function() {
	var form_id = $("#signupform").formValidator();
});

