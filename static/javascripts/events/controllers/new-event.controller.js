/**
* NewEventController
* @namespace gestfg.events.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.events.controllers')
    .controller('NewEventController', NewEventController);

  NewEventController.$inject = ['$rootScope', '$scope', 'Authentication', 'Snackbar', 'Events'];

  /**
  * @namespace NewEventController
  */
  function NewEventController($rootScope, $scope, Authentication, Snackbar, Events) {
    var newEventCtrl = this;

    newEventCtrl.submit = submit;

    $scope.submit = submit;

    var contenido = $("#wysihtml5-editor").val();

    /**
    * @name submit
    * @desc Create a new Event
    * @memberOf gestfg.events.controllers.NewEventController
    */
    function submit() {

      // recogemos el contenido del wysihtml5 editor
      newEventCtrl.event.contenido = $("#wysihtml5-editor").val();

      // newEventCtrl.event.tipo = newEventCtrl.event.tipo.codigo;
      newEventCtrl.event.convocatoria = newEventCtrl.event.tipo.codigo;
      if(newEventCtrl.event.convocatoria && newEventCtrl.event.convocatoria != 'INFOR'){
        newEventCtrl.event.tipo = newEventCtrl.event.sub_tipo.codigo;

        var fechas = $('#fechas').data('daterangepicker');
        // newEventCtrl.event.desde = fechas.startDate.toString();
        // newEventCtrl.event.hasta = fechas.endDate.toString();
        newEventCtrl.event.desde = fechas.startDate.toISOString();
        newEventCtrl.event.hasta = fechas.endDate.toISOString();

      } else {
        newEventCtrl.event.tipo = '';
      }

      $rootScope.$broadcast('event.created', {
        titulo: newEventCtrl.event.titulo,
        tipo: newEventCtrl.event.tipo,
        contenido: newEventCtrl.event.contenido,
        autor: {
          email: Authentication.getAuthenticatedAccount().data.email
        },
        created_at: newEventCtrl.created_at
      });

      // $scope.closeThisDialog();
      preAction();
      Events.create(newEventCtrl.event).then(createEventSuccessFn, createEventErrorFn).finally(postAction);


      /**
      * @name createEventSuccessFn
      * @desc Show snackbar with success message
      */
      function createEventSuccessFn(data, status, headers, config) {
        Snackbar.success('El evento se ha creado con exito.');
      }


      /**
      * @name createEventErrorFn
      * @desc Propagate error event and show snackbar with error message
      */
      function createEventErrorFn(data, status, headers, config) {
        $rootScope.$broadcast('event.created.error');
        Snackbar.error(data.data.message);
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
