/**
* DepartamentosController
* @namespace gestfg.departamentos.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.departamentos.controllers')
    .controller('DepartamentosController', DepartamentosController);

  DepartamentosController.$inject = ['$rootScope', '$scope', 'Authentication', 'Snackbar', 'Departamentos'];

  /**
  * @namespace DepartamentosController
  */
  function DepartamentosController($rootScope, $scope, Authentication, Snackbar, Departamentos) {
    var dptsCtrl = this;

    dptsCtrl.loadSelectedDpt = loadSelectedDpt;

    $scope.loadSelectedDpt = loadSelectedDpt;

    $scope.selectedDpt = new Object();


    function loadSelectedDpt() {
      var dpt = $("#tabla-dpts").DataTable().row( { selected: true } ).data();
      $scope.selectedDpt.old_codigo = dpt.codigo;
      $scope.selectedDpt.codigo = dpt.codigo;
      $scope.selectedDpt.nombre = dpt.nombre;
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
