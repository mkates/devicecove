var formelements = {'firstname':false,'lastname':false,'email':false,'password':false,'confirmpassword':false};
// var states = ['AK',"AL","AR","AS","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"];

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
	//On sign up submission
	$("#signupform").submit(function() {
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
	//id of input
	var index = $(handler).attr('id');
	//Value in the dictionary
	var value = formelements[index];
	//Label handler
	var label = $($(handler).attr('data-label'));
	//If value is false
	if (value==false) {
		if (!(handler.hasClass("has-error"))) {
			handler.addClass("has-error");
			$(handler).next().children('span.glyphicon-ok').css('display','none');
			$(handler).next().children('span.glyphicon-remove').css('display','block');
			console.log($(handler).next().children('span.glyphicon-remove'));
		} 
	} else if (value=='clear') {
		$(handler).next().children('span.glyphicon-ok').css('display','block');
		$(handler).next().children('span.glyphicon-remove').css('display','none');
	} else {
		handler.removeClass("has-error")
		$(handler).next().children('span.glyphicon-ok').css('display','block');
		$(handler).next().children('span.glyphicon-remove').css('display','none');
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
		$("#emailtext").text("");
		checkEmail();
	}
	if ($(handler).attr('id') =='password' || submiting) {
		if ($("#password").val().length < 6) {
			$("#passwordtext").text("Too Short (Minimum 6 Characters)");
			formelements['password'] = false;
		}  else {
			$("#passwordtext").html("");
			formelements['password'] = true;
		}
		updateformcss($("#password"));
	}
	if ($(handler).attr('id') =='confirmpassword' || submiting) {
		if ($("#confirmpassword").val() != $("#password").val()) {
			$("#confirmpasswordtext").text("Passwords do not match");
			formelements['confirmpassword'] = false;
		} else {
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
		$("#emailtext").text("Invalid Email");
		formelements['email'] = false;
		updateformcss($("#email"));
		return;
	}
	// $("#emailimage").attr('src',loading_src);
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
				$("#emailtext").text("Already in use (Login Instead)");
			}
		}
	});
}
