var templates = {};
templates._runtime = require('domthing/runtime');
templates['projects'] = function (context, runtime) {
  runtime = runtime || this._runtime;
  var template = new runtime.Template();

  (function (parent) {
    (function (parent) {
      var element = document.createElement('div');
      var expr;
      (function (parent) {
        (function (parent) {
          var expr = (
            runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
          );
          var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
          expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
          parent.appendChild(node);
        })(parent);
        runtime.hooks.HELPER('data', [
          parent,
          context,
          (
            runtime.hooks.EVENTIFY_BINDING.call(template, context, '')
          ),
          function (parent) {
            (function (parent) {
              var expr = (
                runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
              );
              var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
              expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
              parent.appendChild(node);
            })(parent);
            (function (parent) {
              var element = document.createElement('article');
              var expr;
              element.setAttribute('class', 'project');
              (function (parent) {
                (function (parent) {
                  var expr = (
                    runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
                  );
                  var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
                  expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
                  parent.appendChild(node);
                })(parent);
                (function (parent) {
                  var element = document.createElement('header');
                  var expr;
                  element.setAttribute('class', 'project-header');
                  (function (parent) {
                    (function (parent) {
                      var expr = (
                        runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
                      );
                      var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
                      expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
                      parent.appendChild(node);
                    })(parent);
                    (function (parent) {
                      var element = document.createElement('h1');
                      var expr;
                      (function (parent) {
                        (function (parent) {
                          var expr = (
                            runtime.hooks.EVENTIFY_LITERAL.call(template, " Заголовок ")
                          );
                          var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
                          expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
                          parent.appendChild(node);
                        })(parent);
                      })(element);
                      parent.appendChild(element);
                    })(parent);
                    (function (parent) {
                      var expr = (
                        runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
                      );
                      var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
                      expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
                      parent.appendChild(node);
                    })(parent);
                    (function (parent) {
                      var element = document.createElement('div');
                      var expr;
                      (function (parent) {
                        (function (parent) {
                          var expr = (
                            runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
                          );
                          var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
                          expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
                          parent.appendChild(node);
                        })(parent);
                        (function (parent) {
                          var element = document.createElement('div');
                          var expr;
                          (function (parent) {
                            (function (parent) {
                              var expr = (
                                runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
                              );
                              var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
                              expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
                              parent.appendChild(node);
                            })(parent);
                          })(element);
                          parent.appendChild(element);
                        })(parent);
                        (function (parent) {
                          var expr = (
                            runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
                          );
                          var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
                          expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
                          parent.appendChild(node);
                        })(parent);
                      })(element);
                      parent.appendChild(element);
                    })(parent);
                    (function (parent) {
                      var expr = (
                        runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
                      );
                      var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
                      expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
                      parent.appendChild(node);
                    })(parent);
                  })(element);
                  parent.appendChild(element);
                })(parent);
                (function (parent) {
                  var expr = (
                    runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
                  );
                  var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
                  expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
                  parent.appendChild(node);
                })(parent);
                (function (parent) {
                  var element = document.createElement('p');
                  var expr;
                  (function (parent) {
                    (function (parent) {
                      var expr = (
                        runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
                      );
                      var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
                      expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
                      parent.appendChild(node);
                    })(parent);
                    (function (parent) {
                      var element = document.createElement('span');
                      var expr;
                      element.setAttribute('class', 'short-descr');
                      (function (parent) {
                        (function (parent) {
                          var expr = (
                            runtime.hooks.EVENTIFY_LITERAL.call(template, "Краткое описание: ")
                          );
                          var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
                          expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
                          parent.appendChild(node);
                        })(parent);
                      })(element);
                      parent.appendChild(element);
                    })(parent);
                    (function (parent) {
                      var expr = (
                        runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
                      );
                      var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
                      expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
                      parent.appendChild(node);
                    })(parent);
                  })(element);
                  parent.appendChild(element);
                })(parent);
                (function (parent) {
                  var expr = (
                    runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
                  );
                  var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
                  expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
                  parent.appendChild(node);
                })(parent);
              })(element);
              parent.appendChild(element);
            })(parent);
            (function (parent) {
              var expr = (
                runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
              );
              var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
              expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
              parent.appendChild(node);
            })(parent);
          },
          function (parent) {
        }]);
        (function (parent) {
          var expr = (
            runtime.hooks.EVENTIFY_LITERAL.call(template, " ")
          );
          var node = document.createTextNode((expr.value||expr.value===0) ? expr.value : '');
          expr.on('change', function (text) { node.data = (text||text===0) ? text : ''; });
          parent.appendChild(node);
        })(parent);
      })(element);
      parent.appendChild(element);
    })(parent);
  })(template.html);
  var firstChild = template.html.firstChild;
  firstChild.update = template.update.bind(template);
  return firstChild;
}.bind(templates);
module.exports = templates;