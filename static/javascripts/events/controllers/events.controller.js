/**
* EventsController
* @namespace gestfg.events.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.events.controllers')
    .controller('EventsController', EventsController);

  EventsController.$inject = ['$scope', '$rootScope', 'Events', 'Snackbar'];

  /**
  * @namespace EventsController
  */
  function EventsController($scope, $rootScope, Events, Snackbar) {

    var eventsCtrl = this;

    $scope.editEvent = edit;
    $scope.removeEvent = remove;

    $rootScope.selectedEvent = new Object();

    eventsCtrl.parseTimeAgo = function(fecha){
      // console.log(fecha);

      var fecha = new Date(fecha);
      fecha = moment(fecha).fromNow();

      return fecha;
    }


    eventsCtrl.parseTime = function(fecha){
      // console.log(fecha);

      var fecha = new Date(fecha);
      fecha = moment(fecha).format("DD/MM/YYYY - hh:mm");

      return fecha;
    }

    $scope.loadSelectedEvent = function(evento) {
      $rootScope.selectedEvent = evento;
      $('iframe').contents().find('.wysihtml5-editor').html(evento.contenido);

      var fechas = $('#fechas').data('daterangepicker');

      if(evento.desde){
        fechas.setStartDate(new Date(evento.desde));
      }

      if(evento.hasta){
        fechas.setEndDate(new Date(evento.hasta));
      }

    }

    // eventsCtrl.columns = [];

    activate();


    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf gestfg.events.controllers.EventsController
    */
    function activate() {
      //$scope.$watchCollection(function () { return $scope.events; }, render);
      // $scope.$watch(function () { return $(window).width(); }, render);
    }


    /**
    * @name remove
    * @desc Deletes an event
    * @memberOf gestfg.events.controllers.EventsController
    */
    function remove(eventID) {

      if (confirm('¿Borrar el evento?')) {
        Events.remove(eventID).then(EventsSuccessFn, EventsErrorFn);
      }


      /**
      * @name EventsSuccessFn
      * @desc Update events array on view
      */
      function EventsSuccessFn(data, status, headers, config) {
        Snackbar.success("El evento se ha eliminado con exito");
      }


      /**
      * @name EventsErrorFn
      * @desc Show snackbar with error
      */
      function EventsErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.error);
      }
    }


    /**
    * @name edit
    * @desc Edit an event
    * @memberOf gestfg.events.controllers.EventsController
    */
    function edit(event) {

      alert('por hacer: events.controller.js');

      // if (confirm('¿Borrar el evento?')) {
      //   Events.remove(eventID).then(EventsSuccessFn, EventsErrorFn);
      // }


      /**
      * @name EventsSuccessFn
      * @desc Update events array on view
      */
      function EventsSuccessFn(data, status, headers, config) {
        Snackbar.success("Los cambios se han guardado con exito");
      }


      /**
      * @name EventsErrorFn
      * @desc Show snackbar with error
      */
      function EventsErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.error);
      }
    }

    function preAction(){
      $scope.loading = true;
    }

    function postAction(){
      $scope.loading = false;
    }

  }
})();
