var Model = require('ampersand-model');
var app = require('ampersand-app');

var BaseModel = Model.extend({
	ajaxConfig: function() {

		return {
			headers: {
				"X-Requested-With": "XMLHttpRequest",
				"Access-Token": app.user && app.user.xsrf
			}
		}
	}

});

module.exports = BaseModel;