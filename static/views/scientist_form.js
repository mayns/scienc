var FormView = require('ampersand-form-view');
var BaseView = require('ampersand-view');
var templates = require('../templates/templates');

var ScientistFormView = BaseView.extend({
    template: templates.scientist_form,
	render: function() {
		var self = this;

		self.renderWithTemplate();
		self.form = new FormView({
			el: self.query('form'),
			model: app.user,
			autoAppend: false,
			fields:  [
				new AppInputView({
					el: self.query('.js-email'),
					name: 'email',
		            value: '',
					placeholder: 'E-mail',
		            required: true
				}),
				new AppInputView({
					el: self.query('.js-password'),
					name: 'pwd',
					placeholder: 'Password',
		            value: '',
		            required: true
				})
			],
			submitCallback: function(data) {
				console.log(data);
			}
		});
		self.registerSubview(self.form);
		return this;
	}
});

module.exports = ScientistFormView;