/**
* Snackbar
* @namespace gestfg.utils.services
*/
(function ($, _) {
  'use strict';

  angular
    .module('gestfg.utils.services')
    .factory('Snackbar', Snackbar);

  /**
  * @namespace Snackbar
  */
  function Snackbar() {
    /**
    * @name Snackbar
    * @desc The factory to be returned
    */
    var Snackbar = {
      error: error,
      info: info,
      warning: warning,
      success: success
    };

    return Snackbar;

    ////////////////////

    /**
    * @name _snackbar
    * @desc Display a snackbar
    * @param {string} content The content of the snackbar
    * @param {Object} options Options for displaying the snackbar
    */
    function _snackbar(content, title, options) {
      // options = _.extend({ timeout: 3000 }, options);
      // options.content = content;
      //
      // $.snackbar(options);

      toastr.options = _.extend({
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-bottom-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "4000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
      }, options);

      toastr[options["type"]](content, title);

    }


    /**
    * @name error
    * @desc Display an error snackbar
    * @param {string} content The content of the snackbar
    * @param {Object} options Options for displaying the snackbar
    * @memberOf gestfg.utils.services.Snackbar
    */
    function error(content, options) {
      options = _.extend({
        "type": "error"
      }, options);
      _snackbar(content, 'Error', options);
    }


    /**
    * @name show
    * @desc Display a standard snackbar
    * @param {string} content The content of the snackbar
    * @param {Object} options Options for displaying the snackbar
    * @memberOf gestfg.utils.services.Snackbar
    */
    function success(content, options) {
      options = _.extend({
        "type": "success"
      }, options);
      _snackbar(content, 'Success', options);
    }


    /**
    * @name show
    * @desc Display a standard snackbar
    * @param {string} content The content of the snackbar
    * @param {Object} options Options for displaying the snackbar
    * @memberOf gestfg.utils.services.Snackbar
    */
    function warning(content, options) {
      options = _.extend({
        "type": "warning"
      }, options);
      _snackbar(content, 'Warning', options);
    }



    /**
    * @name show
    * @desc Display a standard snackbar
    * @param {string} content The content of the snackbar
    * @param {Object} options Options for displaying the snackbar
    * @memberOf gestfg.utils.services.Snackbar
    */
    function info(content, options) {
      options = _.extend({
        "type": "info"
      }, options);
      _snackbar(content, 'Info', options);
    }
  }
})($, _);
