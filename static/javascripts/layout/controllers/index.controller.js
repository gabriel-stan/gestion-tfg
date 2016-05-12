/**
* IndexController
* @namespace gestfg.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.layout.controllers')
    .controller('IndexController', IndexController);

  IndexController.$inject = ['$scope', 'Authentication', 'Events', 'Snackbar'];

  /**
  * @namespace IndexController
  */
  function IndexController($scope, Authentication, Events, Snackbar) {
    var indexCtrl = this;

    indexCtrl.isAuthenticated = Authentication.isAuthenticated();
    indexCtrl.isAdmin = Authentication.isAdmin();
    indexCtrl.events = [];

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf gestfg.layout.controllers.IndexController
    */
    function activate() {
      Events.all().then(eventsSuccessFn, eventsErrorFn);

      $scope.$on('event.created', function (event, ev) {
        indexCtrl.events.unshift(ev);
      });

      $scope.$on('event.created.error', function () {
        indexCtrl.events.shift();
      });


      /**
      * @name eventsSuccessFn
      * @desc Update events array on view
      */
      function eventsSuccessFn(data, status, headers, config) {
        indexCtrl.events = data.data.data;
      }


      /**
      * @name eventsErrorFn
      * @desc Show snackbar with error
      */
      function eventsErrorFn(data, status, headers, config) {
        Snackbar.error(data.error);
      }
    }
  }
})();
