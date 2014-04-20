// We must rebind all the actions when results are added to the page
var activateResultsBoxItems = function activateResultsBoxItems() {	
	$('.infobutton').unbind('click');
	$('.closebutton').unbind('click');
	
	//When user clicks for more information
	$('.infobutton').click(function() {
		togglebuttons($(this));
	});
	
	//When user closes the more information
	$('.closebutton').click(function() {
		var result_item = $(this).parent().parent().parent();
		console.log(result_item);
		$(result_item).find('.previewdiv').removeClass('visible');
		var buttons = $(result_item).find('.buttondiv').children();
		for (var b=0; b < buttons.length; b++) {
				$(buttons[b]).removeClass('activeinfo');
			}
	});
	
	// //When a user hovers over a thumbnail
// 	$('.imagethumbnail').hover(function() {
// 		$(this).parent().parent().parent().children('div.imageviewer').css('display','table-cell');
// 		$(this).parent().parent().parent().children('div.imageviewer').html("<div class='verticalalign'><img src='"+$(this).children('img').attr('data-original')+"'/></div>");
// 		console.log($(this).children('img'));
// 	}, function() {
// 		$(this).parent().parent().parent().children('div.imageviewer').css('display','none');
// 		
// 	});
	
	
};

//Functionality for the show more buttons
var togglebuttons = function togglebutton(handler) {
	var box_handle = handler.parent().parent().parent().parent();
	var thisbutton = handler;
	var buttons = handler.parent().children();
	$(buttons).removeClass('activeinfo');
	$(thisbutton).addClass('activeinfo');
	$(box_handle).find('.previewdiv').removeClass("visible")
	var toggleclass = $(thisbutton).attr('data-ref');
	
	$(toggleclass).addClass('visible');
}

$(document).ready(function() {
	activateResultsBoxItems();
});