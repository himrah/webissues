/**
 * Created by rahul on 25/10/16.
 */
(function(angular){
    'use strict';
    angular.module("myapp",[])
        .controller("HelloController", function($scope) {
        $scope.helloTo = {};
        $scope.helloTo.title = "AngularJS";
        $scope.helloTo.body="This is body of anglar";
        this.counter=0;
        this.cl=function(){
        this.counter++;
        }
        })
})(window.angular);