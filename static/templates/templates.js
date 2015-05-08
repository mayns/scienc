(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof exports === 'object') {
        module.exports = factory();
    } else if (typeof root === 'undefined' || root !== Object(root)) {
        throw new Error('templatizer: window does not exist or is not an object');
    } else {
        root.templatizer = factory();
    }
}(this, function () {
    var jade=function(){function e(e){return null!=e&&""!==e}function n(t){return(Array.isArray(t)?t.map(n):t&&"object"==typeof t?Object.keys(t).filter(function(e){return t[e]}):[t]).filter(e).join(" ")}var t={};return t.merge=function r(n,t){if(1===arguments.length){for(var a=n[0],i=1;i<n.length;i++)a=r(a,n[i]);return a}var o=n["class"],s=t["class"];(o||s)&&(o=o||[],s=s||[],Array.isArray(o)||(o=[o]),Array.isArray(s)||(s=[s]),n["class"]=o.concat(s).filter(e));for(var l in t)"class"!=l&&(n[l]=t[l]);return n},t.joinClasses=n,t.cls=function(e,r){for(var a=[],i=0;i<e.length;i++)a.push(r&&r[i]?t.escape(n([e[i]])):n(e[i]));var o=n(a);return o.length?' class="'+o+'"':""},t.style=function(e){return e&&"object"==typeof e?Object.keys(e).map(function(n){return n+":"+e[n]}).join(";"):e},t.attr=function(e,n,r,a){return"style"===e&&(n=t.style(n)),"boolean"==typeof n||null==n?n?" "+(a?e:e+'="'+e+'"'):"":0==e.indexOf("data")&&"string"!=typeof n?(-1!==JSON.stringify(n).indexOf("&")&&console.warn("Since Jade 2.0.0, ampersands (`&`) in data attributes will be escaped to `&amp;`"),n&&"function"==typeof n.toISOString&&console.warn("Jade will eliminate the double quotes around dates in ISO form after 2.0.0")," "+e+"='"+JSON.stringify(n).replace(/'/g,"&apos;")+"'"):r?(n&&"function"==typeof n.toISOString&&console.warn("Jade will stringify dates in ISO form after 2.0.0")," "+e+'="'+t.escape(n)+'"'):(n&&"function"==typeof n.toISOString&&console.warn("Jade will stringify dates in ISO form after 2.0.0")," "+e+'="'+n+'"')},t.attrs=function(e,r){var a=[],i=Object.keys(e);if(i.length)for(var o=0;o<i.length;++o){var s=i[o],l=e[s];"class"==s?(l=n(l))&&a.push(" "+s+'="'+l+'"'):a.push(t.attr(s,l,!1,r))}return a.join("")},t.escape=function(e){var n=String(e).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");return n===""+e?e:n},t.rethrow=function a(e,n,t,r){if(!(e instanceof Error))throw e;if(!("undefined"==typeof window&&n||r))throw e.message+=" on line "+t,e;try{r=r||require("fs").readFileSync(n,"utf8")}catch(i){a(e,null,t)}var o=3,s=r.split("\n"),l=Math.max(t-o,0),f=Math.min(s.length,t+o),o=s.slice(l,f).map(function(e,n){var r=n+l+1;return(r==t?"  > ":"    ")+r+"| "+e}).join("\n");throw e.path=n,e.message=(n||"Jade")+":"+t+"\n"+o+"\n\n"+e.message,e},t}(); 

    var templatizer = {};


    // appbar.jade compiled template
    templatizer["appbar"] = function tmpl_appbar(locals) {
        var buf = [];
        var jade_mixins = {};
        var jade_interp;
        var locals_for_with = locals || {};
        (function(id, image_url) {
            buf.push('<div class="appbar">');
            if (id) {
                buf.push('<a href="/project" class="link js-link"><img src="/static/images/add_project.svg" class="appbar__icon appbar__icon-add"/></a><a href="/scientist/my-projects" class="link js-link"><img src="/static/images/favorite.svg" class="appbar__icon appbar__icon-fav"/></a><a href="/scientists" class="link js-link"><img src="/static/images/members.svg" class="appbar__icon appbar__icon-members"/></a><a' + jade.attr("href", "/scientist/" + id + "", true, false) + ' class="link js-link"><img' + jade.attr("src", "" + image_url + "", true, false) + ' class="appbar__icon appbar__icon-scientist"/></a><a href="/search" class="link js-link"><img src="/static/images/search.svg" class="appbar__icon appbar__icon-search"/></a><div id="signOut"><img src="/static/images/logout.svg" class="appbar__icon appbar__icon-logout"/></div>');
            } else {
                buf.push('<a href="/scientists" class="link js-link"><img src="/static/images/members.svg" class="appbar__icon appbar__icon-members"/></a><div id="signIn"><img src="/static/images/login.svg" class="appbar__icon appbar__icon-login"/></div><a href="/signup" class="link js-link"><img src="/static/images/register.svg" class="appbar__icon appbar__icon-register"/></a><a href="/search" class="link js-link"><img src="/static/images/search.svg" class="appbar__icon appbar__icon-search"/></a>');
            }
            buf.push("</div>");
        }).call(this, "id" in locals_for_with ? locals_for_with.id : typeof id !== "undefined" ? id : undefined, "image_url" in locals_for_with ? locals_for_with.image_url : typeof image_url !== "undefined" ? image_url : undefined);
        return buf.join("");
    };

    // login_modal.jade compiled template
    templatizer["login_modal"] = function tmpl_login_modal() {
        return '<div class="form form_type_signin"><div class="heading heading_level_beta">Log in</div><form action="/api/login/"><div class="form__section"><div class="input js-email"><input type="email" autofocus="autofocus" class="input__field"/><div data-hook="message-container" class="input__message-container"><div class="input__message-text">Поле обязательно для заполнения</div></div></div></div><div class="form__section"><div class="input js-password"><input type="password" class="input__field"/><div data-hook="message-container" class="input__message-container"><div class="input__message-text">Поле обязательно для заполнения</div></div></div></div><div class="form__section"><button type="submit" class="button button_type_submit">Войти</button></div></form><div><a href="/password_recover" class="link link_type_primary js-link">Восстановить пароль</a><a href="/signup" class="link link_type_primary js-link">Зарегистрироваться</a></div></div>';
    };

    // modal.jade compiled template
    templatizer["modal"] = function tmpl_modal() {
        return '<div data-hook="overlay" class="modal__overlay"><div tabindex="0" class="modal__body js-modal__body"><button data-hook="close" class="modal__close">X</button><div data-hook="content" class="modal__content"></div></div></div>';
    };

    // projects.jade compiled template
    templatizer["projects"] = function tmpl_projects(locals) {
        var buf = [];
        var jade_mixins = {};
        var jade_interp;
        var locals_for_with = locals || {};
        (function(data, undefined) {
            buf.push('<div class="page__content">');
            (function() {
                var $obj = data;
                if ("number" == typeof $obj.length) {
                    for (var $index = 0, $l = $obj.length; $index < $l; $index++) {
                        var project = $obj[$index];
                        buf.push('<article class="project"><h1 class="project__header"><a' + jade.attr("href", "/project/" + project.id + "", true, false) + ' class="link js-link">' + jade.escape(null == (jade_interp = project.title) ? "" : jade_interp) + '</a></h1><div class="project__holders">');
                        (function() {
                            var $obj = project.university_connection;
                            if ("number" == typeof $obj.length) {
                                for (var $index = 0, $l = $obj.length; $index < $l; $index++) {
                                    var connection = $obj[$index];
                                    buf.push('<span class="project__holder">' + jade.escape(null == (jade_interp = connection.university) ? "" : jade_interp) + "</span>");
                                }
                            } else {
                                var $l = 0;
                                for (var $index in $obj) {
                                    $l++;
                                    var connection = $obj[$index];
                                    buf.push('<span class="project__holder">' + jade.escape(null == (jade_interp = connection.university) ? "" : jade_interp) + "</span>");
                                }
                            }
                        }).call(this);
                        buf.push('</div><p class="project__description"><span class="project__description-header">Краткое описание:&nbsp;</span><span>' + jade.escape(null == (jade_interp = project.description_short) ? "" : jade_interp) + "</span></p><div><div>");
                        (function() {
                            var $obj = project.research_fields;
                            if ("number" == typeof $obj.length) {
                                for (var $index = 0, $l = $obj.length; $index < $l; $index++) {
                                    var field = $obj[$index];
                                    buf.push('<span class="science-field-item row-flex middle"><img' + jade.attr("src", "/static/images/" + field.id + ".svg", true, false) + ' class="icon"/></span>');
                                }
                            } else {
                                var $l = 0;
                                for (var $index in $obj) {
                                    $l++;
                                    var field = $obj[$index];
                                    buf.push('<span class="science-field-item row-flex middle"><img' + jade.attr("src", "/static/images/" + field.id + ".svg", true, false) + ' class="icon"/></span>');
                                }
                            }
                        }).call(this);
                        buf.push('</div><div class="row-flex middle"><div style="margin-right: 10px; font-size: 26px; color: #808080"></div></div></div></article>');
                    }
                } else {
                    var $l = 0;
                    for (var $index in $obj) {
                        $l++;
                        var project = $obj[$index];
                        buf.push('<article class="project"><h1 class="project__header"><a' + jade.attr("href", "/project/" + project.id + "", true, false) + ' class="link js-link">' + jade.escape(null == (jade_interp = project.title) ? "" : jade_interp) + '</a></h1><div class="project__holders">');
                        (function() {
                            var $obj = project.university_connection;
                            if ("number" == typeof $obj.length) {
                                for (var $index = 0, $l = $obj.length; $index < $l; $index++) {
                                    var connection = $obj[$index];
                                    buf.push('<span class="project__holder">' + jade.escape(null == (jade_interp = connection.university) ? "" : jade_interp) + "</span>");
                                }
                            } else {
                                var $l = 0;
                                for (var $index in $obj) {
                                    $l++;
                                    var connection = $obj[$index];
                                    buf.push('<span class="project__holder">' + jade.escape(null == (jade_interp = connection.university) ? "" : jade_interp) + "</span>");
                                }
                            }
                        }).call(this);
                        buf.push('</div><p class="project__description"><span class="project__description-header">Краткое описание:&nbsp;</span><span>' + jade.escape(null == (jade_interp = project.description_short) ? "" : jade_interp) + "</span></p><div><div>");
                        (function() {
                            var $obj = project.research_fields;
                            if ("number" == typeof $obj.length) {
                                for (var $index = 0, $l = $obj.length; $index < $l; $index++) {
                                    var field = $obj[$index];
                                    buf.push('<span class="science-field-item row-flex middle"><img' + jade.attr("src", "/static/images/" + field.id + ".svg", true, false) + ' class="icon"/></span>');
                                }
                            } else {
                                var $l = 0;
                                for (var $index in $obj) {
                                    $l++;
                                    var field = $obj[$index];
                                    buf.push('<span class="science-field-item row-flex middle"><img' + jade.attr("src", "/static/images/" + field.id + ".svg", true, false) + ' class="icon"/></span>');
                                }
                            }
                        }).call(this);
                        buf.push('</div><div class="row-flex middle"><div style="margin-right: 10px; font-size: 26px; color: #808080"></div></div></div></article>');
                    }
                }
            }).call(this);
            buf.push("</div>");
        }).call(this, "data" in locals_for_with ? locals_for_with.data : typeof data !== "undefined" ? data : undefined, "undefined" in locals_for_with ? locals_for_with.undefined : typeof undefined !== "undefined" ? undefined : undefined);
        return buf.join("");
    };

    // scientist_form.jade compiled template
    templatizer["scientist_form"] = function tmpl_scientist_form(locals) {
        var buf = [];
        var jade_mixins = {};
        var jade_interp;
        var locals_for_with = locals || {};
        (function(dob, first_name, image_url, last_name, location, middle_name) {
            buf.push('<div class="page__content"><form id="form" redirect="/scientists" action="/api/scientists" class="scientist-modify"><fieldset class="fieldset"><legend class="fieldset__header">Общие сведения</legend><div class="row fieldset__block"><div class="col col_size_lg_num_8"><div class="row middle"><label for="first_name" class="action col-lg-4">Имя</label><input id="first_name" type="text" name="first_name"' + jade.attr("value", "" + first_name + "", true, false) + ' class="col-lg-8"/></div><div class="row middle"><label for="last_name" class="action col-lg-4">Фамилия</label><input id="last_name" type="text" name="last_name"' + jade.attr("value", "" + last_name + "", true, false) + ' class="col-lg-8"/></div><div class="row middle"><label for="middlename" class="action col-lg-4">Отчество</label><input id="middlename" type="text" name="middle_name"' + jade.attr("value", "" + middle_name + "", true, false) + ' class="col-lg-8"/></div><div class="row middle"><label class="col-lg-4">Пол</label><div class="col-lg-2"><div class="row-flex middle between"><label for="male">М</label><input id="male" type="radio" value="m" name="gender" checked="{{ gender === \'m\' ? \'checked\' : \'\' }}"/><label for="female">Ж</label><input id="female" type="radio" value="f" name="gender" checked="{{ gender === \'f\' ? \'checked\' : \'\' }}"/></div></div></div><div class="row middle"><label for="dateOfBirth" class="col-lg-4">Дата рождения</label><input id="dateOfBirth" type="text"' + jade.attr("value", "" + dob + "", true, false) + ' name="dob"/></div><div class="row middle"><label for="placeOfLiving" class="col-lg-4">Место проживания</label><div class="col-lg-8"><div class="row between"><input id="placeOfLiving" type="text"' + jade.attr("value", "" + location.country + "", true, false) + ' name="location[country]" placeholder="Страна"/><input type="text"' + jade.attr("value", "" + location.city + "", true, false) + ' name="location[city]" placeholder="Город"/></div></div></div></div><div class="col-lg-4"><input-photo id="photo" size="{&quot;width&quot;: 250, &quot;height&quot;: 250}"' + jade.attr("imageuri", "" + image_url + "", true, false) + '></input-photo></div></div></fieldset><fieldset class="fieldset"><legend>Сведения об образовании</legend><div class="fieldblock"><fieldset><legend>Среднее образование</legend><div class="fieldblock"><div class="row-flex middle"><label for="middle_education_country" class="col-lg-2 action">Страна</label><input id="middle_education_country" type="text" value="{{ middle_education.country }}" data-json="middle_education[country]" class="col-lg-10"/></div><div class="row-flex middle"><label for="middle_education_city" class="col-lg-2">Город</label><input id="middle_education_city" type="text" value="{{ middle_education.city }}" data-json="middle_education[city]" class="col-lg-10"/></div><div class="row-flex middle"><label for="middle_education_school" class="col-lg-2">Школа</label><input id="middle_education_school" type="text" value="{{ middle_education.school }}" data-json="middle_education[school]" class="col-lg-10"/></div><div class="row-flex middle"><label for="middle_education_graduation_year" class="action col-lg-2">Год выпуска</label><input id="middle_education_graduation_year" type="text" value="{{ middle_education.graduation_year }}" data-json="middle_education[graduation_year]" class="col-lg-2"/></div></div></fieldset><fieldset><legend><span>Высшее образование</span><img on-click="{{ addItem }}" data-itemtype="high_education" src="/static/images/plus.svg" alt="" class="action icon"/></legend><template repeat="{{ high_education }}"><div class="fieldblock"><div class="row-flex middle"><label class="col-lg-2 action">Страна</label><input type="text" value="{{ country }}" data-json="high_education[][country]" class="col-lg-10"/></div><div class="row-flex middle"><label class="col-lg-2 action">Город</label><input type="text" value="{{ city }}" data-json="high_education[][city]" class="col-lg-10"/></div><div class="row-flex middle"><label class="col-lg-2 action">Университет</label><input type="text" value="{{ university }}" data-json="high_education[][university]" class="col-lg-10"/></div><div class="row-flex middle"><label class="col-lg-2 action">Факультет</label><input type="text" value="{{ faculty }}" data-json="high_education[][faculty]" class="col-lg-10"/></div><div class="row-flex middle"><label class="col-lg-2 action">Кафедра</label><input type="text" value="{{ chair }}" data-json="high_education[][chair]" class="col-lg-10"/></div><div class="row-flex middle"><label for="high_education_degree" class="col-lg-2 action">Степень</label><input id="high_education_degree" type="text" value="{{ degree }}" data-json="high_education[][degree]" class="col-lg-10"/></div><div class="row-flex middle"><label for="high_education_graduation_year" class="action col-lg-2">Год выпуска</label><input id="high_education_graduation_year" type="number" value="{{ graduation_year }}" data-json="high_education[][graduation_year]" class="col-lg-2"/></div><img data-itemtype="high_education" on-click="{{ deleteItem }}" src="/static/images/minus.svg" alt="" class="deleteItem icon action"/></div></template></fieldset></div></fieldset><fieldset><legend>Научная деятельность</legend><div class="fieldblock"><fieldset><legend><span>Публикации</span><img on-click="{{ addItem }}" data-itemtype="publications" src="/static/images/plus.svg" alt="" class="action icon"/></legend><template repeat="{{ publications }}"><div class="fieldblock"><div class="row-flex middle"><label for="publicationName" class="action col-lg-3">Название</label><input type="text" data-json="publications[][title]" value="{{ title }}" class="col-lg-8"/></div><div class="row-flex middle"><label for="publishingHouse" class="action col-lg-3">Издательство</label><input type="text" data-json="publications[][source]" value="{{ source }}" class="col-lg-8"/></div><div class="row-flex middle"><label for="publicationYear" class="action col-lg-3">Год издания</label><input type="text" data-json="publications[][year]" value="{{ year }}" class="col-lg-8"/></div><div class="row-flex middle"><label for="publicationLink" class="col-lg-3 action">Ссылка</label><input type="url" data-json="publications[][link]" value="{{ link }}" class="col-lg-8"/></div><img data-itemtype="publications" on-click="{{ deleteItem }}" src="/static/images/minus.svg" alt="" class="deleteItem icon action"/></div></template></fieldset><fieldset><legend>О себе</legend><div class="fieldblock row-flex"><textarea id="about" data-json="about" value="{{ about }}" class="col-lg-12"></textarea></div></fieldset><fieldset><legend>Сфера научных интересов</legend><div class="fieldblock"><input-tags id="science_interests" data-json="interests[]" value="{{ interests }}" class="col-lg-12"></input-tags></div></fieldset></div></fieldset><fieldset><legend><span>Контакты</span><img on-click="{{ addItem }}" data-itemtype="contacts" src="/static/images/plus.svg" alt="" class="action icon"/></legend><div class="fieldblock"><div class="col-lg-8"><template repeat="{{ contacts }}"><div class="row-flex middle between"><label class="action">Тип</label><input type="text" data-json="contacts[][connection]" value="{{ connection }}"/><label class="action">Номер</label><input type="text" data-json="contacts[][number]" value="{{ number }}"/><img on-click="{{ deleteItem }}" data-itemtype="contacts" src="/static/images/minus.svg" alt="" class="action icon"/></div></template></div></div></fieldset></form><template if="{{ viewType === \'create\' }}"><fieldset><div class="row-flex fieldblock"><div class="col-lg-9"><div class="row-flex middle"><label for="email" class="col-lg-3">Email</label><input id="email" type="email" data-json="email" required="" class="col-lg-5"/></div><div class="row-flex middle"><label for="pwd" class="col-lg-3">Пароль</label><input id="pwd" type="password" data-json="pwd" required="" class="col-lg-5"/></div></div></div></fieldset></template><template if="{{ viewType === \'update\' }}"><input type="hidden" value="{{ data.id }}" data-json="scientist_id"/></template><div class="row-flex center"><button type="submit" class="button submit">{{ viewType === \'create\' ? \'Вступаю\' : \'Сохранить\' }}</button></div></div>');
        }).call(this, "dob" in locals_for_with ? locals_for_with.dob : typeof dob !== "undefined" ? dob : undefined, "first_name" in locals_for_with ? locals_for_with.first_name : typeof first_name !== "undefined" ? first_name : undefined, "image_url" in locals_for_with ? locals_for_with.image_url : typeof image_url !== "undefined" ? image_url : undefined, "last_name" in locals_for_with ? locals_for_with.last_name : typeof last_name !== "undefined" ? last_name : undefined, "location" in locals_for_with ? locals_for_with.location : typeof location !== "undefined" ? location : undefined, "middle_name" in locals_for_with ? locals_for_with.middle_name : typeof middle_name !== "undefined" ? middle_name : undefined);
        return buf.join("");
    };

    // scientists.jade compiled template
    templatizer["scientists"] = function tmpl_scientists(locals) {
        var buf = [];
        var jade_mixins = {};
        var jade_interp;
        var locals_for_with = locals || {};
        (function(data, undefined) {
            buf.push('<div class="page__content">');
            (function() {
                var $obj = data;
                if ("number" == typeof $obj.length) {
                    for (var $index = 0, $l = $obj.length; $index < $l; $index++) {
                        var scientist = $obj[$index];
                        buf.push('<div class="scientist-thumb"><div class="scientist-thumb__photo-block"><img' + jade.attr("src", "" + scientist.image_url + "", true, false) + ' class="scientist-thumb__photo"/></div><div class="scientist-thumb__details-block"><a' + jade.attr("href", "/scientist/" + scientist.id + "", true, false) + ' class="link js-link scientist-thumb__name">' + jade.escape(null == (jade_interp = scientist.full_name) ? "" : jade_interp) + '</a><div class="scientist-thumb__education">' + jade.escape(null == (jade_interp = scientist.location) ? "" : jade_interp) + '</div><div class="scientist-thumb__projects"><span class="scientist-thumb__project-label">Проектов</span><span class="scientist-thumb__project-count">' + jade.escape(null == (jade_interp = scientist.projects) ? "" : jade_interp) + "</span></div></div></div>");
                    }
                } else {
                    var $l = 0;
                    for (var $index in $obj) {
                        $l++;
                        var scientist = $obj[$index];
                        buf.push('<div class="scientist-thumb"><div class="scientist-thumb__photo-block"><img' + jade.attr("src", "" + scientist.image_url + "", true, false) + ' class="scientist-thumb__photo"/></div><div class="scientist-thumb__details-block"><a' + jade.attr("href", "/scientist/" + scientist.id + "", true, false) + ' class="link js-link scientist-thumb__name">' + jade.escape(null == (jade_interp = scientist.full_name) ? "" : jade_interp) + '</a><div class="scientist-thumb__education">' + jade.escape(null == (jade_interp = scientist.location) ? "" : jade_interp) + '</div><div class="scientist-thumb__projects"><span class="scientist-thumb__project-label">Проектов</span><span class="scientist-thumb__project-count">' + jade.escape(null == (jade_interp = scientist.projects) ? "" : jade_interp) + "</span></div></div></div>");
                    }
                }
            }).call(this);
            buf.push("</div>");
        }).call(this, "data" in locals_for_with ? locals_for_with.data : typeof data !== "undefined" ? data : undefined, "undefined" in locals_for_with ? locals_for_with.undefined : typeof undefined !== "undefined" ? undefined : undefined);
        return buf.join("");
    };

    return templatizer;
}));