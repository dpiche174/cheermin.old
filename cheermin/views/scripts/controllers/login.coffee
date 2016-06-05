'use strict'

###*
 # @ngdoc function
 # @name cheerminWebappApp.controller:LoginCtrl
 # @description
 # # LoginCtrl
 # Controller of the cheerminWebappApp
###
app = angular.module('cheermin')

# Application Controller
app.controller 'ApplicationController', ->

# Attendance Controller
app.controller 'AttendanceController', ->
  @athletes = athletes

# Login Controller
app.controller 'LoginController', ($scope, $rootScope, AUTH_EVENTS, AuthService) ->
  $scope.credentials = { username: ''
                       , password: ''
                       }
  $scope.login (credentials) ->
    AuthService.login(credentials).then(
      (user) ->
        $rootScope.$broadcast(AUTH_EVENTS.loginSuccess)
        $scope.setCurrentUser(user)
    , () ->
        $rootScope.$broadcast(AUTH_EVENTS.loginFailed)
    )
  return

# Authentication Service
app.factory 'AuthService', ($http, Session) ->
    authService = {}

    authService.login (credentials) ->
        $http.post('/login', credentials).then((res) ->
            Session.create(res.data.id, res.data.user.id, res.data.user.role)
            return res.data.user
        )

    authService.isAuthenticated () ->
        return !!Session.userId

    authService.isAuthorized (authorizedRoles) ->
        if !angular.isArray(authorizedRoles)
            authorizedRoles = [authorizedRoles]
      return authService.isAuthenticated() and authorizedRoles.indexOf(Session.userRole) != -1

    return authService

