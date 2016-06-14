/**
* NewDepartamentoController
* @namespace gestfg.departamentos.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.departamentos.controllers')
    .controller('NewDepartamentoController', NewDepartamentoController);

  NewDepartamentoController.$inject = ['$rootScope', '$scope', 'Authentication', 'Snackbar', 'Departamentos'];

  /**
  * @namespace NewDepartamentoController
  */
  function NewDepartamentoController($rootScope, $scope, Authentication, Snackbar, Departamentos) {
    var newDepartamentoCtrl = this;

    newDepartamentoCtrl.submit = submit;

    /**
    * @name submit
    * @desc Create a new Departamento
    * @memberOf gestfg.departamentos.controllers.NewDepartamentoController
    */
    function submit() {

      $rootScope.$broadcast('departamento.created', {
        id: newDepartamentoCtrl.departamento.id,
        nombre: newDepartamentoCtrl.departamento.nombre
      });

      // $scope.closeThisDialog();

      Departamentos.create(newDepartamentoCtrl.departamento).then(createDepartamentoSuccessFn, createDepartamentoErrorFn);


      /**
      * @name createDepartamentoSuccessFn
      * @desc Show snackbar with success message
      */
      function createDepartamentoSuccessFn(data, status, headers, config) {
        Snackbar.success('El usuario se ha creado con éxito.');
      }


      /**
      * @name createDepartamentoErrorFn
      * @desc Propagate error event and show snackbar with error message
      */
      function createDepartamentoErrorFn(data, status, headers, config) {
        $rootScope.$broadcast('departamento.created.error');
        Snackbar.error(data.message);
      }
    }
  }
})();
