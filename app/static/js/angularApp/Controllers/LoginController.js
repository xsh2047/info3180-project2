app.controller('LoginController', ['$scope', '$http', '$location',function($scope, $http, $location){
	
	if(localStorage.userID != null){
		$location.url('/wishlist')
	}

	$scope.login = function(){
		data = {
			'email':$scope.email,
			'password':$scope.password
		}

		console.log("password")
		console.log($scope.password)
		console.log("encoded password")
		console.log(btoa($scope.password))
		console.log("decoded password")
		console.log(atob(btoa($scope.password)))

		config = {

			headers:{'Content-Type': "application/json"}

		}

		$http.post('/api/users/login', data, config).then(function(response){
			if(response.data.message =="Success"){
				localStorage.setItem("name", response.data.data.user.name)
				localStorage.setItem("userID", response.data.data.user.id)
				localStorage.setItem("username", response.data.data.user.email)
				localStorage.setItem("token", btoa(response.data.data.user.email + ":" + $scope.password))
				console.log(localStorage)
				$location.url('/wishlist')
			}
			else{
				console.log(response.data.message)
			}
			
		})
	}
}])