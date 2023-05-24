$(document).ready(function() {

	function consoleText(id) {
		var con = $('#console');
		var target = $('#console-text');
		var strToType = target.attr('data-text').split(', ');
		var letterCount = 1;
		var x = 1;
		var waiting = false;
		

		window.setInterval(function() {
			if (letterCount === 0 && !waiting) {
				waiting = true;
				target.html(strToType[0].substring(0, letterCount));
				window.setTimeout(function() {
					var usedWord = strToType.shift();
					strToType.push(usedWord);
					x = 1;
					letterCount += x;
					waiting = false;
				}, 1500);
			} else if (letterCount === strToType[0].length + 1 && !waiting) {
				waiting = true;
				window.setTimeout(function() {
					x = -1;
					letterCount += x;
					waiting = false;
				}, 1500);
			} else if (!waiting) {
				target.html(strToType[0].substring(0, letterCount)); 
				letterCount += x;
			}
		}, 100);
		
		window.setInterval(function() {
			$('#console').toggleClass('hidden');
		}, 400);
	}

	consoleText('console-text');

	// SMOOTH SCROLLING TO ALL LINKS IN NAVBAR
	$(".navbar a, footer a[href='#myPage']").on('click', function(event) {
		if (this.hash !== "") {
			event.preventDefault();

			var hash = this.hash;

			$('html, body').animate({
				scrollTop: $(hash).offset().top
			}, 900, function() {
				window.location.hash = hash;
			});
		}
	});
});
