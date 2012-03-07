function isScrolledIntoView(index, elem)
{
	var $elem = $(elem);
    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();

    var elemTop = $elem.offset().top;
    var elemBottom = elemTop + $elem.height();

//	var isInView = (elemBottom > docViewTop) && (elemTop < docViewBottom) && (elemBottom < docViewBottom) &&  (elemTop > docViewTop);
	var isInView = ((elemTop < docViewBottom) && (elemTop > docViewTop));
	//console.debug(elem, isInView);
	if(!isInView) {
		if(!$elem.hasClass('collapsed')){
			$elem.addClass('collapsed');
			$elem.css('overflow', 'hidden');
			$elem.animate({height:'60px'}, 500);
		}
	} else {
		if($elem.hasClass('collapsed')){
			var $img = $elem.find('img.feed-photo');
			if(!$img.attr('src')){
				$img.attr('src', $img.attr('data-src'));				
			}
			var height = $elem.find('div.feed-item').height();
			height = height<60?60:height;
			$elem.find('div.feed-item').height();
			$elem.removeClass('collapsed');
			//console.debug('animate');
			$elem.animate({height:$elem.find('div.feed-content').height()+'px'}, 500);
		}
	}
    return isInView;
}
var scrollInt = null;
$(document).bind("mobileinit", function(){
	$.extend($.mobile , {
    	loadingMessage : '加载中',
		defaultTransition : 'slide',
		pageLoadErrorMessage : '好像出错了'
	});
	// $(document).delegate('#page-home', 'swipeleft', function(){
	// 	console.debug('swipe');
	// 	$.mobile.changePage('settings', {transition:'slide'});
	// });

	$('#page-home').live('pageshow', function(event){
		$('#page-home ul li').addClass('collapsed');
		$('#page-home ul li').each(isScrolledIntoView);
//		console.debug('create');
	});

	$('#page-settings').live('pageshow',function(event){
		$("div.page-home").remove();
	});

	$(document).scroll(function(){
		//alert('scroll start');
//		console.log('scroll');
		// $('#page-home ul li').each(isScrolledIntoView);
		// if(!scrollInt){
		// 	scrollInt = setInterval(function(){
		// 		$('#page-home ul li').each(isScrolledIntoView);
		// 	}, 500);
		// }
		var list = $('#page-home ul li'), length = list.length;
		for(var i = 0; i<length; i++){
			isScrolledIntoView(i, list[i]);
		}
		if(!scrollInt){
			scrollInt = setInterval(function(){
				var breakIndex = 0; 
				for(var i = 0; i<length; i++){
					if(breakIndex>0 && i == breakIndex) break;
					if(isScrolledIntoView(i, list[i])){
						breakIndex = i+10;
					}
				}
			}, 500);
		}
	});

	$(document).live('scrollstart', function(){
		//alert('scroll start');
		// if(!scrollInt){
		// 	scrollInt = setInterval(function(){
		// 		$('#page-home ul li').each(isScrolledIntoView);
		// 	}, 500);
		// }
		if(!scrollInt){
			scrollInt = setInterval(function(){
				var breakIndex = 0; 
				for(var i = 0; i<length; i++){
					if(breakIndex>0 && i == breakIndex) break;
					if(isScrolledIntoView(i, list[i])){
						breakIndex = i+10;
					}
				}
			}, 1000);
		}
	});

	$(document).live('scrollstop', function(){
		//alert('scroll stop');
		clearInterval(scrollInt);
		scrollInt = null;
	});

	$(document).delegate('#add-button', 'tap', function(){
//		console.debug($('#add-text').val());
		var word =  $('#add-text').val();
		if(word)
			$.get('/settings/add/' + word, function(res){
				var length = $('#checkboxes div.ui-checkbox').length;
				$($('#checkboxes div.ui-checkbox')[length-1]).find('label').removeClass('ui-corner-bottom ui-controlgroup-last');
				res = $.parseJSON(res);
//				console.debug(res);
				$('#checkboxes').append('<a class="delete-word ui-btn ui-btn-icon-notext ui-btn-up-c" data-iconpos="notext" data-word="' + res.w + '" data-theme="c"><span class="ui-btn-inner"><span class="ui-btn-text">删除</span><span class="ui-icon ui-icon-delete ui-icon-shadow"></span></span></a><div class="ui-checkbox"><input type="checkbox" data-word="' + res.w + '" class="checkbox-item" id="checkbox-'+ length + '" name="checkbox-'+ length + '" class="custom" checked /><label for="checkbox-'+ length + '" class="ui-btn ui-btn-up-c ui-btn-icon-left ui-checkbox-on ui-corner-bottom ui-controlgroup-last"><span class="ui-btn-inner ui-corner-bottom ui-controlgroup-last"><span class="ui-btn-text">'+ res.w+' @ ' + res.c+ '</span><span class="ui-icon ui-icon-shadow ui-icon-checkbox-on"></span></span></label></div>');
			});
	});

	$('a.delete-word').live('tap', function(){
		var word = $(this).attr('data-word');
		var $this = $(this), $div = $this.next();
		$.get('/settings/delete/' + word, function(){
			$this.fadeOut();
			$div.fadeOut();
		});
	});

	$('input.checkbox-item').live('change', function(){
		var checked = $(this).prop('checked');
		var word = $(this).attr('data-word');
	 	
		if(checked)
			$.get('/settings/update/' + word + '/1');
		else 
			$.get('/settings/update/' + word + '/0');
		// console.debug($('#add-text').val());
		// var word =  $('#add-text').val();
		// $.get('/settings/add/' + word);
	});
});
