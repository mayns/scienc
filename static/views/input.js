var InputView = require('ampersand-input-view');

var AppInputView = InputView.extend({
	initialize: function() {
		InputView.prototype.initialize.apply(this, arguments);
		this.render();
	},
	renderWithTemplate: function() {
		if (!this.el) {
			throw Error('View constructor expects el');
		}
		else {
			return this;
		}
	}
});

module.exports = AppInputView;