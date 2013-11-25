///***********************************************************************
///This script controls functionality to select the quality of the product
///***********************************************************************
var pagevariables = {'name':"",'manufacturer':"",'category':'','serialno':'','year':2013,'type':'preowned','contract':'notincluded','ownedlength':'','quality':4,'conditiondescription':"",'productdescription':'','pictureid':[],'mainimageid':-1,'shippingincluded':true,'price':0};


$(document).ready(function() {
	pictureBinds();
    var currentvalue = "4";
	$(".qualitybox select").css("opacity",".4");
	var q1 = "<span>Parts Only</span><p>This equipment has missing parts or serious defects. This item can be used to replace missing parts on other machines. </p>";
	var q2 = "<span>Fairly Used</span><p>This item has normal wear and tear</p>";
	var q3 = "<span>Gently Used</span><p>This item has small signs of use, but it is fully functional</p>";
	var q4 = "<span>Refurbished</span><p>This item has been restored to manufacturer standards</p>";
	var q5 = "<span>New</span><p>This item has not been used</p>";
	$(".qualitydescription p").html(q4);
	var qualitydict = {"1":q1,"2":q2,"3":q3,"4":q4,"5":q5};
	$('#inputname').typeahead('destroy');
	$('#inputname').typeahead({
	name: Math.random().toString(36).substr(2, 5),
	local: [
		'bob',
		'bill'
	] 
	});
	
	$(".qualitynumber").click(function() {
		var handle = $(this);
		var value = $(handle).attr('id').split("_")[1];
		if (currentvalue != value) {
			currentvalue = value;
			//Change opacities of the numbers
			$(".qualitynumber").css("opacity",".3");
			handle.css("opacity","1");
			//Move the arrow
			var margintomove = "";
			if (value == 1) {margintomove = '130px'};
			if (value == 2) {margintomove = '255px'};
			if (value == 3) {margintomove = '382px'};
			if (value == 4) {margintomove = '503px'};
			if (value == 5) {margintomove = '630px'};
			if (value == 6) {margintomove = '758px'};
			pagevariables['quality'] = value;
			$(".downarrow").animate({"margin-left":margintomove},400);
			$(".qualitydescription p").fadeOut('fast',function() {
				$(".qualitydescription p").html(qualitydict[value]);
				$(".qualitydescription p").fadeIn();
			});
		}		
	});
	$('#inputprice').blur(function() {
		$('#inputprice').html(null);
		$(this).formatCurrency({ colorize: true, negativeFormat: '-%s%n', roundToDecimalPlace: 0 });
		pagevariables['price'] = $(this).asNumber();
	})
	.keyup(function(e) {
		var e = window.event || e;
		var keyUnicode = e.charCode || e.keyCode;
		if (e !== undefined) {
			switch (keyUnicode) {
				case 16: break; // Shift
				case 17: break; // Ctrl
				case 18: break; // Alt
				case 27: this.value = ''; break; // Esc: clear entry
				case 35: break; // End
				case 36: break; // Home
				case 37: break; // cursor left
				case 38: break; // cursor up
				case 39: break; // cursor right
				case 40: break; // cursor down
				case 78: break; // N (Opera 9.63+ maps the "." from the number key section to the "N" key too!) (See: http://unixpapa.com/js/key.html search for ". Del")
				case 110: break; // . number block (Opera 9.63+ maps the "." from the number block to the "N" key (78) !!!)
				case 190: break; // .
				default: $(this).formatCurrency({ colorize: true, negativeFormat: '-%s%n', roundToDecimalPlace: -1, eventOnDecimalsEntered: true });
			}
		}
	})
	$("#fileupload").change(function() { 
		$("#fileform").submit();
		$("#imageloadercontainer .progress").css("display","block");
		$("#imageloadercontainer .progress-bar").animate({"width":"80%"},1000);
	});
	$('#fileform').ajaxForm(function(e) { 
		 $.each(e,function(index,value) {
		 	$("#imageloadercontainer .progress-bar").animate({"width":"100%"},400,function() {
		 		$("#imageloadercontainer .progress").css("display","none");
		 		$("#imageloadercontainer .progress-bar").attr({"width":"0%"});
		 	});
			$("#noimages").css('display','none');
			pagevariables['pictureid'].push(e[index][0]);
			if (pagevariables['pictureid'].length > 1) {
				var main = '<h6>Make Main Photo</h6>';
			}
			else {
				var main= "<h6 class='main'>Main Photo</h6>";
				pagevariables['mainimageid'] = parseInt(e[index][0]);
			}
			$("#imagepreview").append("<div class='imagepreviewcontainer'>"+main+"<div class='imagepreviewborder'><p class='delete'>&#10006;</p><img class='imagepreview' id='image_"+e[index][0]+"' src='"+e[index][1]+"'/><div></div>");
		 	pictureBinds();
		 });
	});
	$("#inputcontract").change(function() { 
		console.log("here");
		if ($(this).val() == 'included') {
			$("#warrantydescribe").text("Please describe the details of the warranty or service contract in the product description");
		}
		if ($(this).val() == 'optional') {
			$("#warrantydescribe").text("Upon a buyer purchasing your item, you will acquire a transferrable service contract at your cost");
		}
		if ($(this).val() == 'notincluded') {
			$("#warrantydescribe").text("There is no warranty of service contract associated with this item");
		}
	});
	$("#inputtype").change(function() { 
		console.log("here");
		if ($(this).val() == 'preowned') {
			$("#dateacquired").fadeIn();
		}
		else {
			$("#dateacquired").fadeOut();
		}
	});
	
	var checkin = $('#inputownerlength').datepicker();
	$("#postitem").click(function() { 
		updatePageVariables();
		postitem();
	});
	$("#edititem").click(function() { 
		updatePageVariables();
		edititem();
	});
});	

