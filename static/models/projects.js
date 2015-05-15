var BaseModel = require('./base');

var Projects = BaseModel.extend({
    urlRoot: '/api/projects',
	props: {
		projects: 'array'
	}
});

module.exports = Projects;