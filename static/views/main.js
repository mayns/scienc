/*global app, me, $*/
// This app view is responsible for rendering all content that goes into
// <html>. It's initted right away and renders iteslf on DOM ready.

// This view also handles all the 'document' level events such as keyboard shortcuts.
var AmpersandView = require('ampersand-view');
var ViewSwitcher = require('ampersand-view-switcher');
var app = require('ampersand-app');

module.exports = AmpersandView.extend({
    initialize: function () {
        app.router.on('route', function(){
           console.log(arguments);
        });
        app.router.on('newPage', function(){
           console.log(arguments);
        });
        // init and configure our page switcher
        this.pageSwitcher = new ViewSwitcher(this.el, {
            show: function (newView, oldView) {
                // store an additional reference, just because
                app.views.active = newView;
            }
        });
    },
    setPage: function (view) {
        // tell the view switcher to render the new one
        this.pageSwitcher.set(view);
    }
});