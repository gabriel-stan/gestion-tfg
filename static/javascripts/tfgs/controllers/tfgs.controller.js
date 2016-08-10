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
