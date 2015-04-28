var Model = require('ampersand-model');

var Projects = Model.extend({
    urlRoot: '/api/projects',
	props: {
		data: 'array'
	}
});

module.exports = Projects;