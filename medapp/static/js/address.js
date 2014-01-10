var formelements = {'address_name':false,'address_one':false,'address_two':true,'address_zipcode':false,'address_city':false,'address_state':true,'address_phonenumber':false};
var states = ['AK',"AL","AR","AS","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"];

//On an address edit click, pre-populate new address fields
$('.editinformation').click(function() {
	var parent = $(this).parent();
	$("#address_name").val(parent.find('.address_name').text());
	$("#address_one").val(parent.find('.address_one').text());
	$("#address_two").val(parent.find('.address_two').text());
	$("#address_city").val(parent.find('.address_city').text());
	$("#address_state").val(parent.find('.address_state').text());
	$("#address_zipcode").val(parent.find('.address_zipcode').text());
	$("#address_phonenumber").val(parent.find('.address_phonenumber').text());
});

$(document).ready(function() {
	$("#address_phonenumber").mask("(999) 999-9999");
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
		$("#address_state").append("<option>"+states[i]+"</option>");
	}
	//On sign up submission
	$(".addressform").submit(function() {
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
	if ($(handler).attr('id') =='address_name' || submiting) {
		var validated = ($("#address_name").val().length < 1 ) ? false : true;
		formelements['address_name'] = validated;
		updateformcss($("#address_name"));
	}
	if ($(handler).attr('id') =='address_one' || submiting) {
		var validated = ($("#address_one").val().length < 5) ? false : true;
		formelements['address_one'] = validated;
		updateformcss($("#address_one"));
	}
	if ($(handler).attr('id') =='address_city' || submiting) {
		var validated = ($("#address_city").val().length < 3) ? false : true;
		formelements['address_city'] = validated;
		updateformcss($("#address_city"));
	}
	if ($(handler).attr('id') =='address_state' || submiting) {
		formelements['address_state'] = true;
		updateformcss($("#address_state"));
	}
	if ($(handler).attr('id') =='address_zipcode' || submiting) {
		var validated = ($("#address_zipcode").val().length == 5) ? true : false;
		formelements['address_zipcode'] = validated;
		updateformcss($("#address_zipcode"));
	}
	if ($(handler).attr('id') =='address_phonenumber' || submiting) {
		var validated = ($("#address_phonenumber").val().length == 14) ? true : false;
		formelements['address_phonenumber'] = validated;
		updateformcss($("#address_phonenumber"));
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
