/**
* Event
* @namespace gestfg.events.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.events.directives')
    .directive('event', event);

  /**
  * @namespace Event
  */
  function event() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.events.directives.Event
    */
    var directive = {
      controller: 'EventsController',
      controllerAs: 'vm',
      restrict: 'E',
      scope: {
        event: '='
      },
      templateUrl: '/static/templates/events/event.html'
    };

    return directive;
  }
})();
