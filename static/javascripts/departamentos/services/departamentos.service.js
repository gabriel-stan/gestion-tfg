/**
* Departamentos
* @namespace gestfg.departamentos.services
*/
(function () {
  'use strict';

  angular
    .module('gestfg.departamentos.services')
    .factory('Departamentos', Departamentos);

  Departamentos.$inject = ['$http'];

  /**
  * @namespace Departamentos
  * @returns {Factory}
  */
  function Departamentos($http) {
    var Departamentos = {
      all: all,
      create: create,
      edit: edit,
      get: get
    };

    return Departamentos;

    ////////////////////

    /**
    * @name all
    * @desc Get all Departamentos
    * @returns {Promise}
    * @memberOf gestfg.departamentos.services.Departamentos
    */
    function all() {
      return $http.get('/api/v1/departamentos/');
    }


    /**
    * @name create
    * @desc Create a new Departamento
    * @param {string} content The content of the new Departamento
    * @returns {Promise}
    * @memberOf gestfg.departamentos.services.Departamentos
    */
    function create(content) {
      return $http.post('/api/v1/departamentos/', {
        content: content
      });
    }

    /**
    * @name edit
    * @desc edit a Departamento
    * @returns {Promise}
    * @memberOf gestfg.departamentos.services.Departamentos
    */
    function edit(content) {
      return $http.put('/api/v1/departamentos/', {
        codigo: content.old_codigo,
        datos: JSON.stringify(content)
      });
    }

    /**
     * @name get
     * @desc Get a Departamento
     * @param {string} email The id of the Departamento
     * @returns {Promise}
     * @memberOf gestfg.departamentos.services.Departamentos
     */
    function get(id) {
      return $http.get('/api/v1/departamentos/' + id);
    }
  }
})();
