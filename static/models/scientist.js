var BaseModel = require('./base');
var AmpState = require('ampersand-state');
var BaseCollection = require('ampersand-collection');
var App = require('ampersand-app');

var HighEducation = AmpState.extend({
	initialize: function() {
		this.set({_id: App.getId()});
	},
	props: {
		chair: ['string', false, ''],
		city: ['string', false, ''],
		country: ['string', false, ''],
		degree: ['string', false, ''],
		faculty: ['string', false, ''],
		graduation_year: ['string', false, ''],
		university: ['string', false, '']
	},
	session: {
		_id: 'number'
	}
});

var HighEducationCollection = BaseCollection.extend({
	model: HighEducation,
	mainIndex: '_id'
});

var ScientistModel = BaseModel.extend({
	urlRoot: '/api/scientists',
	idAttribute: 'id',
	props: {
		id: ['string', true, ''],
		first_name: ['string', true, ''],
		middle_name: ['string', true, ''],
		last_name: ['string', true, ''],
		image_url: ['string', false,  '/static/images/profile.svg'],
		dob: ['string', true, ''],
		gender: {
			type: 'string',
			values: ['f', 'm']
		},
		location: 'object',
		middle_education: 'object',
		interests: 'array',
		about: ['string', false, '']
	},
	collections: {
		high_education: HighEducationCollection,
		publications: BaseCollection,
		contacts: BaseCollection
	},
	derived: {
		formType: {
			deps: ['id'],
			fn: function () {
                return this.id === '' ? 'create' : 'update';
            }
		}
	}
});



module.exports = ScientistModel;