/**
* DashboardController
* @namespace gestfg.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.layout.controllers')
    .controller('DashboardController', DashboardController);

  DashboardController.$inject = ['$scope', 'Authentication', 'Events', 'Snackbar', 'Dashboard'];

  /**
  * @namespace DashboardController
  */
  function DashboardController($scope, Authentication, Events, Snackbar, Dashboard) {
    var dashCtrl = this;

    dashCtrl.events = [];
    dashCtrl.upload = upload;

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf gestfg.layout.controllers.DashboardController
    */
    function activate() {

      // cargar datos de relleno para la demo TODO quitar cuando no nos haga falta en el dashboard
      try {
        var s = document.createElement('script'); // use global document since Angular's $document is weak
        s.src = 'static/dist/js/pages/dashboard2.js';
        document.body.appendChild(s);
      } catch (e) {
        console.log(e);
      }


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


    function upload(){
      var fd = new FormData();

      var f = document.getElementById('upload-file').files[0];

      fd.append('file', f);
      fd.append('model', dashCtrl.up.model);

      Dashboard.upload(fd).then(uploadSuccessFn, uploadErrorFn);


      function uploadSuccessFn(data, status, headers, config) {
        Snackbar.success("Subida realizada correctamente");
      }

      function uploadErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.message);
      }

      // var r = new FileReader();
      // r.onloadend = function(e){
      //   var data = e.target.result;
      //   dashCtrl.up.file = data;
      //   send you binary data via $http or $resource or do anything else with it
      // }
      // r.readAsBinaryString(f);
    }
  }
})();
