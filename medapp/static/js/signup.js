var formelements = {'firstname':false,'lastname':false,'email':false,'password':false,'confirmpassword':false};
var states = ['AK',"AL","AR","AS","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"];

function isEmail(email) {
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  return emailReg.test(email);
}

$(document).ready(function() {
	$("input").blur(function() {
		validateinput($(this),false);
	});
	$("input").keyup(function() {
		validateinput($(this),false);
	});
	$("#zipcode").keyup(function() {
		$(this).val($(this).val().replace(/\D/g,''));
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
	if ($(handler).attr('id') =='firstname' || submiting) {
		var validated = ($("#firstname").val().length < 1 ) ? false : true;
		formelements['firstname'] = validated;
		updateformcss($("#firstname"));
	}
	if ($(handler).attr('id') =='lastname' || submiting) {
		var validated = ($("#lastname").val().length < 1 ) ? false : true;
		formelements['lastname'] = validated;
		updateformcss($("#lastname"));
	}
	if ($(handler).attr('id') =='email' || submiting ) {
		checkEmail();
	}
	if ($(handler).attr('id') =='zipcode' || submiting) {
		var validated = ($("#zipcode").val().length == 5) ? true : false;
		formelements['zipcode'] = validated;
		updateformcss($("#zipcode"));
	}
	if ($(handler).attr('id') =='password' || submiting) {
		if ($("#password").val().length < 6) {
			$("#passwordtext").html("Too Short (Minimum 6 Characters)");
			formelements['password'] = false;
		}  else {
			$("#passwordtext").html("");
			formelements['password'] = true;
		}
		updateformcss($("#password"));
	}
	if ($(handler).attr('id') =='confirmpassword' || submiting) {
		if ($("#confirmpassword").val() != $("#password").val()) {
			$("#confirmpasswordtext").html("Passwords do not match");
			formelements['confirmpassword'] = false;
		}  else {
			$("#confirmpasswordtext").html("");
			formelements['confirmpassword'] = true;
		}
		updateformcss($("#confirmpassword"));
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
				$("#formemailtext").text("Already in use (Login Instead)");
			}
		}
	});
}
