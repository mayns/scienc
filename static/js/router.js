var AmpersandRouter = require('ampersand-router');

var AppRouter = AmpersandRouter.extend({

  routes: {
    "scientist": "scientist",
    "scientists": "search",
    "search/:query/p:page": "search"
  },

  scientist: function() {
    //...
  },

  search: function(query, page) {
    //...
  }

});

module.exports = AppRouter;

//<app-route path="/" element="project-list"></app-route>
//<app-route path="/scientist" element="scientist-form"></app-route>
//<app-route path="/scientists" element="scientists-list"></app-route>
//<app-route path="/scientist/my-projects" element="my-projects"></app-route>
//<app-route path="/scientist/:id" element="scientist-page"></app-route>
//<app-route path="/project/:id" element="project-page"></app-route>
//<app-route path="/project" element="project-modify"></app-route>
//<app-route path="/signup" element="scientist-modify"></app-route>
//<app-route path="/page-not-found" element="page-not-found"></app-route>
//<app-route path="/search" element="search-page"></app-route>
//<app-route path="*" redirect="/page-not-found"></app-route>