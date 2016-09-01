/**
* Authentication
* @namespace gestfg.authentication.services
*/
(function () {
  'use strict';

  angular
    .module('gestfg.authentication.services')
    .factory('Authentication', Authentication);

  Authentication.$inject = ['$cookies', '$http', 'Snackbar'];

  /**
  * @namespace Authentication
  * @returns {Factory}
  */
  function Authentication($cookies, $http, Snackbar) {
    /**
    * @name Authentication
    * @desc The Factory to be returned
    */
    var Authentication = {
      getAuthenticatedAccount: getAuthenticatedAccount,
      isAuthenticated: isAuthenticated,
      isAdmin: isAdmin,
      login: login,
      logout: logout,
      register: register,
      recoverPassword: recoverPassword,
      resetPassword: resetPassword,
      setAuthenticatedAccount: setAuthenticatedAccount,
      unauthenticate: unauthenticate
    };

    return Authentication;

    ////////////////////

    /**
    * @name register
    * @desc Try to register a new user
    * @param {string} first_name The first_name entered by the user
    * @param {string} last_name The last_name entered by the user
    * @param {string} password The password entered by the user
    * @param {string} email The email entered by the user
    * @returns {Promise}
    * @memberOf gestfg.authentication.services.Authentication
    */
    function register(email, dni, first_name, last_name) {
      return $http.post('/api/v1/alumnos/', {
        first_name: first_name,
        last_name: last_name,
        dni: dni,
        email: email
       }).then(registerSuccessFn, registerErrorFn);

      /**
      * @name registerSuccessFn
      * @desc Log the new user in
      */
      function registerSuccessFn(data, status, headers, config) {
        //window.location = '/login';
        //Authentication.login(email, password);
        Snackbar.success("Compruebe el correo indicado para activar su cuenta.");
      }

      /**
      * @name registerErrorFn
      * @desc Log "Epic failure!" to the console
      */
      function registerErrorFn(data, status, headers, config) {
        // console.error('Epic failure!');
        // jQuery.each(data.data.message, function(i, val) {
        //   Snackbar.error(i + ": " + val[0]);
        // });
        Snackbar.error(data.data.message);
      }
    }

    /**
     * @name login
     * @desc Try to log in with email `email` and password `password`
     * @param {string} email The email entered by the user
     * @param {string} password The password entered by the user
     * @returns {Promise}
     * @memberOf gestfg.authentication.services.Authentication
     */
    function login(email, password) {
      return $http.post('/api/v1/auth/login/', {
        email: email, password: password
      }).then(loginSuccessFn, loginErrorFn);

      /**
       * @name loginSuccessFn
       * @desc Set the authenticated account and redirect to index
       */
      function loginSuccessFn(data, status, headers, config) {
        Authentication.setAuthenticatedAccount(data.data);

        window.location = '/';
      }

      /**
       * @name loginErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function loginErrorFn(data, status, headers, config) {
        var message = data.data.message;

        if(!message && data.status==401){
          message = 'Usuario/contraseña no coinciden';
        }

        Snackbar.error(message);
      }
    }

    /**
     * @name recoverPassword
     * @desc send recover password request for email provided
     * @param {string} email The email entered by the user
     * @returns {Promise}
     * @memberOf gestfg.authentication.services.Authentication
     */
    function recoverPassword(email) {
      return $http.post('/api/v1/auth/reset_password', {
        email: email
      }).then(recoverPasswordSuccessFn, recoverPasswordErrorFn);

      /**
       * @name recoverPasswordSuccessFn
       * @desc Show success message
       */
      function recoverPasswordSuccessFn(data, status, headers, config) {
        Snackbar.success("Se le ha enviado un enlace para reestrablecer la contraseña");
      }

      /**
       * @name recoverPasswordErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function recoverPasswordErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.message);
      }
    }


    /**
     * @name resetPassword
     * @desc send reset password request for token provided
     * @returns {Promise}
     * @memberOf gestfg.authentication.services.Authentication
     */
    function resetPassword(password, repassword, uidb64, token) {
      return $http.post('/api/v1/auth/password_reset_confirm/', {
        token: token,
        uidb64: uidb64,
        new_password1: password,
        new_password2: repassword
      }).then(resetPasswordSuccessFn, resetPasswordErrorFn);

      /**
       * @name resetPasswordSuccessFn
       * @desc Show success message
       */
      function resetPasswordSuccessFn(data, status, headers, config) {
        Snackbar.success("Se le ha enviado un enlace para reestrablecer la contraseña");
      }

      /**
       * @name resetPasswordErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function resetPasswordErrorFn(data, status, headers, config) {
        if(data.status>500){
          Snackbar.error('Error interno');
        } else {
          Snackbar.error(data.data.message);
        }
      }
    }

    /**
     * @name getAuthenticatedAccount
     * @desc Return the currently authenticated account
     * @returns {object|undefined} Account if authenticated, else `undefined`
     * @memberOf gestfg.authentication.services.Authentication
     */
    function getAuthenticatedAccount() {
      if (!$cookies.authenticatedAccount) {
        return;
      }

      return JSON.parse($cookies.authenticatedAccount);
    }

    /**
     * @name isAuthenticated
     * @desc Check if the current user is authenticated
     * @returns {boolean} True is user is authenticated, else false.
     * @memberOf gestfg.authentication.services.Authentication
     */
    function isAuthenticated() {
      return !!$cookies.authenticatedAccount;
    }

    /**
     * @name isAdmin
     * @desc Check if the current user is admin
     * @returns {boolean} True is user is admin, else false.
     * @memberOf gestfg.authentication.services.Authentication
     */
    function isAdmin() {
      var user = getAuthenticatedAccount();
      return (user === undefined) ? false : user.data.is_admin;
    }

    /**
     * @name setAuthenticatedAccount
     * @desc Stringify the account object and store it in a cookie
     * @param {Object} user The account object to be stored
     * @returns {undefined}
     * @memberOf gestfg.authentication.services.Authentication
     */
    function setAuthenticatedAccount(account) {
      $cookies.authenticatedAccount = JSON.stringify(account);
    }

    /**
     * @name unauthenticate
     * @desc Delete the cookie where the user object is stored
     * @returns {undefined}
     * @memberOf gestfg.authentication.services.Authentication
     */
    function unauthenticate() {
      delete $cookies.authenticatedAccount;
    }

    /**
     * @name logout
     * @desc Try to log the user out
     * @returns {Promise}
     * @memberOf gestfg.authentication.services.Authentication
     */
    function logout() {
      return $http.post('/api/v1/auth/logout/')
        .then(logoutSuccessFn, logoutErrorFn);

      /**
       * @name logoutSuccessFn
       * @desc Unauthenticate and redirect to index with page reload
       */
      function logoutSuccessFn(data, status, headers, config) {
        Authentication.unauthenticate();

        window.location = '/';
      }

      /**
       * @name logoutErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function logoutErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }

  }
})();
