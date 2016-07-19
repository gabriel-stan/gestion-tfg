/**
* Tfg
* @namespace gestfg.tfgs.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.tfgs.directives')
    .directive('tfg', tfg);

  /**
  * @namespace Tfg
  */
  function tfg() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.tfgs.directives.Tfg
    */
    var directive = {
      restrict: 'E',
      scope: {
        tfg: '='
      },
      templateUrl: '/static/templates/tfgs/tfg.html'
    };

    return directive;
  }
})();
