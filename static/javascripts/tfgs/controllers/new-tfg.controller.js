/**
* NewTfgController
* @namespace gestfg.tfgs.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.tfgs.controllers')
    .controller('NewTfgController', NewTfgController);

  NewTfgController.$inject = ['$rootScope', '$scope', 'Authentication', 'Snackbar', 'Tfgs'];

  /**
  * @namespace NewTfgController
  */
  function NewTfgController($rootScope, $scope, Authentication, Snackbar, Tfgs) {
    var newTfgCtrl = this;

    newTfgCtrl.submit = submit;

    /**
    * @name submit
    * @desc Create a new Tfg
    * @memberOf gestfg.tfgs.controllers.NewTfgController
    */
    function submit() {

      $rootScope.$broadcast('tfg.created', {
        first_name: newTfgCtrl.tfg.first_name,
        last_name: newTfgCtrl.tfg.last_name,
        clase: newTfgCtrl.tfg.clase,
        is_admin: newTfgCtrl.tfg.is_admin,
        email: newTfgCtrl.tfg.email,
        departamento: newTfgCtrl.tfg.departamento,
        created_at: newTfgCtrl.created_at
      });

      // $scope.closeThisDialog();

      Tfgs.create(newTfgCtrl.tfg).then(createTfgSuccessFn, createTfgErrorFn);


      /**
      * @name createTfgSuccessFn
      * @desc Show snackbar with success message
      */
      function createTfgSuccessFn(data, status, headers, config) {
        Snackbar.success('El TFG se ha creado con éxito.');
      }


      /**
      * @name createTfgErrorFn
      * @desc Propagate error event and show snackbar with error message
      */
      function createTfgErrorFn(data, status, headers, config) {
        $rootScope.$broadcast('tfg.created.error');
        Snackbar.error(data.data.message);
      }
    }
  }
})();
