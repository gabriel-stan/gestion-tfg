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

    $scope.load_validated = function() {
      $scope.validados = $routeParams.datos;
      var validados = $rootScope.tfgs_validados;
      var tabla = $('#tabla-tfgs').DataTable();
      tabla.clear().draw();

      function anadir( i, val ) {
        tabla.row.add([
          val.tfg.titulacion,
          val.tfg.tipo,
          val.tfg.titulo,
          val.tfg.n_alumnos,
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
      cabeceras.titulacion = uploadTfgsCtrl.titulacion2;

      var fd = new FormData();

      var f = document.getElementById('upload-file').files[0];

      fd.append('file', f);
      fd.append('cabeceras', JSON.stringify(cabeceras));
      fd.append('u_fila', uploadTfgsCtrl.u_fila);
      fd.append('p_fila', uploadTfgsCtrl.p_fila);
      fd.append('titulacion', uploadTfgsCtrl.titulacion);
      fd.append('tipe_file', 'tfg');

      Tfgs.upload(fd).then(uploadTfgsSuccessFn, uploadTfgsErrorFn);

      /**
      * @name uploadTfgsSuccessFn
      * @desc Show snackbar with success message
      */
      function uploadTfgsSuccessFn(data, status, headers, config) {
        Snackbar.success('Los TFGs se han procesado con exito. Compruebe los datos y confirmelos.');
        $rootScope.tfgs_validados = data.data;
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
  }
})();
