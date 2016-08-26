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
    comisionesCtrl.getComisiones = getComisiones;

    /**
    * @name generarComisiones
    * @desc Genera las comisiones
    * @memberOf gestfg.comisiones.controllers.ComisionesController
    */
    function generarComisiones(){

      if(confirm('¿Seguro?')){
        Comisiones.generate(comisionesCtrl.convocatoria).then(ComisionesSuccessFn, ComisionesErrorFn);
      }

      /**
      * @name ComisionesSuccessFn
      * @desc Show Snackbar with success
      */
      function ComisionesSuccessFn(data, status, headers, config) {
        Snackbar.success("Comisiones generadas correctamente");
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

  }
})();
