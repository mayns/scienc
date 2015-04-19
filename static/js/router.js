var AmpersandRouter = require('ampersand-router');

var AppRouter = AmpersandRouter.extend({

  routes: {
    "help":                 "help",    // #help
    "search/:query":        "search",  // #search/kiwis
    "search/:query/p:page": "search"   // #search/kiwis/p7
  },

  help: function() {
    //...
  },

  search: function(query, page) {
    //...
  }

});

module.exports = AppRouter;