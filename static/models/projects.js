var Model = require('ampersand-model');

var Projects = Model.extend({
    urlRoot: '/api/projects'
});

module.exports = Projects;