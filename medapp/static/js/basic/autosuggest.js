/* ========================================================================
** Custom Built Autosuggest for the search bar ****************************
 * ======================================================================== */
var autosuggest = true;
var displayresults = [];
var activeid = -1;
var resultshandle = [];
var searchtext = '';

var autosuggestcall = function autosuggestcall(bar) {
	var data = (bar == 'desktop' ) ? $("#searchinput").val() : $("#mobile-searchbar input").val();
	$.ajax({
		url: '/form/autosuggest',
		type: 'GET',
		data: {"searchterm":data},
		cache:true,
		dataType: 'json',
		success: function(response){
			if (response.length == 0) {
				$("#autosuggest").css('display','none');
			} else {
				if (bar=='desktop') {
					resultshandle = [];
					activeid = -1;
					displayresults = response;
					$("#autosuggest .section-content").empty();
					$("#autosuggest .section").css('display','none');
					$.each(displayresults, function( key, value ) {
						if (!(value['mainimage'])) {
							value['mainimage'] = noImageURL;
						}
						if (value['type'] == 'category') {
							var so = $("<a class='searchoption' href='/category/"+value['link']+"'><div class='textitem'><p class='displaytext'>"+value['name']+"</p></div></a>");
							$("#categoriessection").append(so);
							$(".categoriesheader").css('display','block');
							resultshandle.push(so);
						} else if (value['type'] == 'manufacturer') {
							var so = $("<a class='searchoption' href='/manufacturer/"+value['link']+"'><div class='textitem'><p class='displaytext'>"+value['name']+"</p></div></a>");
							$("#manufacturerssection").append(so);
							$(".manufacturerheader").css('display','block');
							resultshandle.push(so);
						} else if (value['type'] == 'product'){
							var so = $("<a class='searchoption' href='/product/"+value['link']+"'><div class='productitem'><div class='img-div'><img src='"+value['mainimage']+"'/></div><div class='producttext'><p class='displaytext' class='productname'>"+value['name']+"</p><p class='productsubtext'>in "+value['category']+"</p></div><div class='clear'></div></div></a></div>");
							$("#productssection").append(so);
							resultshandle.push(so);
							$(".productsheader").css('display','block');
						}
					});
					$("#autosuggest").css('display','block');
				} else {
					$("#sidr-searchresults").empty();
					$.each(response, function( key, value ) {
						$("#sidr-searchresults").append("<a href='"+value['link']+"'>"+value['name']+"</a>");
					});
				}
			} 
		}
	});
	return
}


$(document).ready(function() {
	//Show the X if their is a value in the search
	if ($("#searchinput").val().length > 0) {
		$("#search-exit").css("display","block");
	}
	//On X click, clear search results
	$("#search-exit").click(function() {
		$("#searchinput").val("");
		$("#searchinput").focus();
		$("#search-exit").css("display","none");
	});

	//On focus back to searchbar
	$("#searchinput").focus(function() {
		if ($("#searchinput").val().length > 0) {
			//autosuggestcall();
			//$("#autosuggest").css("display","block");
			autosuggest = true;
		} else {
			autosuggest = false;
		}
	});

	//On key enter for searching on desktop
	$("#searchinput").keyup(function(e) {
		if ($("#searchinput").val().length > 0) {
			$("#search-exit").css("display","block");
			if ($(e.target).attr("id") == "searchinput" && e.keyCode != 40 && e.keyCode !=38)  {
				autosuggestcall('desktop');
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

	//If click outside of search bar or autosuggest, hide it
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
