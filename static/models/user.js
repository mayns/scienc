var Model = require('ampersand-model');

var User = Model.extend({
    initialize: function() {
        this.fetch();
    },
    urlRoot: '/api/user',
    props: {
        id: 'number',
        image_url: 'string',
        desired_vacancies: 'array',
        liked_projects: 'array',
        managing_project_ids: 'array'
    }
});

module.exports = User;

//desired_vacancies: []
//id: 2
//image_url: "https://en.gravatar.com/userimage/39116033/0b1c1ef31de9d584943a47db3a03143a.jpg?size=60"
//liked_projects: []
//managing_project_ids: [1]