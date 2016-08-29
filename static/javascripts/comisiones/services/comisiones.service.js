/**
* Comisiones
* @namespace gestfg.comisiones.services
*/
(function () {
  'use strict';

  angular
    .module('gestfg.comisiones.services')
    .factory('Comisiones', Comisiones);

  Comisiones.$inject = ['$http'];

  /**
  * @namespace Comisiones
  * @returns {Factory}
  */
  function Comisiones($http) {
    var Comisiones = {
      all: all,
      generate: generate
    };

    return Comisiones;

    ////////////////////

    /**
    * @name all
    * @desc Get all Comisiones
    * @returns {Promise}
    * @memberOf gestfg.comisiones.services.Comisiones
    */
    function all() {
      return $http.get('/api/v1/comisiones/');
    }

    /**
    * @name generate
    * @desc generate all Comisiones
    * @returns {Promise}
    * @memberOf gestfg.comisiones.services.Comisiones
    */
    function generate(convocatoria) {
      return $http.post('/api/v1/comisiones/',{
        convocatoria: convocatoria
      });
    }

  }
})();
