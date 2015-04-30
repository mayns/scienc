var app = require('ampersand-app');
var View = require('ampersand-view');

var MainView = View.extend({
	events: {
		'click .js-link': 'handleLinkClick'
	},
	handleLinkClick: function (e) {
		e.preventDefault();
		app.router.navigate(e.target.href);
	}
});

module.exports = MainView;