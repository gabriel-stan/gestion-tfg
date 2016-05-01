/**
* DashboardController
* @namespace gestfg.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.layout.controllers')
    .controller('DashboardController', DashboardController);

  DashboardController.$inject = ['$scope', 'Authentication', 'Events', 'Snackbar'];

  /**
  * @namespace DashboardController
  */
  function DashboardController($scope, Authentication, Events, Snackbar) {
    var dashCtrl = this;

    dashCtrl.events = [];

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf gestfg.layout.controllers.DashboardController
    */
    function activate() {

      // cargar datos de relleno para la demo TODO quitar cuando no nos haga falta en el dashboard
      var s = document.createElement('script'); // use global document since Angular's $document is weak
      s.src = 'static/dist/js/pages/dashboard2.js';
      document.body.appendChild(s);

      Events.all().then(eventsSuccessFn, eventsErrorFn);
      //
      // $scope.$on('event.created', function (event, ev) {
      //   dashCtrl.events.unshift(ev);
      // });
      //
      // $scope.$on('event.created.error', function () {
      //   dashCtrl.events.shift();
      // });


      /**
      * @name eventsSuccessFn
      * @desc Update events array on view
      */
      function eventsSuccessFn(data, status, headers, config) {
        dashCtrl.events = data.data.data;
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
