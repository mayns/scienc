(function(){
	var customElements = (typeof document.registerElement === 'function');
	var shadowDom = (typeof document.createElement('div').createShadowRoot === 'function');
	var templates = (Object.getPrototypeOf(document.createElement('template')) === HTMLTemplateElement.prototype);
	var imports = ('import' in document.createElement('link'));
	var support = [customElements, shadowDom, templates, imports].every(function(item){
		return item;
	});

	if (!support) {
		var warning = document.createElement('div');
		var warningHtml = "Мы использовали некоторые передовые штуки так что ПОЖАЛУЙСТА откройте этот сайт в последней версии " +
			"<a href='https://www.google.com/chrome/browser/desktop/'>Chrome</a> или <a href='http://www.opera.com/download/'>Opera</a>";
		var scale = 1.171875;
		var body = document.body;
		var img = document.createElement('img');
		var height = window.innerHeight;
		var top = height;
		var width = window.innerWidth;
		var imgWidth = width * 0.8;
		var imgHeight = Math.round(imgWidth * scale);
		var marginLeft = imgWidth / 2;
		var direction = -1;


		img.src = '/static/images/slowpoke.svg';
		img.style.width = imgWidth + 'px';
		img.style.top = top + "px";
		img.style.marginLeft = -marginLeft + 'px';
		warning.innerHTML = warningHtml;
		body.innerHTML = "";
		body.classList.add('slowpoke');
		body.appendChild(img);
		body.appendChild(warning);

		function animate() {
			top = top + direction;
			if (top === -imgHeight) {
				direction = 1;
			}
			if (top === height) {
				direction = -1;
			}
			img.style.top = top + 'px';
			requestAnimationFrame(animate);
		}

		requestAnimationFrame(animate)
	}
})();