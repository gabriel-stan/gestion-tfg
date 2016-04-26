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
    var vm = this;

    vm.submit = submit;

    /**
    * @name submit
    * @desc Create a new Event
    * @memberOf gestfg.events.controllers.NewEventController
    */
    function submit() {
      $rootScope.$broadcast('event.created', {
        contenido: vm.content,
        autor: {
          email: Authentication.getAuthenticatedAccount().data.email
        },
        created_at: vm.created_at
      });

      $scope.closeThisDialog();

      Events.create(vm.content).then(createEventSuccessFn, createEventErrorFn);


      /**
      * @name createEventSuccessFn
      * @desc Show snackbar with success message
      */
      function createEventSuccessFn(data, status, headers, config) {
        Snackbar.show('El evento se ha creado con exito.');
      }


      /**
      * @name createEventErrorFn
      * @desc Propagate error event and show snackbar with error message
      */
      function createEventErrorFn(data, status, headers, config) {
        $rootScope.$broadcast('event.created.error');
        Snackbar.error(data.error);
      }
    }
  }
})();
