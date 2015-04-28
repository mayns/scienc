/*global app, me, $*/
// This app view is responsible for rendering all content that goes into
// <html>. It's initted right away and renders iteslf on DOM ready.

// This view also handles all the 'document' level events such as keyboard shortcuts.
var AmpersandView = require('ampersand-view');
var ViewSwitcher = require('ampersand-view-switcher');
var app = require('ampersand-app');

var MainView = AmpersandView.extend({
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

module.exports = MainView;