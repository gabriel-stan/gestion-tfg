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
    newTfgCtrl.update = update;
    newTfgCtrl.submitAsig = submitAsig;
    newTfgCtrl.updateAsig = updateAsig;

    $scope.submit = submit;
    $scope.update = update;
    $scope.submit = submitAsig;
    $scope.update = updateAsig;

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
      preAction();
      Tfgs.create(newTfgCtrl.tfg).then(createTfgSuccessFn, TfgErrorFn).finally(postAction);


      /**
      * @name createTfgSuccessFn
      * @desc Show snackbar with success message
      */
      function createTfgSuccessFn(data, status, headers, config) {
        Snackbar.success('El TFG se ha creado con éxito.');
      }
    }


    /**
    * @name update
    * @desc Update a Tfg
    * @memberOf gestfg.tfgs.controllers.NewTfgController
    */
    function update() {

      preAction();
      Tfgs.update($scope.tfg).then(updateTfgSuccessFn, TfgErrorFn).finally(postAction);

      /**
      * @name updateTfgSuccessFn
      * @desc Show snackbar with success message
      */
      function updateTfgSuccessFn(data, status, headers, config) {
        Snackbar.success('El TFG se ha modificado con éxito.');
      }
    }


    /**
    * @name TfgErrorFn
    * @desc Propagate error event and show snackbar with error message
    */
    function TfgErrorFn(data, status, headers, config) {
      $rootScope.$broadcast('tfg.created.error');
      Snackbar.error(data.data.message);
    }

    function preAction(){
      $scope.loading = true;
    }

    function postAction(){
      $scope.loading = false;
    }

  }
})();
