var FormView = require('ampersand-form-view');
var BaseView = require('ampersand-view');
var templates = require('../templates/templates');
var AppInputView = require('./input');

var HighEducationView = BaseView.extend({
	template: templates.scientist_form.high_education
});


var ScientistFormView = BaseView.extend({
	events: {
		'click .js-add-education': 'addEducation',
		'click .js-delete-education': 'deleteEducation'
	},
    template: templates.scientist_form.main,
	render: function() {
		var self = this;

		self.renderWithTemplate();
		self.form = new FormView({
			el: self.query('.js-form'),
			model: self.model,
			autoAppend: false,
			fields:  [
				new AppInputView({
					el: self.query('.js-first-name'),
					name: 'first_name',
		            value: self.model.first_name,
					placeholder: 'Иван',
		            required: true
				}),
				new AppInputView({
					el: self.query('.js-last-name'),
					name: 'last_name',
					placeholder: 'Иванов',
		            value: self.model.last_name,
		            required: true
				}),
				new AppInputView({
					el: self.query('.js-middle-name'),
					name: 'middle_name',
					placeholder: 'Иванович',
		            value: self.model.middle_name,
		            required: true
				})
			],
			validCallback: function (valid) {
                if (valid) {
                    console.log('The form is valid!');
                } else {
                    console.log('The form is not valid!');
                }
            },
			submitCallback: function(data) {
				console.log(data);
			}
		});
		self.registerSubview(self.form);

		self.high_education = self.renderCollection(self.model.high_education, HighEducationView, self.query('.js-high-education'));
		return this;
	},
	addEducation: function() {
		this.model.high_education.add({});
	},
	deleteEducation: function(e) {
		var id = e.target.dataset._id;
		this.model.high_education.remove(id);
	}
});


module.exports = ScientistFormView;