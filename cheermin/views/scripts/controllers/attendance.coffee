'use strict'

###*
 # @ngdoc function
 # @name cheerminWebappApp.controller:AttendanceCtrl
 # @description
 # # AttendanceCtrl
 # Controller of the cheerminWebappApp
###
angular.module('cheermin')
  .controller 'AttendanceController', (Athletes) ->
    @athletes = Athletes.query()
    return
