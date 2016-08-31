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
      generarComisiones: generarComisiones,
      generarTribunales: generarTribunales
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
    * @name generarComisiones
    * @desc generate all Comisiones
    * @returns {Promise}
    * @memberOf gestfg.comisiones.services.Comisiones
    */
    function generarComisiones(titulacion, convocatoria, anio) {
      return $http.post('/api/v1/comisiones/',{
        titulacion: titulacion,
        convocatoria: convocatoria,
        anio: anio
      });
    }

    /**
    * @name generarTribunales
    * @desc generate all tribunales
    * @returns {Promise}
    * @memberOf gestfg.comisiones.services.Comisiones
    */
    function generarTribunales(titulacion, convocatoria, anio, comisiones) {
      return $http.post('/api/v1/tribunales/',{
        titulacion: titulacion,
        convocatoria: convocatoria,
        anio: anio,
        comisiones: comisiones
      });
    }

  }
})();