var updatePageVariables = function updatePageVariables() {
	pagevariables['name'] = $("#inputname").val();
	pagevariables['manufacturer'] = $("#inputmanufacturer").val();
	pagevariables['category'] = $("#inputcategory").val();
	pagevariables['serialno'] = $("#inputserialno").val();
	pagevariables['productdescription'] = $("#inputproductdescription").val();
	pagevariables['conditiondescription'] = $("#inputconditiondescription").val();
	pagevariables['price'] = parseInt($("#inputprice").asNumber());
	pagevariables['contract'] = $("#inputcontract").val();
	pagevariables['ownedlength'] = $("#inputownerlength").val();
	if (pagevariables['pictureid'].length == 0) {
		pagevariables['mainimageid'] = -1;
	}
	if ($("#shippingincluded").is(":checked")) {
		pagevariables['shippingincluded'] = true;
	} else {
		pagevariables['shippingincluded'] = false;
	}
};

var postitem = function postitem() {
	if (validate()) {
		$.ajax({
			type : "POST",
			data : pagevariables,
			url : "/postitem",
			success : function(data) {
				console.log(data)
				if (data == '100') {
					window.location.href = "/listeditems";
				}
			}, 
			error : function(jqXHR, textStatus, errorThrown) {
				alert("Error posting product. Please try again later or email us so we can diagnose the problem");
			}
		});
	}
}
var edititem = function saveitem() {
	if (validate()) {
		$.ajax({
			type : "POST",
			data : pagevariables,
			url : "/editform",
			success : function(data) {
				window.location.href = "/listeditems";
			}, 
			error : function(jqXHR, textStatus, errorThrown) {
				alert(errorThrown);
			}
		});
	}
}
var validate = function validate() {
	var errorstring = "Oops! It looks like you forget the " 
	var submittable = true;
	if ($("#inputname").val().length == 0) {
		errorstring += "model name, "
		submittable = false;
	}
	if ($("#inputproductdescription").val().length == 0) {
		errorstring += "product description, "
		submittable = false;
	}
	if ($("#inputconditiondescription").val().length == 0) {
		errorstring += "condition description, "
		submittable = false;
	}
	if ($("#inputprice").val().length == 0) {
		errorstring += "price, "
		submittable = false;
	}
	if (!($("#termsagree").is(":checked"))) {
		errorstring += 'agreeing to selling terms, ';
		submittable = false;
	} 
	if (submittable) {
		return true;
	} else {
		errorstring = errorstring.slice(0,-2);
		errorstring += ".";
		alert(errorstring);
	}
		

}
var pictureBinds = function pictureBinds() {
	$(".imagepreviewcontainer .delete").click(function() {
		var id = parseInt($(this).next().attr('id').split("_")[1]);
		index = pagevariables['pictureid'].indexOf(id);
		if (index > -1) {
			pagevariables['pictureid'].splice(index, 1);
		}
		if ($(this).parent().parent().children('h6').hasClass('main') && pagevariables['pictureid'].length > 0 ) {
			var child =$("#imagepreview").children('.imagepreviewcontainer')[0]
			$(child).children('h6').addClass('main');
			var newmainid = $("#imagepreview").children('.imagepreviewcontainer').find('img').attr('id').split("_")[1];
			pagevariables['mainimageid'] = newmainid;
		} 
		$(this).parent().parent().remove();
		if ($("#imagepreview").children('.imagepreviewcontainer').length == 0) {
			pagevariables['mainimageid'] = -1;
		}
	});
	$(".imagepreviewcontainer h6").click(function() {
		var id = parseInt($(this).next().children('.imagepreview').attr('id').split("_")[1]);
		pagevariables['mainimageid'] = id;
		$(".imagepreviewcontainer h6").removeClass('main');
		$(".imagepreviewcontainer h6").text('Make Main Photo');
		$(this).addClass('main');
		$(this).text('Main Photo');
	
	});
}