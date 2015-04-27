var AmpersandView = require('ampersand-view');
var dom = require('ampersand-dom');
var templates = require('../templates/templates');

var AppBarView = AmpersandView.extend({
    template: templates.appBar
});

module.exports = AppBarView;