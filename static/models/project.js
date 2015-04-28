var Model = require('ampersand-model');

var Project = Model.extend({
	idAttribute: 'id',
    props: {
    	id: 'number',
    	title: ['string', true, ''],
    	description_short: ['string', true, ''],
    	research_fields: ['array', true, []],
    	university_connection: ['boolean', false, true],
    	description_full: 'string',
    	objective: 'string',
    	usage_possibilities: 'string',
    	results: 'string',
    	likes: ['number', false, 0],
    	in_progress: ['boolean', false, true]
    }
});

module.exports = Project;