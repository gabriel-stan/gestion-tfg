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
      filter: filter,
      create: create,
      update: update,
      remove: remove,
      updateAsig: updateAsig,
      removeAsig: removeAsig,
      asignar: asignar,
      get: get,
      upload: upload,
      presentar: presentar,
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
    * @name filter
    * @desc Get filtered Tfgs
    * @returns {Promise}
    * @memberOf gestfg.tfgs.services.Tfgs
    */
    function filter(titulacion, asignados, publicados) {

      var params = '?';

      if(titulacion){
        params += 'titulacion=' + titulacion;
      }

      if(asignados != null && asignados != 'all' ){
        params += '&asignado=' + asignados;
      }

      if(publicados != null && publicados != 'all' ){
        params += '&publicado=' + publicados;
      }

      return $http.get('/api/v1/tfgs/' + params);
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
        n_alumnos: content.n_alumnos,
        conocimientos_previos: content.conocimientos_previos,
        hard_soft: content.hard_soft,
        tutor: content.tutor,
        cotutor: content.cotutor
      });
    }


    /**
    * @name update
    * @desc update a Tfg
    * @param {string} content The content of the Tfg
    * @returns {Promise}
    * @memberOf gestfg.tfgs.services.Tfgs
    */
    function update(content) {

      var datos = new Object();

      datos.titulacion = content.titulacion;
      datos.tipo = content.tipo;
      datos.titulo = content.titulo;
      datos.descripcion = content.descripcion;
      datos.n_alumnos = content.n_alumnos;
      datos.conocimientos_previos = content.conocimientos_previos;
      datos.hard_soft = content.hard_soft;
      datos.tutor = content.tutor;
      datos.cotutor = content.cotutor;

      return $http.put('/api/v1/tfgs/', {
        //content: content
        tfg: content.old_titulo,
        datos: JSON.stringify(datos)
      });
    }


    /**
    * @name remove
    * @desc remove a Tfg
    * @returns {Promise}
    * @memberOf gestfg.tfgs.services.Tfgs
    */
    function remove(tfg) {

      return $http.delete('/api/v1/tfgs/', {
        tfg: tfg
      });
    }


    /**
    * @name updateAsig
    * @desc update a Tfg asignado
    * @returns {Promise}
    * @memberOf gestfg.tfgs.services.Tfgs
    */
    function updateAsig(content) {

      var datos = new Object();

      datos.alumno_1 = content.alumno_1;
      datos.alumno_2 = content.alumno_2;
      datos.alumno_3 = content.alumno_3;

      return $http.put('/api/v1/tfgs_asig/', {
        //content: content
        tfg: content.titulo,
        datos: JSON.stringify(datos)
      });
    }


    /**
    * @name removeAsig
    * @desc remove a Tfg asignado
    * @returns {Promise}
    * @memberOf gestfg.tfgs.services.Tfgs
    */
    function removeAsig(tfg) {

      return $http.delete('/api/v1/tfgs_asig/' + tfg + '/', {
        tfg: tfg
      });
    }


    /**
    * @name presentar
    * @desc Presentar un TFG a la convocatoria indicada
    * @param {string} tfg Titulo del TFG
    * @param {string} convocatoria Coonvocatoria
    * @returns {Promise}
    * @memberOf gestfg.tfgs.services.Tfgs
    */
    function presentar(tfg, convocatoria) {
      return $http.put('/api/v1/tfgs_asig/', {
        //content: content
        tfg: tfg,
        datos: convocatoria
      });
    }


    /**
    * @name asignar
    * @desc asignar un TFG
    * @param {string} tfg TFG
    * @returns {Promise}
    * @memberOf gestfg.tfgs.services.Tfgs
    */
    function asignar(tfg) {
      return $http.post('/api/v1/tfgs_asig/', {
        //content: content
        tfg: tfg.titulo,
        alumno_1: tfg.alumno1,
        alumno_2: tfg.alumno2,
        alumno_3: tfg.alumno3
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
    function upload(llamada, content) {
      return $http.post(llamada, content, {
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
