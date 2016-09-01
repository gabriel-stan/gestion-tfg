/**
* UploadTfgsController
* @namespace gestfg.tfgs.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.tfgs.controllers')
    .controller('UploadTfgsController', UploadTfgsController);

  UploadTfgsController.$inject = ['$rootScope', '$scope', '$location', '$routeParams', 'Authentication', 'Snackbar', 'Tfgs'];

  /**
  * @namespace UploadTfgsController
  */
  function UploadTfgsController($rootScope, $scope, $location, $routeParams, Authentication, Snackbar, Tfgs) {
    var uploadTfgsCtrl = this;

    uploadTfgsCtrl.submit = submit;

    $scope.submit = submit;

    $scope.load_validated = function() {
      $scope.validados = $routeParams.datos;
      var validados = $rootScope.tfgs_validados;
      var tabla = $('#tabla-tfgs').DataTable();
      tabla.clear().draw();

      function anadir( i, val ) {

        var alumnos;
        if($rootScope.preasignados){
          alumnos = val.tfg.alumno_1;
          if(val.tfg.alumno_2){
            alumnos += ', ' + val.tfg.alumno_2;
          }
          if(val.tfg.alumno_3){
            alumnos += ', ' + val.tfg.alumno_3;
          }
        } else {
          alumnos = val.tfg.n_alumnos;
        }

        tabla.row.add([
          val.tfg.titulacion,
          val.tfg.tipo,
          val.tfg.titulo,
          alumnos,
          val.tfg.descripcion,
          val.tfg.conocimientos_previos ? val.tfg.conocimientos_previos : '',
          val.tfg.hard_soft ? val.tfg.hard_soft : '',
          val.tfg.tutor,
          val.tfg.cotutor ? val.tfg.cotutor : ''
        ]).draw();
      }

      if(validados){
        jQuery.each( validados.errores, function( i, val ) {

        });

        jQuery.each( validados.exitos, anadir);
      }

      tabla.draw();

    };

    $scope.insert_validated = function() {

      if($rootScope.tfgs_validados){
        preAction();
        if($rootScope.preasignados){
          Tfgs.insert_validated('tfg_asig', JSON.stringify($rootScope.tfgs_validados.exitos)).then(insertTfgsSuccessFn, insertTfgsErrorFn).finally(postAction);
        } else {
          Tfgs.insert_validated('tfg', JSON.stringify($rootScope.tfgs_validados.exitos)).then(insertTfgsSuccessFn, insertTfgsErrorFn).finally(postAction);
        }
      } else {
        alert('no hay TFGs validados');
      }

      /**
      * @name insertTfgsSuccessFn
      * @desc Show snackbar with success message
      */
      function insertTfgsSuccessFn(data, status, headers, config) {
        Snackbar.success('Los TFGs se han insertado con exito.');
        postActionSuccess();
      }


      /**
      * @name insertTfgsErrorFn
      * @desc Propagate error event and show snackbar with error message
      */
      function insertTfgsErrorFn(data, status, headers, config) {
        $rootScope.$broadcast('tfg.insert.error');
        Snackbar.error(data.data.message);
      }

    }

    /**
    * @name submit
    * @desc Upload a lot of Projects
    * @memberOf gestfg.tfgs.controllers.UploadTfgsController
    */
    function submit() {

      var cabeceras = new Object();
      cabeceras.tipo = uploadTfgsCtrl.tipo;
      cabeceras.titulo = uploadTfgsCtrl.titulo;
      cabeceras.n_alumnos = uploadTfgsCtrl.n_alumnos;
      cabeceras.descripcion = uploadTfgsCtrl.descripcion;
      cabeceras.conocimientos_previos = uploadTfgsCtrl.conocimientos_previos;
      cabeceras.hard_soft = uploadTfgsCtrl.hard_soft;
      cabeceras.tutor = uploadTfgsCtrl.tutor;
      cabeceras.cotutor = uploadTfgsCtrl.cotutor;
      //cabeceras.titulacion = uploadTfgsCtrl.titulacion2;

      if(uploadTfgsCtrl.preasignados){
        cabeceras.alumno_1 = uploadTfgsCtrl.alumno1;
        cabeceras.alumno_2 = uploadTfgsCtrl.alumno2;
        cabeceras.alumno_3 = uploadTfgsCtrl.alumno3;
      }

      var fd = new FormData();

      var f = document.getElementById('upload-file').files[0];

      fd.append('file', f);
      fd.append('cabeceras', JSON.stringify(cabeceras));
      fd.append('u_fila', uploadTfgsCtrl.u_fila);
      fd.append('p_fila', uploadTfgsCtrl.p_fila);
      fd.append('titulacion', uploadTfgsCtrl.titulacion);

      if(uploadTfgsCtrl.preasignados){
        fd.append('type_file', 'tfg_asig');
      } else {
        fd.append('type_file', 'tfg');
      }

      preAction();
      Tfgs.upload('/api/v1/upload_file_tfgs/', fd).then(uploadTfgsSuccessFn, uploadTfgsErrorFn).finally(postAction);

      /**
      * @name uploadTfgsSuccessFn
      * @desc Show snackbar with success message
      */
      function uploadTfgsSuccessFn(data, status, headers, config) {
        Snackbar.success('Los TFGs se han procesado con exito. Compruebe los datos y confirmelos.');
        $rootScope.tfgs_validados = data.data;
        $rootScope.preasignados = uploadTfgsCtrl.preasignados;
        $location.path('/dashboard/tfgs/validate?datos=validados');
      }


      /**
      * @name uploadTfgsErrorFn
      * @desc Propagate error event and show snackbar with error message
      */
      function uploadTfgsErrorFn(data, status, headers, config) {
        $rootScope.$broadcast('tfg.upload.error');
        Snackbar.error(data.data.message);
      }
    }

    function preAction(){
      $scope.loading = true;
      $('.action-btn').addClass('disabled');
    }

    function postAction(){
      $scope.loading = false;
      $('.action-btn').removeClass('disabled');
    }

    function postActionSuccess(){
      $("#tabla-tfgs").DataTable().clear().draw();
      // $("#tabla-tfgs").DataTable().ajax.reload();
    }

  }
})();
