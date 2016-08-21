/**
* TfgsController
* @namespace gestfg.tfgs.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.tfgs.controllers')
    .controller('TfgsController', TfgsController);

  TfgsController.$inject = ['$scope', 'Tfgs', 'Snackbar'];

  /**
  * @namespace TfgsController
  */
  function TfgsController($scope, Tfgs, Snackbar) {

    var tfgsCtrl = this;
    tfgsCtrl.loadTfgs = loadTfgs;
    tfgsCtrl.filter = filter;
    tfgsCtrl.loading = true;

    tfgsCtrl.parseTimeAgo = function(fecha){
      // console.log(fecha);

      var fecha = new Date(fecha);
      fecha = moment(fecha).fromNow();

      return fecha;
    }


    tfgsCtrl.parseTime = function(fecha){
      // console.log(fecha);

      var fecha = new Date(fecha);
      fecha = moment(fecha).format("DD/MM/YYYY - hh:mm");

      return fecha;
    }

    $scope.loadSelectedTFG = function() {
      var tfg = $("#tabla-tfgs").DataTable().row( { selected: true } ).data();
      $scope.selectedTFG.titulacion = tfg.titulacion.codigo;
      $scope.selectedTFG.asignado = tfg.asignado;
      $scope.selectedTFG.titulo = tfg.titulo;
      $scope.selectedTFG.n_alumnos = tfg.n_alumnos;
      $scope.selectedTFG.descripcion = tfg.descripcion;
      $scope.selectedTFG.conocimientos_previos = tfg.conocimientos_previos;
      $scope.selectedTFG.hard_soft = tfg.hard_soft;
      $scope.selectedTFG.tutor = tfg.tutor.email;
      $scope.selectedTFG.cotutor = tfg.cotutor.email;
      $scope.selectedTFG.alumno1 = tfg.alumno1;
      $scope.selectedTFG.alumno2 = tfg.alumno2;
      $scope.selectedTFG.alumno3 = tfg.alumno3;
      $scope.selectedTFG.tipo = tfg.tipo;
    }

    $scope.selectedTFG = new Object();

    //loadTfgs();

    /**
    * @name loadTfgs
    * @desc Loads all tfgs from database
    * @memberOf gestfg.tfgs.controllers.TfgsController
    */
    function loadTfgs(){
      // alert("Load tfgs controlador");
      preFilter();

      Tfgs.all().then(TfgsSuccessFn, TfgsErrorFn).finally(filterFinally);

      /**
      * @name TfgsSuccessFn
      * @desc Update tfgs array on view
      */
      function TfgsSuccessFn(data, status, headers, config) {
        tfgsCtrl.tfgs = data.data.data;
      }


      /**
      * @name TfgsErrorFn
      * @desc Show snackbar with error
      */
      function TfgsErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.error);
      }
    }

    /**
    * @name filter
    * @desc filter tfgs from database
    * @memberOf gestfg.tfgs.controllers.TfgsController
    */
    function filter(){
      // alert("Load tfgs controlador");
      preFilter();

      Tfgs.filter(tfgsCtrl.filter.titulacion.codigo, tfgsCtrl.filter.asignados, tfgsCtrl.filter.publicados).then(filterSuccessFn, filterErrorFn).finally(filterFinally);

      /**
      * @name TfgsSuccessFn
      * @desc Update tfgs array on view
      */
      function filterSuccessFn(data, status, headers, config) {
        tfgsCtrl.tfgs = data.data.data;
      }


      /**
      * @name TfgsErrorFn
      * @desc Show snackbar with error
      */
      function filterErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.message);
      }
    }

    /**
    * @name preFilter
    * @desc Update view
    */
    function preFilter(data, status, headers, config) {
      tfgsCtrl.loading = true;
      tfgsCtrl.tfgs = [];
      $('#filter').addClass('disabled');
    }

    /**
    * @name filterFinally
    * @desc Update view
    */
    function filterFinally(data, status, headers, config) {
      tfgsCtrl.loading = false;
      $('#filter').removeClass('disabled');
    }

  }
})();
