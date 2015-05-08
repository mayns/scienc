var Model = require('ampersand-model');

var BaseModel = Model.extend({
	ajaxConfig: {
		headers: {
			"X-Requested-With": "XMLHttpRequest",
			"Access-Token": this.xsrf
		}
	}
});