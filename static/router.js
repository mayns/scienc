var Router = require('ampersand-router');
var ProjectsView = require('./views/projects');
var Projects = require('./models/projects');
var ScientistsView = require('./views/scientists');
var Scientists = require('./models/scientists');
var ScientistView = require('./views/scientist_form');
var Scientist = require('./models/scientist');
var App = require('ampersand-app');

var AppRouter = Router.extend({
    routes: {
        "": "projects",
	    "projects/:id": "project",
        "scientists": "scientists",
        "scientist/:id": "scientist",
        "scientist/my-projects": "myProjects"
    },
    projects: function () {
        var self = this;
        var projects = new Projects();

        projects.on('sync', function(){
            self.trigger('newPage', new ProjectsView({
                model: projects
            }));
        });

        projects.fetch();
    },
	project: function(id) {
		var self = this;
		var project = new Project({
			id: id
		});

		project.on('sync', function(){
			self.trigger('newPage', new ProjectView({
				model: project
			}));
		});

		project.fetch();
	},
    scientists: function () {
		var self = this;
	    var scientists = new Scientists();

	    scientists.on('sync', function(){
            self.trigger('newPage', new ScientistsView({
                model: scientists
            }));
        });

        scientists.fetch();
    },
    scientist: function (id) {
        var self = this;
        var scientist = new Scientist({
	        id: id
        });
	    var scientistView = new ScientistView({
            model: scientist
        });

        scientist.on('sync', function(){
            self.trigger('newPage', scientistView);
        });
		App.models.active = scientist;
		App.views.active = scientistView;
        scientist.fetch();
    }

});

module.exports = AppRouter;
//<app-route path="/" element="project-list"></app-route>
//<app-route path="/scientists" element="scientists-list"></app-route>
//<app-route path="/scientist/my-projects" element="my-projects"></app-route>
//<app-route path="/scientist/:id" element="scientist-page"></app-route>
//<app-route path="/project/:id" element="project-page"></app-route>
//<app-route path="/project" element="project-modify"></app-route>
//<app-route path="/signup" element="scientist-modify"></app-route>
//<app-route path="/page-not-found" element="page-not-found"></app-route>
//<app-route path="/search" element="search-page"></app-route>
//<app-route path="*" redirect="/page-not-found"></app-route>