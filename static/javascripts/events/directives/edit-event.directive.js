/**
* Event
* @namespace gestfg.events.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.events.directives')
    .directive('editEvent', editEvent);

  /**
  * @namespace editEvent
  */
  function editEvent() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.events.directives.editEvent
    */
    var directive = {
      controller: 'EventsController',
      controllerAs: 'vm',
      restrict: 'E',
      // scope: {
      //   event: '='
      // },
      templateUrl: '/static/templates/events/edit-event.html'
    };

    return directive;
  }
})();
