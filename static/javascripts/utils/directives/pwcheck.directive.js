/**
* pwCheck
* @namespace gestfg.utils.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.utils.directives')
    .directive('pwCheck', pwCheck);

  /**
  * @namespace pwCheck
  */
  function pwCheck() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.utils.directives.pwCheck
    */
    var directive = {
      restrict: 'A',
      require: 'ngModel',
      link: function (scope, elem, attrs, ctrl) {
        var firstPassword = '#' + attrs.pwCheck;
        elem.add(firstPassword).on('keyup', function () {
          scope.$apply(function () {
            var v = elem.val()===$(firstPassword).val();
            ctrl.$setValidity('pwmatch', v);
          });
        });
      }
    };

    return directive;
  }
})();
