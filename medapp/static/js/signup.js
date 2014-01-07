var formelements = {'businesstype':false,'name':false,'company':true,'email':false,'address_one':false,'address_two':true,'zipcode':false,'city':false,'state':true,'website':true,'phonenumber':false, 'password':false};
var states = ['AK',"AL","AR","AS","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"];

function isEmail(email) {
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  console.log(emailReg.test(email));
  return emailReg.test(email);
}

$(document).ready(function() {
	$(".phonenumber").mask("(999) 999-9999");
	$("input").blur(function() {
		validateinput($(this),false);
	});
	$("input").keyup(function() {
		validateinput($(this),false);
	});
	$("select").change(function() {
		validateinput($(this),false);
	});
	//Populate the state field
	for (var i=0; i < states.length; i++) {
		$("#state").append("<option>"+states[i]+"</option>");
	}
	//Hide certain elements
	$("#businesstype").change(function() {
		$(this).val() != 'none' ? $(".companyextra").fadeIn() : $(".companyextra").fadeOut();
	});
	//On sign up submission
	$(".signupform").submit(function() {
		var submittable = validateinput($(".one"),true);
		if (submittable) {
			return true;
		} else {
			return false;
		}
	});
});

//Updates the css taking in a dictionary
var updateformcss = function updateformcss(handler) {
	//Id of input
	var index = $(handler).attr('id');
	//Value in the dictionary
	var value = formelements[index];
	//Label handler
	var label = $($(handler).attr('data-label'));
	//If value is false
	if (value==false) {
		if (!(handler.hasClass("has-error"))) {
			handler.addClass("has-error");
		} 
		handler.parent().next().children("img").attr("src",x_mark_src);
	} else if (value=='clear') {
		handler.parent().next().children("img").attr("src",blank_src);
	} else {
		handler.removeClass("has-error")
		handler.parent().next().children("img").attr("src",check_mark_src);
	}
}

//Takes in a list of inputs to verify
var validateinput = function validateinput(handler,submiting) {
	if ($(handler).attr('id') =='businesstype' || submiting) {
		var validated = ($("#businesstype").val() == 'none' ) ? false : true;
		formelements['businesstype'] = validated;
		updateformcss($("#businesstype"));
	}
	if ($(handler).attr('id') =='name' || submiting) {
		var validated = ($("#name").val().length < 1 ) ? false : true;
		formelements['name'] = validated;
		updateformcss($("#name"));
	}
	if ($(handler).attr('id') =='email' || submiting ) {
		checkEmail();
	}
	if ($(handler).attr('id') =='address_one' || submiting) {
		var validated = ($("#address_one").val().length < 5) ? false : true;
		formelements['address_one'] = validated;
		updateformcss($("#address_one"));
	}
	if ($(handler).attr('id') =='city' || submiting) {
		var validated = ($("#city").val().length < 3) ? false : true;
		formelements['city'] = validated;
		updateformcss($("#city"));
	}
	if ($(handler).attr('id') =='state' || submiting) {
		formelements['state'] = true;
		updateformcss($("#state"));
	}
	if ($(handler).attr('id') =='zipcode' || submiting) {
		var validated = ($("#zipcode").val().length == 5) ? true : false;
		formelements['zipcode'] = validated;
		updateformcss($("#zipcode"));
	}
	if ($(handler).attr('id') =='website' || submiting) {
		formelements['website'] = true;
	}
	if ($(handler).attr('id') =='phonenumber' || submiting) {
		var validated = ($("#phonenumber").val().length == 14) ? true : false;
		formelements['phonenumber'] = validated;
		updateformcss($("#phonenumber"));
	}
	if ($(handler).attr('id') =='password' || submiting) {
		if ($("#password").val().length < 6) {
			$("#passwordtext").html("Password must be at least 6 characters");
			formelements['password'] = false;
		}  else {
			$("#passwordtext").html("");
			formelements['password'] = true;
		}
		updateformcss($("#password"));
	}
	var submittable = true;
	$.each(formelements, function(index,value) {
		if (value == false) {
			submittable = false;
		}
	});
	if (submittable) {
		return true;
	} else {
		return false;
	}
}

var checkEmail = function checkEmail() {
	$("#formemailtext").text("");
	var validemail = (isEmail($("#email").val()) && $("#email").val().length >0);
	if (!(validemail)) {
		formelements['email'] = false;
		updateformcss($("#email"));
		return;
	}
	$("#emailimage").attr('src',loading_src);
	$.ajax({
		type : "GET",
		data : {'email':$("#email").val()},
		url : "/checkemail",
		success : function(data) {
			if (data == 'valid') {
				formelements['email'] = true;
				updateformcss($("#email"));
			} else {
				formelements['email'] = false;
				updateformcss($("#email"));
				$("#formemailtext").text("Already in use");
			}
		}
	});
}
