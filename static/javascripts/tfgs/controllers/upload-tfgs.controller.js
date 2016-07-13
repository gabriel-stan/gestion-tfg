/**
* UploadTfgsController
* @namespace gestfg.tfgs.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.tfgs.controllers')
    .controller('UploadTfgsController', UploadTfgsController);

  UploadTfgsController.$inject = ['$rootScope', '$scope', 'Authentication', 'Snackbar', 'Tfgs'];

  /**
  * @namespace UploadTfgsController
  */
  function UploadTfgsController($rootScope, $scope, Authentication, Snackbar, Tfgs) {
    var uploadTfgsCtrl = this;

    uploadTfgsCtrl.submit = submit;

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
