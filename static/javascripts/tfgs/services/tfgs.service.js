/**
* Tfgs
* @namespace gestfg.tfgs.services
*/
(function () {
  'use strict';

  angular
    .module('gestfg.tfgs.services')
    .factory('Tfgs', Tfgs);

  Tfgs.$inject = ['$http'];

  /**
  * @namespace Tfgs
  * @returns {Factory}
  */
  function Tfgs($http) {
    var Tfgs = {
      all: all,
      create: create,
      get: get,
      upload: upload,
      insert_validated: insert_validated
    };

    return Tfgs;

    ////////////////////

    /**
    * @name all
    * @desc Get all Tfgs
    * @returns {Promise}
    * @memberOf gestfg.tfgs.services.Tfgs
    */
    function all() {
      return $http.get('/api/v1/tfgs/');
    }


    /**
    * @name create
    * @desc Create a new Tfg
    * @param {string} content The content of the new Tfg
    * @returns {Promise}
    * @memberOf gestfg.tfgs.services.Tfgs
    */
    function create(content) {
      return $http.post('/api/v1/tfgs/', {
        //content: content
        titulacion: content.titulacion,
        tipo: content.tipo,
        titulo: content.titulo,
        descripcion: content.descripcion,
        n_alumnos: content.alumnos,
        conocimientos_previos: content.previos,
        hard_soft: content.hwsw,
        tutor: content.tutor,
        cotutor: content.cotutor
      });
    }

    /**
     * @name get
     * @desc Get a Tfg
     * @param {string} email The id of the Tfg
     * @returns {Promise}
     * @memberOf gestfg.tfgs.services.Tfgs
     */
    function get(id) {
      return $http.get('/api/v1/tfgs/' + id);
    }

    /**
     * @name upload
     * @desc Upload a lot of TFGs
     * @param content
     * @returns {Promise}
     * @memberOf gestfg.tfgs.services.Tfgs
     */
    function upload(content) {
      return $http.post('/api/v1/upload_file_tfgs/', content, {
        transformRequest: angular.identity,
        headers: {'Content-Type': undefined}
      });
    }

    /**
     * @name insert_validated
     * @desc Insert a lot of TFGs
     * @param content
     * @returns {Promise}
     * @memberOf gestfg.tfgs.services.Tfgs
     */
    function insert_validated(model, tfgs) {
      return $http.post('/api/v1/upload_file_tfgs_confirm/', {
        model: model,
        list_tfg: tfgs
      });
    }
  }
})();
