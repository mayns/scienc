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