/**
* Dashboard
* @namespace gestfg.layout.services
*/
(function () {
  'use strict';

  angular
    .module('gestfg.layout.services')
    .factory('Dashboard', Dashboard);

  Dashboard.$inject = ['$http'];

  /**
  * @namespace Dashboard
  * @returns {Factory}
  */
  function Dashboard($http) {
    var Dashboard = {
      upload: upload
    };

    function upload(content) {
      return $http.post('/api/v1/auth/load_data/', content, {
        transformRequest: angular.identity,
        headers: {'Content-Type': undefined}
      });
    }

    return Dashboard;
  }
})();
