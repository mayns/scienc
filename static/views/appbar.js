var BaseView = require('./base');
var templates = require('../templates/templates');

var AppBarView = BaseView.extend({
	initialize: function() {
		var self = this;

		self.model.on('sync', function(){
			self.render();
		});
	},
    template: templates.appbar
});

module.exports = AppBarView;