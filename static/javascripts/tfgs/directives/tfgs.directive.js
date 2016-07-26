/**
* tfgs
* @namespace gestfg.tfgs.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.tfgs.directives')
    .directive('tfgs', tfgs);

  /**
  * @namespace tfgs
  */
  function tfgs() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.tfgs.directives.tfgs
    */
    var directive = {
      controller: 'TfgsController',
      controllerAs: 'vm',
      restrict: 'E',
      templateUrl: '/static/templates/tfgs/tfgs.html'
    };

    return directive;
  }
})();
