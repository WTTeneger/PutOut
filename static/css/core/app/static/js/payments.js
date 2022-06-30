!function() {
	var overlay_content,overlay_close,overlay_frame,body_scroll_top,body_scroll_left,iframe_src,
		skeep_scroll = false,
		overlay_hidden = false,
		mobile = false,
		html = document.getElementsByTagName('html')[0],
		head = document.head || document.getElementsByTagName('head')[0],
		body = document.body || document.getElementsByTagName('body')[0],
		overlay = document.getElementById('Prodamus-payform-overlay'),
		overlay_style = document.getElementById('Prodamus-payform-style'),
		overlay_links = document.getElementsByClassName('Prodamus-startPay');

	var viewport_old = document.querySelector("meta[name=viewport]"),
		content_old = null,
		viewport_new = null,
		content_new = 'initial-scale=1, maximum-scale=1, user-scalable=no, width=device-width';

	if (viewport_old)
		content_old = viewport_old.getAttribute('content');

	// определение операционки
	if (navigator.userAgent.indexOf ('iPhone') != -1) {
		html.classList.add('iphone');
		html.classList.add('mobile');
		mobile = true;
	} else if (navigator.userAgent.indexOf ('iPad') != -1) {
		html.classList.add('ipad');
		html.classList.add('mobile');
		mobile = true;
	} else if (navigator.userAgent.indexOf ('Android') != -1) {
		html.classList.add('android');
	} else if (navigator.userAgent.indexOf ('Windows') != -1) {
		html.classList.add('windows');
	} else if (navigator.userAgent.indexOf ('Linux')!= -1) {
		html.classList.add('linux');
	} else if (navigator.userAgent.indexOf ('Mac')!= -1) {
		html.classList.add('mac');
	} else if (navigator.userAgent.indexOf ('FreeBSD')!= -1) {
		html.classList.add('freebsb');
	}

	if (!overlay) {
		//
		overlay = document.createElement('div');
		overlay.id = 'Prodamus-payform-overlay';
		overlay.style.display = 'none';
		body.appendChild(overlay);
		window.onkeydown = function (e) {
			var code = e.keyCode ? e.keyCode : e.which;
			// esc
			if (code === 27) {
				if (!overlay_hidden)
					hideOverlay();
			}
		};
		//
		overlay_content = document.createElement('div');
		overlay_content.id = 'Prodamus-payform-overlay_content';
		overlay.appendChild(overlay_content);
		//
		// iframe_src = document.currentScript.getAttribute('src').replace('/widget.js','/');
		iframe_src = document.currentScript.getAttribute('src').replace('/widget.js','/') + '?widget';
		overlay_frame = document.createElement('iframe');
		overlay_frame.id = 'Prodamus-payform-overlay_frame';
		// overlay_frame.allow = 'payment';
		overlay_frame.src = iframe_src;
		overlay_frame.frameborder = 0;
		overlay_frame.scrolling = 'yes';
		overlay_frame.setAttribute('allowpaymentrequest', '');
		overlay_frame.onload = function(){
			// прокрутка на начало страницы при загрузке, если не закрыли оверлей
			/*
			if (skeep_scroll)
				skeep_scroll = false;
			else if (990 >= window.innerWidth)
				window.scrollTo(0, 0);
			*/
		};
		overlay_content.appendChild(overlay_frame);
		//
// 		if (navigator.userAgent.match(/(iPod|iPhone|iPad)/)) {
// 			addClassName(overlay_content, 'ios');
// 			overlay_frame.scrolling = 'no';
// 		}
		//
		hideOverlay();
	}

	if (!overlay_style) {
		overlay_style = document.createElement('link');
		overlay_style.setAttribute('id', 'Prodamus-payform-style');
		overlay_style.setAttribute('rel', 'stylesheet');
		overlay_style.setAttribute('type', 'text/css');
		overlay_style.setAttribute('href', document.currentScript.getAttribute('src').replace('/widget.js','/widget.css'));
		head.appendChild(overlay_style);
	}

	if (overlay_links) {
		[].forEach.call(overlay_links, function(e, i, a) {
			e.addEventListener("click", function(evt){
				evt.preventDefault();
				evt.stopPropagation();
				toggleOverlay();
			});
		});
	}

	body.addEventListener('click', function(e) { if (!overlay_hidden) hideOverlay(); });
	overlay.addEventListener('click', function(e) { e.stopPropagation(); });

	function showOverlay() {
		// сохраняем позицию прокрутки для возврата при закрытии
		body_scroll_top = document.documentElement.scrollTop || document.body.scrollTop;
		body_scroll_left = document.documentElement.scrollLeft || document.body.scrollLeft;
		//
		addClassName(html, 'Prodamus-noScroll');
		removeClassName(overlay, 'Prodamus-state-hidden');
		// прокрутка на начало страницы на мобильных
		if (mobile) {
			window.scrollTo(0, 0);
			// setViewport();
		}
		overlay_hidden = false;
		CreateClose();
	}
	function hideOverlay() {
		removeClassName(html, 'Prodamus-noScroll');
		addClassName(overlay, 'Prodamus-state-hidden');
		// прокрутка на старое положение
		if (mobile) {
			window.scrollTo(body_scroll_left, body_scroll_top);
			//skeep_scroll = true;
			// rollbackViewport();
		}
		overlay_hidden = true;
		overlay_frame.src = iframe_src;
		if (overlay_close) { overlay_close.parentNode.removeChild(overlay_close); }

	}
	function toggleOverlay() {
		overlay_hidden ? showOverlay() : hideOverlay();
	}
	function CreateClose() {
		//
		overlay_close = document.createElement('img');
		overlay_close.id = 'Prodamus-payform-overlay_close';
		overlay_close.src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyRpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMy1jMDExIDY2LjE0NTY2MSwgMjAxMi8wMi8wNi0xNDo1NjoyNyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNiAoTWFjaW50b3NoKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo2MTRBRjQ0OEI5NzkxMUU3OTk0Q0UxNzE2NEYwREUzRSIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDo2MTRBRjQ0OUI5NzkxMUU3OTk0Q0UxNzE2NEYwREUzRSI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOkIwRjE4MEZGQjk1NzExRTc5OTRDRTE3MTY0RjBERTNFIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOkIwRjE4MTAwQjk1NzExRTc5OTRDRTE3MTY0RjBERTNFIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+3Pc8rQAABgZJREFUeNp8VutP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';
		overlay_close.addEventListener("click", function(evt){
			evt.preventDefault();
			hideOverlay();
		});
		overlay.appendChild(overlay_close);
	}
	function toggleClassName(element, class_name) {
		if (element.classList)
			element.classList.toggle(class_name);
		else {
			var classes = element.className.split(" "),
				i = classes.indexOf(class_name);
			if (i >= 0)
				classes.splice(i, 1);
			else
				classes.push(class_name);
			element.className = classes.join(" ");
		}
	}
	function addClassName(element, class_name) {
		if (element.classList)
			element.classList.add(class_name);
		else if (element.className.split(" ").indexOf(class_name) == -1)
			element.className += " " + class_name;
	}
	function removeClassName(element, class_name) {
		if (element.classList)
			element.classList.remove(class_name);
		else {
			var classes = element.className.split(" "),
				i = classes.indexOf(class_name);
			if (i >= 0) {
				classes.splice(i, 1);
				element.className = classes.join(" ");
			}
		}
	}
	function setViewport() {
		if (viewport_old) {
			viewport_old.setAttribute('content', content_new);
		}
		else {
			viewport_new = document.createElement('meta');
			viewport_new.setAttribute('name', 'viewport');
			viewport_new.setAttribute('content', content_new);
			head.appendChild(viewport_new);
		}
	}

	function rollbackViewport() {
		if (viewport_old) {
			viewport_old.setAttribute('content', content_old);
		}
		else if (viewport_new) {
			viewport_new.setAttribute('content', '');
			viewport_new = null;
		}
	}
}();