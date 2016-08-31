/**
* NewDepartamentoController
* @namespace gestfg.departamentos.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.departamentos.controllers')
    .controller('NewDepartamentoController', NewDepartamentoController);

  NewDepartamentoController.$inject = ['$rootScope', '$scope', 'Snackbar', 'Departamentos'];

  /**
  * @namespace NewDepartamentoController
  */
  function NewDepartamentoController($rootScope, $scope, Snackbar, Departamentos) {
    var newDepartamentoCtrl = this;

    newDepartamentoCtrl.submit = submit;
    newDepartamentoCtrl.edit = edit;

    $scope.submit = submit;
    $scope.edit = edit;

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
      preAction();
      Departamentos.create(newDepartamentoCtrl.departamento).then(createDepartamentoSuccessFn, DepartamentoErrorFn).finally(postAction);


      /**
      * @name createDepartamentoSuccessFn
      * @desc Show snackbar with success message
      */
      function createDepartamentoSuccessFn(data, status, headers, config) {
        Snackbar.success('El departamento se ha creado con éxito.');
      }

    }

    /**
    * @name edit
    * @desc edit a Departamento
    * @memberOf gestfg.departamentos.controllers.NewDepartamentoController
    */
    function edit() {

      preAction();
      Departamentos.edit($scope.departamento).then(editDepartamentoSuccessFn, DepartamentoErrorFn).finally(postAction);

      /**
      * @name editDepartamentoSuccessFn
      * @desc Show snackbar with success message
      */
      function editDepartamentoSuccessFn(data, status, headers, config) {
        Snackbar.success('El departamento se ha modificado con éxito.');
        postActionSuccess();
      }

    }

    /**
    * @name DepartamentoErrorFn
    * @desc Show snackbar with error message
    */
    function DepartamentoErrorFn(data, status, headers, config) {
      Snackbar.error(data.message);
    }

    function preAction(){
      $scope.loading = true;
    }

    function postAction(){
      $scope.loading = false;
    }

    function postActionSuccess(){
      $('.modal').modal('hide');
      $("#tabla-dpts").DataTable().clear().draw();
      $("#tabla-dpts").DataTable().ajax.reload();
    }

  }
})();
