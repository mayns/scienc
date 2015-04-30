var View = require('ampersand-view');
var templates = require('../templates/templates');

var AppBarView = View.extend({
    template: templates.appBar
});

module.exports = AppBarView;