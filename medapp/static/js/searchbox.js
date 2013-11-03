// We must rebind all the actions when results are added to the page
var activateResultsBoxItems = function activateResultsBoxItems() {	
	//When user clicks for more information
	$('.infobutton').click(function() {
		togglebuttons($(this));
	});
	
	//When user closes the more information
	$('.closebutton').click(function() {
		$(this).parent().parent().addClass('hidden');
		var buttons = $(this).parent().parent().parent().children('div.textdiv').children('div.buttondiv').children();
		for (var b=0; b < buttons.length; b++) {
				$(buttons[b]).removeClass('activeinfo');
			}
	});
	//When a user clicks on an image
	$('.imgdiv img').click(function() {
		togglebuttons($($(this).parent().parent().children('div.textdiv').children('div.buttondiv').children()[0]));
	});
	
	//When a user hovers over a thumbnail
	$('.imagethumbnail img').hover(function() {
		$(this).parent().parent().parent().parent().children('div.imageviewer').css('display','table-cell');
		$(this).parent().parent().parent().parent().children('div.imageviewer').html("<div class='verticalalign'><img src='"+$(this).attr('src')+"'/></div>");
	}, function() {
		$(this).parent().parent().parent().parent().children('div.imageviewer').css('display','none');
		
	});
	
	
};

//Functionality for the show more buttons
var togglebuttons = function togglebutton(handler) {
	var buttons = handler.parent().children();
		if (!(handler.hasClass('activeinfo'))) {
			for (var b=0; b < buttons.length; b++) {
				$(buttons[b]).removeClass('activeinfo');
				handler.addClass('activeinfo');
			}
			var buttons = handler.parent().parent().parent().children('div.previewdiv');
			for (var i=0; i < buttons.length; i++) {
				if (!($(buttons[i]).hasClass("hidden"))) {
					$(buttons[i]).addClass("hidden");
				}
			};
			if ($(handler).text() == 'Details') {
				handler.parent().parent().parent().children('div.detailsdiv').removeClass('hidden');
			} else if ($(handler).text() == 'Specs') {
				handler.parent().parent().parent().children('div.specsdiv').removeClass('hidden');
			} else if ($(handler).text() == 'Condition') {
				handler.parent().parent().parent().children('div.conditiondiv').removeClass('hidden');
			} 
		}
}