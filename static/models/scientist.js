var BaseModel = require('./base');
var AmpState = require('ampersand-state');
var BaseCollection = require('ampersand-collection');
var App = require('ampersand-app');
var ValidationMixin = require('ampersand-model-validations-mixin');

var Publication = AmpState.extend({
	props: {
		link: ['string', false, ''],
		source: ['string', false, ''],
		title: ['string', false, ''],
		year: ['number', false, '']
	}
});

var Contact = AmpState.extend({
	props: {
		connection: ['string', false, ''],
		number: ['string', false, '']
	}
});

var HighEducation = AmpState.extend({
	props: {
		chair: ['string', false, ''],
		city: ['string', false, ''],
		country: ['string', false, ''],
		degree: ['string', false, ''],
		faculty: ['string', false, ''],
		graduation_year: ['string', false, ''],
		university: ['string', false, '']
	}
});

var HighEducationsCollection = BaseCollection.extend({
	model: HighEducation,
	mainIndex: 'cid'
});

var PublicationsCollection = BaseCollection.extend({
	model: Publication,
	mainIndex: 'cid'
});

var ContactsCollection = BaseCollection.extend({
	model: Contact,
	mainIndex: 'cid'
});

var ScientistModel = BaseModel.extend(ValidationMixin, {
	urlRoot: '/api/scientists',
	idAttribute: 'id',
	props: {
		id: ['string', true, ''],
		first_name: ['string', true, ''],
		middle_name: ['string', true, ''],
		last_name: ['string', true, ''],
		image_url: ['string', false,  '/static/images/profile.svg'],
		dob: ['string', false, ''],
		gender: {
			type: 'string',
			values: ['f', 'm']
		},
		location: 'object',
		middle_education: 'object',
		interests: 'array',
		about: ['string', false, '']
	},
	validations: {
		first_name: {
			type: 'blank',
			msg: 'Поле обязательно для заполнения'
		},
		middle_name: {
			type: 'blank',
			msg: 'Поле обязательно для заполнения'
		},
		last_name: {
			type: 'blank',
			msg: 'Поле обязательно для заполнения'
		}
	},
	collections: {
		high_education: HighEducationsCollection,
		publications: PublicationsCollection,
		contacts: ContactsCollection
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