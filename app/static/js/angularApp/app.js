app  = angular.module('WishlistApp', ['ngRoute']);

app.config(['$routeProvider',function($routeProvider, $locationProvider){

	$routeProvider
	.when('/', {
		templateUrl: '/static/js/angularApp/Views/homePage.html',
		controller :'HomeController'
	})
	.when('/register',{
		controller: 'RegisterController',
		templateUrl: '/static/js/angularApp/Views/register.html'
	})
	.when('/login',{
		controller: 'LoginController',
		templateUrl: '/static/js/angularApp/Views/login.html'
	})
	.when('/logout',{
		controller:'LogoutController',
		template: ""
	})
	.when('/wishlist',{
		controller:'WishlistController',
		templateUrl:'/static/js/angularApp/Views/wishlist.html'
	})
	.when('/wishlist/new',{
		controller: 'NewItemController',
		templateUrl: '/static/js/angularApp/Views/new.html'
	})
	.when('/wishlist/share',{
		controller:"ShareController",
		templateUrl:'/static/js/angularApp/Views/share.html'
	})
	.otherwise({
		redirectTo:'/'
	})


}])
