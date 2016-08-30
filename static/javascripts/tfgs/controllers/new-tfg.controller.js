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
    newTfgCtrl.asignar = asignar;
    // newTfgCtrl.updateAsig = updateAsig;

    $scope.submit = submit;
    $scope.update = update;
    $scope.asignar = asignar;
    // $scope.update = updateAsig;

    /**
    * @name submit
    * @desc Create a new Tfg
    * @memberOf gestfg.tfgs.controllers.NewTfgController
    */
    function submit() {

      // $scope.closeThisDialog();
      preAction();
      Tfgs.create(newTfgCtrl.tfg).then(createTfgSuccessFn, TfgErrorFn).finally(postAction);


      /**
      * @name createTfgSuccessFn
      * @desc Show snackbar with success message
      */
      function createTfgSuccessFn(data, status, headers, config) {
        Snackbar.success('El TFG se ha creado con éxito.');
        if(newTfgCtrl.tfg.preasignado){
          asignar();
        }
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
        postActionSuccess();
      }
    }

    /**
    * @name submitAsig
    * @desc Create a new Tfg Asignado
    * @memberOf gestfg.tfgs.controllers.NewTfgController
    */
    function asignar() {

      // $scope.closeThisDialog();
      preAction();
      Tfgs.asignar(newTfgCtrl.tfg).then(asignarTfgAsigSuccessFn, TfgErrorFn).finally(postAction);

      /**
      * @name asignarTfgAsigSuccessFn
      * @desc Show snackbar with success message
      */
      function asignarTfgAsigSuccessFn(data, status, headers, config) {
        Snackbar.success('El TFG se ha asignado con éxito.');
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

    function postActionSuccess(){
      $('.modal').modal('hide');
      $("#tabla-tfgs").DataTable().clear().draw();
      $("#tabla-tfgs").DataTable().ajax.reload();
    }

  }
})();
