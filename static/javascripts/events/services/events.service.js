/**
* Events
* @namespace gestfg.events.services
*/
(function () {
  'use strict';

  angular
    .module('gestfg.events.services')
    .factory('Events', Events);

  Posts.$inject = ['$http'];

  /**
  * @namespace Events
  * @returns {Factory}
  */
  function Events($http) {
    var Events = {
      all: all,
      create: create,
      get: get
    };

    return Events;

    ////////////////////

    /**
    * @name all
    * @desc Get all Events
    * @returns {Promise}
    * @memberOf gestfg.events.services.Events
    */
    function all() {
      return $http.get('/api/v1/events/');
    }


    /**
    * @name create
    * @desc Create a new Event
    * @param {string} content The content of the new Event
    * @returns {Promise}
    * @memberOf gestfg.events.services.Events
    */
    function create(content) {
      return $http.post('/api/v1/events/', {
        content: content
      });
    }

    /**
     * @name get
     * @desc Get the Events of a given user
     * @param {string} username The username to get Events for
     * @returns {Promise}
     * @memberOf gestfg.events.services.Events
     */
    function get(username) {
      return $http.get('/api/v1/accounts/' + username + '/events/');
    }
  }
})();
