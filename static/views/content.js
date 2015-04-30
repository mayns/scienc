var app = require('ampersand-app');
var View = require('ampersand-view');
var ViewSwitcher = require('ampersand-view-switcher');

var PageView = View.extend({
    initialize: function () {
        var self = this;

        app.router.on('newPage', function(view){
           self.pageSwitcher.set(view);
        });

        // init and configure our page switcher
        self.pageSwitcher = new ViewSwitcher(self.el, {
            show: function (newView, oldView) {
                // store an additional reference, just because
                app.views.active = newView;
            }
        });
    }
});

module.exports = PageView;