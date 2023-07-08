from rest_framework.throttling import UserRateThrottle
#dekh yaha mene UserRateThrottle import kiya h mtlb m login user pr laga raha hu 

class ReviewCreateThrottle(UserRateThrottle):
    scope = "review-create"

class ReviewListThrottle(UserRateThrottle):
    scope = "review-list"