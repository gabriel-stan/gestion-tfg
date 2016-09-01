/**
* TfgsController
* @namespace gestfg.tfgs.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.tfgs.controllers')
    .controller('TfgsController', TfgsController);

  TfgsController.$inject = ['$scope', '$document', 'Tfgs', 'Snackbar'];

  /**
  * @namespace TfgsController
  */
  function TfgsController($scope, $document, Tfgs, Snackbar) {

    var tfgsCtrl = this;
    tfgsCtrl.loadTfgs = loadTfgs;
    tfgsCtrl.presentarTFGs = presentarTFGs;
    tfgsCtrl.asignarTFG = asignarTFG;
    tfgsCtrl.filter = filter;

    tfgsCtrl.loading = true;

    $scope.presentarTFGs = presentarTFGs;

    $scope.selectedTFG = new Object();

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

      $scope.selectedTFG.old_titulo = tfg.titulo;
    }

    $scope.loadSelectedTFGAsig = function() {
      var tfg = $("#tabla-tfgs").DataTable().row( { selected: true } ).data();
      $scope.selectedTFG.titulacion = tfg.tfg.titulacion.codigo;
      $scope.selectedTFG.asignado = true;
      $scope.selectedTFG.n_alumnos = tfg.tfg.n_alumnos;
      $scope.selectedTFG.tipo = tfg.tfg.tipo;

      $scope.selectedTFG.titulo = tfg.tfg.titulo;
      $scope.selectedTFG.descripcion = tfg.tfg.descripcion;
      $scope.selectedTFG.conocimientos_previos = tfg.tfg.conocimientos_previos;
      $scope.selectedTFG.hard_soft = tfg.tfg.hard_soft;

      $scope.selectedTFG.tutor = tfg.tfg.tutor.email;
      if(tfg.tfg.cotutor){
          $scope.selectedTFG.cotutor = tfg.tfg.cotutor.email;
      }

      $scope.selectedTFG.alumno1 = tfg.alumno_1.email;
      if(tfg.alumno_2){
          $scope.selectedTFG.alumno2 = tfg.alumno_2.email;
      }

      if(tfg.alumno_3){
          $scope.selectedTFG.alumno2 = tfg.alumno_3.email;
      }
    }

    $scope.loadSelectedTFGPresentar = function() {
      var tfgs = $("#tabla-tfgs").DataTable().rows( { selected: true } ).data();

      tfgsCtrl.tfgs_presentar = [];

      $.each(tfgs, function( i, tfg ) {
        var t = new Object();
        t.titulo = tfg.tfg.titulo;
        tfgsCtrl.tfgs_presentar.push(t);
      });

    }


    /**
    * @name presentarTFGs
    * @desc Presenta los tfgs a la convocatoria
    * @memberOf gestfg.tfgs.controllers.TfgsController
    */
    function presentarTFGs(){

      $.each(tfgsCtrl.tfgs_presentar, function( i, tfg ) {
        var convocatoria = new Object();
        convocatoria.anio = tfgsCtrl.anio;
        convocatoria.convocatoria = tfgsCtrl.convocatoria;

        preAction();
        Tfgs.presentar(tfg.titulo, JSON.stringify(convocatoria)).then(TfgsSuccessFn, TfgsErrorFn).finally(postAction);
      });

      /**
      * @name TfgsSuccessFn
      * @desc Show Snackbar with success
      */
      function TfgsSuccessFn(data, status, headers, config) {
        Snackbar.success("TFG presentado correctamente");
        postActionSuccess();
      }

    }


    /**
    * @name asignarTFG
    * @desc Asigna los alumnos al TFG
    * @memberOf gestfg.tfgs.controllers.TfgsController
    */
    function asignarTFG(){

      preAction();
      Tfgs.asignar($scope.selectedTFG).then(TfgsSuccessFn, TfgsErrorFn).finally(postAction);

      /**
      * @name TfgsSuccessFn
      * @desc Show Snackbar with success
      */
      function TfgsSuccessFn(data, status, headers, config) {
        Snackbar.success("TFG asignado correctamente");
        postActionSuccess();
      }

    }

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

    /**
    * @name TfgsErrorFn
    * @desc Show snackbar with error
    */
    function TfgsErrorFn(data, status, headers, config) {
      Snackbar.error(data.data.message);
    }


    function preAction(){
      $scope.loading = true;
    }

    function postAction(){
      $scope.loading = false;
    }

    function postActionSuccess(){
      $('.modal').modal('hide');
      $("#tabla-tfgs").DataTable().clear().draw();
      $("#tabla-tfgs").DataTable().ajax.reload();
    }

    $document.on('/dashboard/tfgs', function(){
      //$document.off('/dashboard/tfgs');
      //$document.trigger('ready');
    });

    $document.on('/dashboard/tfgs-asig', function(){
      //$document.off('/dashboard/tfgs-asig');
      //$document.trigger('ready');
    });

  }
})();
