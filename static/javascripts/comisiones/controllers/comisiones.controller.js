/**
* ComisionesController
* @namespace gestfg.comisiones.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.comisiones.controllers')
    .controller('ComisionesController', ComisionesController);

  ComisionesController.$inject = ['$scope', '$rootScope', 'Comisiones', 'Snackbar'];

  /**
  * @namespace ComisionesController
  */
  function ComisionesController($scope, $rootScope, Comisiones, Snackbar) {

    var comisionesCtrl = this;
    comisionesCtrl.generarComisiones = generarComisiones;
    comisionesCtrl.generarTribunales = generarTribunales;
    comisionesCtrl.getComisiones = getComisiones;

    $scope.generarComisiones = generarComisiones;
    $scope.generarTribunales = generarTribunales;
    $scope.getComisiones = getComisiones;

    /**
    * @name generarComisiones
    * @desc Genera las comisiones
    * @memberOf gestfg.comisiones.controllers.ComisionesController
    */
    function generarComisiones(){

      if(confirm('¿Seguro?')){
        preAction();
        Comisiones.generarComisiones(comisionesCtrl.titulacion, comisionesCtrl.convocatoria, comisionesCtrl.anio).then(ComisionesSuccessFn, ComisionesErrorFn).finally(postAction);
      }

      /**
      * @name ComisionesSuccessFn
      * @desc Show Snackbar with success
      */
      function ComisionesSuccessFn(data, status, headers, config) {
        Snackbar.success("Comisiones generadas correctamente");
        postActionSuccess();
      }


      /**
      * @name TfgsErrorFn
      * @desc Show snackbar with error
      */
      function ComisionesErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.message);
      }
    }

    /**
    * @name generarTribunales
    * @desc Genera los tribunales a partir de las comisiones y TFGs presentados
    * @memberOf gestfg.comisiones.controllers.ComisionesController
    */
    function generarTribunales(){

      alert('por hacer: comisiones.controller.js');
      // if(confirm('¿Seguro?')){
      //   preAction();
      //   Comisiones.generate(comisionesCtrl.convocatoria).then(ComisionesSuccessFn, ComisionesErrorFn).finally(postAction);
      // }

      /**
      * @name ComisionesSuccessFn
      * @desc Show Snackbar with success
      */
      function ComisionesSuccessFn(data, status, headers, config) {
        Snackbar.success("Comisiones generadas correctamente");
        postActionSuccess();
      }


      /**
      * @name TfgsErrorFn
      * @desc Show snackbar with error
      */
      function ComisionesErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.message);
      }
    }


    /**
    * @name getComisiones
    * @desc Obtiene las comisiones
    * @memberOf gestfg.comisiones.controllers.ComisionesController
    */
    function getComisiones(){


      Comisiones.all().then(ComisionesSuccessFn, ComisionesErrorFn);

      /**
      * @name ComisionesSuccessFn
      * @desc Show Snackbar with success
      */
      function ComisionesSuccessFn(data, status, headers, config) {
        Snackbar.success("llamada realizada correctamente");
      }


      /**
      * @name TfgsErrorFn
      * @desc Show snackbar with error
      */
      function ComisionesErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.message);
      }
    }

    function preAction(){
      $scope.loading = true;
    }

    function postAction(){
      $scope.loading = false;
    }

    function postActionSuccess(){
      $('.modal').modal('hide');
      $("#tabla-comisiones").DataTable().clear().draw();
      $("#tabla-comisiones").DataTable().ajax.reload();
    }

  }
})();
