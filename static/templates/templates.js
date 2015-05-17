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
    templatizer["scientist_form"] = {};

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
        return '<div class="form form_type_signin"><div class="heading heading_level_beta">Log in</div><form class="js-form"><div class="form__section"><div class="input js-email"><input type="email" autofocus="autofocus" class="input__field"/><div data-hook="message-container" class="input__message-container"><div class="input__message-text">Поле обязательно для заполнения</div></div></div></div><div class="form__section"><div class="input js-password"><input type="password" class="input__field"/><div data-hook="message-container" class="input__message-container"><div class="input__message-text">Поле обязательно для заполнения</div></div></div></div><div class="form__section"><button type="submit" class="button button_type_submit">Войти</button></div></form><div><a href="/password_recover" class="link link_type_primary js-link">Восстановить пароль</a><a href="/signup" class="link link_type_primary js-link">Зарегистрироваться</a></div></div>';
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
        (function(projects, undefined) {
            buf.push('<div class="page__content">');
            (function() {
                var $obj = projects;
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
        }).call(this, "projects" in locals_for_with ? locals_for_with.projects : typeof projects !== "undefined" ? projects : undefined, "undefined" in locals_for_with ? locals_for_with.undefined : typeof undefined !== "undefined" ? undefined : undefined);
        return buf.join("");
    };

    // scientist_form/contacts.jade compiled template
    templatizer["scientist_form"]["contacts"] = function tmpl_scientist_form_contacts(locals) {
        var buf = [];
        var jade_mixins = {};
        var jade_interp;
        var locals_for_with = locals || {};
        (function(_id) {
            buf.push('<div class="row row_align_middle row_align_between"><label>Тип</label><input type="text" name="contacts[][connection]"/><label>Номер</label><input type="text" name="contacts[][number]"/><img' + jade.attr("data-_id", "" + _id + "", true, false) + ' data-type="contacts" src="/static/images/minus.svg" alt="" class="icon icon_size_small js-delete-item"/></div>');
        }).call(this, "_id" in locals_for_with ? locals_for_with._id : typeof _id !== "undefined" ? _id : undefined);
        return buf.join("");
    };

    // scientist_form/high_educations.jade compiled template
    templatizer["scientist_form"]["high_educations"] = function tmpl_scientist_form_high_educations(locals) {
        var buf = [];
        var jade_mixins = {};
        var jade_interp;
        var locals_for_with = locals || {};
        (function(model) {
            buf.push('<fieldset class="fieldset fieldset_nested"><div class="form__line row row_align_middle"><label class="col col_type_lg_size_4">Страна</label><input type="text" name="high_education[][country]" class="col col_type_lg_size_20"/></div><div class="form__line row row_align_middle"><label class="col col_type_lg_size_4 action">Город</label><input type="text" name="high_education[][city]" class="col col_type_lg_size_20"/></div><div class="form__line row row_align_middle"><label class="col col_type_lg_size_4 action">Университет</label><input type="text" name="high_education[][university]" class="col col_type_lg_size_20"/></div><div class="form__line row row_align_middle"><label class="col col_type_lg_size_4 action">Факультет</label><input type="text" name="high_education[][faculty]" class="col col_type_lg_size_20"/></div><div class="form__line row row_align_middle"><label class="col col_type_lg_size_4 action">Кафедра</label><input type="text" name="high_education[][chair]" class="col col_type_lg_size_20"/></div><div class="form__line row row_align_middle"><label for="high_education_degree" class="col col_type_lg_size_4 action">Степень</label><input type="text" name="high_education[][degree]" class="col col_type_lg_size_20"/></div><div class="form__line row row_align_middle"><label for="high_education_graduation_year" class="action col col_type_lg_size_4">Год выпуска</label><input type="number" name="high_education[][graduation_year]" class="col col_type_lg_size_4"/></div><img src="/static/images/minus.svg" alt=""' + jade.attr("data-_id", "" + model._id + "", true, false) + ' data-type="high_educations" class="icon icon_size_small js-delete-item"/></fieldset>');
        }).call(this, "model" in locals_for_with ? locals_for_with.model : typeof model !== "undefined" ? model : undefined);
        return buf.join("");
    };

    // scientist_form/main.jade compiled template
    templatizer["scientist_form"]["main"] = function tmpl_scientist_form_main(locals) {
        var buf = [];
        var jade_mixins = {};
        var jade_interp;
        var locals_for_with = locals || {};
        (function(formType, image_url) {
            buf.push('<div class="page__content"><form class="form js-form"><fieldset class="fieldset"><legend class="fieldset__heading">Общие сведения</legend><div class="row fieldset__block"><div class="col col_type_lg_size_16"><div class="form__line input js-first-name"><div class="row row_align_middle"><label for="scientist_first_name" class="col col_type_lg_size_8 input__label">Имя</label><input type="text" name="first_name" class="col col_type_lg_size_16 input__field"/></div><div class="row"><div data-hook="message-container" class="col col_type_lg_size_16 col_offset_type_lg_size_8 input__message-container"><div class="input__message input__message_type_error">Поле обязательно для заполнения</div></div></div></div><div class="form__line input js-last-name"><div class="row row_align_middle"><label for="scientist_last_name" class="col col_type_lg_size_8 input__label">Фамилия</label><input type="text" name="last_name" class="col col_type_lg_size_16 input__field"/></div><div class="row"><div data-hook="message-container" class="col col_type_lg_size_16 col_offset_type_lg_size_8 input__message-container"><div class="input__message input__message_type_error">Поле обязательно для заполнения</div></div></div></div><div class="form__line input js-middle-name"><div class="row row_align_middle"><label for="scientist_middle_name" class="col col_type_lg_size_8 input__label">Отчество</label><input type="text" name="middle_name" class="col col_type_lg_size_16 input__field"/></div><div class="row"><div data-hook="message-container" class="col col_type_lg_size_16 col_offset_type_lg_size_8 input__message-container"><div class="input__message input__message_type_error">Поле обязательно для заполнения</div></div></div></div><div class="form__line row row_align_between"><label class="col col_type_lg_size_8">Пол</label><div class="col col_type_lg_size_4"><div class="row row_align_middle row_align_between"><label for="male">М</label><input id="male" type="radio" value="m" name="gender" checked=""/><label for="female">Ж</label><input id="female" type="radio" value="f" name="gender" checked=""/></div></div></div><div class="form__line input js-middle-name"><div class="row row_align_middle"><label for="dateOfBirth" class="col col_type_lg_size_8 input__label">Дата рождения</label><input type="text" name="dob" class="col col_type_lg_size_16 input__field"/></div><div class="row"><div data-hook="message-container" class="col col_type_lg_size_16 col_offset_type_lg_size_8 input__message-container"><div class="input__message input__message_type_error">Неверный формат даты</div></div></div></div><div class="form__line input js-middle-name"><div class="row row_align_middle"><label for="placeOfLiving" class="col col_type_lg_size_8 input__label">Место проживания</label><input type="text" name="location[country]" class="col col_type_lg_size_7 input__field"/><input type="text" name="location[city]" class="col col_type_lg_size_8 input__field col_offset_type_lg_size_1"/></div></div></div><div class="col col_type_lg_size_8"><input-photo id="photo" size="{&quot;width&quot;: 250, &quot;height&quot;: 250}"' + jade.attr("imageuri", "" + image_url + "", true, false) + '></input-photo></div></div></fieldset><fieldset class="fieldset"><legend class="fieldset__heading">Сведения об образовании</legend><fieldset class="fieldset fieldset_nested"><legend class="fieldset__heading">Среднее образование</legend><fieldset class="fieldset fieldset_nested"><div class="form__line row row_align_middle"><label for="middle_education_country" class="col col_type_lg_size_4">Страна</label><input id="middle_education_country" type="text" name="middle_education[country]" class="col col_type_lg_size_20"/></div><div class="form__line row row_align_middle"><label for="middle_education_city" class="col col_type_lg_size_4">Город</label><input id="middle_education_city" type="text" name="middle_education[city]" class="col col_type_lg_size_20"/></div><div class="form__line row row_align_middle"><label for="middle_education_school" class="col col_type_lg_size_4">Школа</label><input id="middle_education_school" type="text" name="middle_education[school]" class="col col_type_lg_size_20"/></div><div class="form__line row row_align_middle"><label for="middle_education_graduation_year" class="col col_type_lg_size_4">Год выпуска</label><input id="middle_education_graduation_year" type="text" name="middle_education[graduation_year]" class="col col_type_lg_size_20"/></div></fieldset></fieldset><fieldset class="fieldset fieldset_nested"><legend class="fieldset__heading"><span>Высшее образование</span><img data-type="high_educations" src="/static/images/plus.svg" alt="" class="icon icon_size_small js-add-item"/></legend><div class="js-high-educations"></div></fieldset></fieldset><fieldset class="fieldset"><legend class="fieldset__heading">Научная деятельность</legend><fieldset class="fieldset fieldset_nested"><legend class="fieldset__heading"><span>Публикации</span><img data-type="publications" src="/static/images/plus.svg" alt="" class="icon icon_size_small js-add-item"/></legend><div class="js-publications"></div></fieldset><fieldset class="fieldset fieldset_nested"><legend class="fieldset__heading">О себе</legend><div class="row fieldset fieldset_nested"><textarea name="about" class="col col_type_lg_size_24"></textarea></div></fieldset><fieldset class="fieldset fieldset_nested"><legend class="fieldset__heading">Интересы</legend><div class="row"><input name="interests[]" class="col col_type_lg_size_24"/></div></fieldset></fieldset><fieldset class="fieldset"><legend class="fieldset__heading"><span>Контакты</span><img data-type="contacts" src="/static/images/plus.svg" alt="" class="icon icon_size_small js-add-item"/></legend><fieldset class="row fieldset fieldset_nested"><div class="col col_type_lg_size_16 js-contacts"></div></fieldset></fieldset>');
            if (formType === "create") {
                buf.push('<fieldset class="row fieldset"><div class="col col_type_lg_size_18"><div class="row row_align_middle"><label for="email" class="col col_type_lg_size_6">Email</label><input type="email" name="email" class="col col_type_lg_size_10"/></div><div class="row row_align_middle"><label for="pwd" class="col col_type_lg_size_6">Пароль</label><input type="password" name="pwd" class="col col_type_lg_size_10"/></div></div></fieldset>');
            }
            buf.push('<button type="submit" class="button button_type_submit">' + jade.escape(null == (jade_interp = formType === "create" ? "Создать" : "Сохранить") ? "" : jade_interp) + "</button></form></div>");
        }).call(this, "formType" in locals_for_with ? locals_for_with.formType : typeof formType !== "undefined" ? formType : undefined, "image_url" in locals_for_with ? locals_for_with.image_url : typeof image_url !== "undefined" ? image_url : undefined);
        return buf.join("");
    };

    // scientist_form/publications.jade compiled template
    templatizer["scientist_form"]["publications"] = function tmpl_scientist_form_publications(locals) {
        var buf = [];
        var jade_mixins = {};
        var jade_interp;
        var locals_for_with = locals || {};
        (function(model) {
            buf.push('<div class="fieldset fieldset_nested"><div class="form__line row row_align_middle"><label for="publicationName" class="col col_type_lg_size_6">Название</label><input type="text" name="publications[][title]" class="col col_type_lg_size_16"/></div><div class="form__line row row_align_middle"><label for="publishingHouse" class="col col_type_lg_size_6">Издательство</label><input type="text" name="publications[][source]" class="col col_type_lg_size_16"/></div><div class="form__line row row_align_middle"><label for="publicationYear" class="col col_type_lg_size_6">Год издания</label><input type="text" name="publications[][year]" class="col col_type_lg_size_16"/></div><div class="form__line row row_align_middle"><label for="publicationLink" class="col col_type_lg_size_6">Ссылка</label><input type="url" name="publications[][link]" class="col col_type_lg_size_16"/></div><img src="/static/images/minus.svg" alt=""' + jade.attr("data-_id", "" + model._id + "", true, false) + ' data-type="publications" class="icon icon_size_small js-delete-item"/></div>');
        }).call(this, "model" in locals_for_with ? locals_for_with.model : typeof model !== "undefined" ? model : undefined);
        return buf.join("");
    };

    // scientists.jade compiled template
    templatizer["scientists"] = function tmpl_scientists(locals) {
        var buf = [];
        var jade_mixins = {};
        var jade_interp;
        var locals_for_with = locals || {};
        (function(scientists, undefined) {
            buf.push('<div class="page__content">');
            (function() {
                var $obj = scientists;
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
        }).call(this, "scientists" in locals_for_with ? locals_for_with.scientists : typeof scientists !== "undefined" ? scientists : undefined, "undefined" in locals_for_with ? locals_for_with.undefined : typeof undefined !== "undefined" ? undefined : undefined);
        return buf.join("");
    };

    return templatizer;
}));