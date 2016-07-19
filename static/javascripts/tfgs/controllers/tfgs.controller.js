/**
* TfgsController
* @namespace gestfg.tfgs.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.tfgs.controllers')
    .controller('TfgsController', TfgsController);

  TfgsController.$inject = ['$scope', 'Tfgs'];

  /**
  * @namespace TfgsController
  */
  function TfgsController($scope, Tfgs) {

    var tfgsCtrl = this;
    tfgsCtrl.loadTfgs = loadTfgs;

    loadTfgs();

    /**
    * @name loadTfgs
    * @desc Loads all tfgs from database
    * @memberOf gestfg.tfgs.controllers.TfgsController
    */
    function loadTfgs(){
      // alert("Load tfgs controlador");
      Tfgs.all().then(TfgsSuccessFn, TfgsErrorFn);

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
  }
})();
