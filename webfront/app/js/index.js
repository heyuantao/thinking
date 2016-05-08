/**
 * Created by hyt on 16-5-8.
 */
/**
 * Created by hyt on 16-5-7.
 */
var app=angular.module('indexApp',[])
app.controller('indexController',['$scope','$http',function($scope,$http){
    $scope.msg="hello word!";
    $http.get("http://networkhoststatus.hudieshanfood.com/api/status/")
        .success(function(response){
            $scope.hostList=response.networks['192.168.0.1/24'];
        })
}])
app.filter('portFilter',function(){
    return function(value){
        if(value>0){
            return "在线"
        }else{
            return "离线"
        }
    }
});