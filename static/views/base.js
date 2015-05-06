var View = require('ampersand-view');

var BaseView = View.extend({
	render: function() {
		this.renderWithTemplate(this.model);
		return this;
	}
});

module.exports = BaseView;