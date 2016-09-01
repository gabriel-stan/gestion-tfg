/**
* MainController
* @namespace gestfg.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.layout.controllers')
    .controller('MainController', MainController);

  MainController.$inject = ['$scope', '$location', 'Authentication', 'Events', 'Snackbar', 'Dashboard', 'Departamentos'];

  /**
  * @namespace MainController
  */
  function MainController($scope, $location, Authentication, Events, Snackbar, Dashboard, Departamentos) {
    var dashCtrl = this;

    $scope.$on('$viewContentLoaded', function(){
      //Here your view content is fully loaded !!
      //alert('loaded!');
      //console.log($location.path());
      //$( document ).trigger( 'ready' );

      var event; // The custom event that will be created

      if (document.createEvent) {
        event = document.createEvent("HTMLEvents");
        event.initEvent($location.path(), true, true);
      } else {
        event = document.createEventObject();
        event.eventType = $location.path();
      }

      event.eventName = $location.path();

      if (document.createEvent) {
        document.dispatchEvent(event);
      } else {
        document.fireEvent("on" + event.eventType, event);
      }
    });

  }
})();
