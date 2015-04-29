var View = require('ampersand-view');
var templates = require('../templates/templates');

var ProjectsView = View.extend({
    template: templates.projects,
    render: function() {
        this.renderWithTemplate(this.model);
        return this;
    }
});

module.exports = ProjectsView;