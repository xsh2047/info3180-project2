app.controller('WishlistController', ['$scope','$http','$location', function($scope,$http,$location){
	if(localStorage.userID == null){
		$location.url("/")
	}

	config = {

			headers:{'Accept': "json",
			"Authorization":"Basic " +localStorage.token

		}


		}

	$http.get('/api/users/'+localStorage.userID+'/wishlist', config).then(function(response){
		
			if(response.data.message =="Success"){
				console.log(response.data)
				$scope.wishlist = response.data.data.items
				// $scope.url = response.data.data.items[0].thumbnail_url
				// console.log($scope.wishlist)
				// console.log($scope.url)
			}else{
				console.log(response.data.message)
			}
			
	
	})

	$scope.addNew = function(){
		$location.url('/wishlist/new')
	}


}])