var FormView = require('ampersand-form-view');
var templates = require('../templates/templates');

var ScientistFormView = FormView.extend({
    template: templates.scientist_form,
	fields: function() {
		return {

		};
	}
});

module.exports = ScientistFormView;