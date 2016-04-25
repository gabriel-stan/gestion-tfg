/**
* Events
* @namespace gestfg.events.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.events.directives')
    .directive('events', events);

  /**
  * @namespace Events
  */
  function events() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.events.directives.Events
    */
    var directive = {
      controller: 'EventsController',
      controllerAs: 'vm',
      restrict: 'E',
      scope: {
        posts: '='
      },
      templateUrl: '/static/templates/events/events.html'
    };

    return directive;
  }
})();
