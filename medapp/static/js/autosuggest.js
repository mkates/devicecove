/* ========================================================================
** Custom Built Autosuggest for the search bar ****************************
 * ======================================================================== */
var autosuggest = true;
var displayresults = [];
var activeid = -1;
var resultshandle = [];
var searchtext = '';						
var autosuggestcall = function autosuggestcall() {
	$.ajax({
		url: '/autosuggest',
		type: 'GET',
		data: {"searchterm":$("#searchinput").val()},
		cache:true,
		dataType: 'json',
		success: function(response){
			console.log(response.length);
			if (response.length == 0) {
				$("#autosuggest").css('display','none');
			} else {
				resultshandle = [];
				activeid = -1;
				displayresults = response;
				$("#categoriessection").empty();
				$("#productssection").empty();
				$(".categoriesheader").css('display','none');
				$(".productsheader").css('display','none');
				$.each(displayresults, function( key, value ) {
					if (!(value['mainimage'])) {
						value['mainimage'] = noImageURL;
					}
					if (value['type'] == 'category') {
						var so = $("<a class='searchoption' href='"+value['link']+"'><div class='textitem'><p class='displaytext'>"+value['name']+"</p></div></a>");
						$("#categoriessection").append(so);
						$(".categoriesheader").css('display','block');
						resultshandle.push(so);
					} else if (value['type'] == 'subcategory') {
						var so = $("<a class='searchoption' href='"+value['link']+"'><div class='textitem'><p class='displaytext'>"+value['name']+"</p></div></a>");
						$("#categoriessection").append(so);
						$(".categoriesheader").css('display','block');
						resultshandle.push(so);
					} else if (value['type'] == 'product'){
						var so = $("<a class='searchoption' href='"+value['link']+"'><div class='productitem'><img src='"+value['mainimage']+"'/><div class='producttext'><p class='displaytext' class='productname'>"+value['name']+"</p><p class='productsubtext'>in "+value['category']+"</p></div><div class='clear'></div></div></a></div>");
						$("#productssection").append(so);
						resultshandle.push(so);
						$(".productsheader").css('display','block');
					}
				});
				$("#autosuggest").css('display','block');
			} 
		}
	});
	return
}


$(document).ready(function() {
	if ($("#searchinput").val().length > 0) {
		$("#search-exit").css("display","block");
	}
	$(".customsearchbar input").focus(function() {
		$(".customsearchbar button").addClass("blueborder");
	});
	$(".customsearchbar input").blur(function() {
		$(".customsearchbar button").removeClass("blueborder");
	});
	$("#search-exit").click(function() {
		$("#searchinput").val("");
		$("#searchinput").focus();
		$("#search-exit").css("display","none");
	});
	$("#searchinput").focus(function() {
		if ($("#searchinput").val().length > 0) {
			//autosuggestcall();
			$("#autosuggest").css("display","block");
			autosuggest = true;
		} else {
			//autosuggest = false;
		}
	});
	$("#searchinput").keyup(function(e) {
		if ($("#searchinput").val().length > 0) {
			$("#search-exit").css("display","block");
			if ($(e.target).attr("id") == "searchinput" && e.keyCode != 40 && e.keyCode !=38)  {
				autosuggestcall();
			}
			autosuggest = true;
		} else {
			$("#autosuggest").css("display","none");
			$("#search-exit").css("display","none");
			autosuggest = false;
		}
		if (e.keyCode != 40 && e.keyCode !=38) {
			searchtext =  $("#searchinput").val();
		}
	});
	$(document).click(function (e)
	{
		var container = $("#desktopsearchbar");

		if (!container.is(e.target) // if the target of the click isn't the container...
			&& container.has(e.target).length === 0) // ... nor a descendant of the container
		{
			$("#autosuggest").hide();
		}
	});
	$("#searchform").submit(function() {
		var active = $(".activesearchoption");
		if (active.length > 0) {
			window.location.href = $(active).attr("href")
			return false;
		} else {
			return true;
		}
	});
});  
$(document).keyup(function(e){
	if (e.keyCode == 40 && autosuggest==true) {
	   $(".searchoption").removeClass("activesearchoption");
	   activeid += 1;
	   if (activeid <= 0) {
		   $(resultshandle[0]).addClass("activesearchoption");
	   } else if (activeid >= resultshandle.length) {
		   $(resultshandle[activeid-1]).addClass("activesearchoption");
		   activeid -= 1;
		   return false;
	   } else {
			$(resultshandle[activeid]).addClass("activesearchoption");
	   }
		$("#searchinput").val($(resultshandle[Math.max(0,activeid)]).find(".displaytext").text());
	   return false;
	} else if (e.keyCode == 38 && autosuggest==true) {
		activeid -= 1;
	   $(".searchoption").removeClass("activesearchoption");
	   if (activeid < 0) {
			activeid = -1;
			$("#searchinput").val(searchtext);
			return false;
	   } else {
			$(resultshandle[activeid]).addClass("activesearchoption");
	   }
		$("#searchinput").val($(resultshandle[activeid]).find(".displaytext").text());
	   return false;
	}
});
