/**
* Users
* @namespace gestfg.users.services
*/
(function () {
  'use strict';

  angular
    .module('gestfg.users.services')
    .factory('Users', Users);

  Users.$inject = ['$http'];

  /**
  * @namespace Users
  * @returns {Factory}
  */
  function Users($http) {
    var Users = {
      all: all,
      create: create,
      get: get,
      update: update,
      remove: remove
    };

    return Users;

    ////////////////////

    /**
    * @name all
    * @desc Get all Users
    * @returns {Promise}
    * @memberOf gestfg.users.services.Users
    */
    function all() {
      return $http.get('/api/v1/usuarios/');
    }


    /**
    * @name create
    * @desc Create a new User
    * @param {string} content The content of the new User
    * @returns {Promise}
    * @memberOf gestfg.users.services.Users
    */
    function create(content) {
      return $http.post('/api/v1/' + content.tipo + '/', {
        content: content
      });
    }

    /**
     * @name get
     * @desc Get a User
     * @param {string} email The email of the User
     * @returns {Promise}
     * @memberOf gestfg.users.services.Users
     */
    function get(email) {
      return $http.get('/api/v1/usuarios/' + email);
    }

    function update(content) {
      return $http.put('/api/v1/' + content.llamada + '/', content);
    }

    function remove(tipo, email) {
      return $http.delete('/api/v1/' + tipo + '/' + email);
    }
  }
})();
