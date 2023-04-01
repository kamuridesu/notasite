Title: Django Rest Framework Notes
Date: 2023-04-01 14:12


## Differences between APIView and ViewSet

### Viewsets

Viewsets are a abstraction on top of APIView. It provides a lot of methods already defined to perform simple CRUD operations.

Viewsets can be very easy to use and makes the development faster, in detriment of having control of every operation.

### APIView

APIView is the base for all other Api Views classes in DRF. If you want to have more control about your crud operations and avoid dealing with all the Viewsets and GenericViews abstractions, this is the way to go.

APIView also takes more time, as you'll have to implement everything yourself. And this mean a lot more code.


