app.controller('WishlistController', ['$scope','$http','$location', function($scope,$http,$location){
	if(localStorage.userID == null){
		$location.url("/")
	}

	config = {

			headers:{'Accept': "json"}

		}

	$http.get('/api/users/'+localStorage.userID+'/wishlist', config).then(function(response){
		
			$scope.wishlist = response.data.wishlist
			$scope.url = response.data.wishlist[0].thumbnail
			console.log($scope.wishlist)
			console.log($scope.url)
	
	})

	$scope.addNew = function(){
		$location.url('/wishlist/new')
	}


}])